"""
sentiment_monitoring.py

7 monitoring, error detection, error recovery, and error correction mechanisms
for sentiment analysis pipelines.

1. Detailed error logging with structured error types
2. Input validation layer
3. Output validation with reconciliation report
4. Retry strategy with exponential backoff
5. Health check module
6. Idempotent checkpoints for safe resumption
7. Real-time progress dashboard
"""

from __future__ import annotations

import csv
import json
import subprocess
import sys
import logging
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional
from enum import Enum
import hashlib
import shutil
import os
from threading import Lock, Semaphore

logger = logging.getLogger(__name__)

# ════════════════════════════════════════════════════════════════════════════════
# 1. DETAILED ERROR LOGGING WITH STRUCTURED ERROR TYPES
# ════════════════════════════════════════════════════════════════════════════════

class ErrorCategory(Enum):
    """Categorize errors for targeted recovery"""
    API_ERROR = "api_error"                    # Claude CLI exit code != 0
    JSON_PARSE_ERROR = "json_parse_error"      # Output not valid JSON
    SCHEMA_VALIDATION_ERROR = "schema_validation_error"  # Missing required fields
    TIMEOUT = "timeout"                        # Subprocess timeout
    MISSING_FIELD_ERROR = "missing_field_error"  # Row missing required input field
    INVALID_VALUE_ERROR = "invalid_value_error"  # Row has invalid data type/range
    UNKNOWN = "unknown"

@dataclass
class ErrorRecord:
    """Structured error record for logging and analysis"""
    submission_id: str
    edit_name: str
    category: ErrorCategory
    message: str
    timestamp: str
    retry_count: int = 0
    stderr_snippet: Optional[str] = None

    def to_dict(self):
        return {
            "submission_id": self.submission_id,
            "edit_name": self.edit_name,
            "category": self.category.value,
            "message": self.message,
            "timestamp": self.timestamp,
            "retry_count": self.retry_count,
            "stderr_snippet": self.stderr_snippet or "",
        }

class ErrorLogger:
    """Log structured errors with categorization (thread-safe)"""

    def __init__(self, error_log_path: Path):
        self.error_log_path = error_log_path
        self.errors = []
        self.lock = Lock()

    def log_error(self, error_record: ErrorRecord) -> None:
        """Add error to log (thread-safe)"""
        with self.lock:
            self.errors.append(error_record)

    def save(self) -> None:
        """Write all errors to CSV"""
        if not self.errors:
            return

        self.error_log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.error_log_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "submission_id", "edit_name", "category", "message", "timestamp",
                "retry_count", "stderr_snippet"
            ])
            writer.writeheader()
            for error in self.errors:
                writer.writerow(error.to_dict())

    def get_error_summary(self) -> dict:
        """Return categorized error counts"""
        summary = {}
        for error in self.errors:
            cat = error.category.value
            summary[cat] = summary.get(cat, 0) + 1
        return summary

# ════════════════════════════════════════════════════════════════════════════════
# 2. INPUT VALIDATION LAYER
# ════════════════════════════════════════════════════════════════════════════════

class InputValidator:
    """Pre-flight validation before processing"""

    REQUIRED_FIELDS = ["submission_id", "text"]

    @staticmethod
    def validate_submission(sub_id: str, text: str) -> tuple[bool, Optional[str]]:
        """Validate a single submission"""
        if not sub_id or len(sub_id) < 3:
            return False, f"Invalid submission_id: '{sub_id}'"

        if not isinstance(text, str) or len(text) < 10:
            return False, f"Invalid text for {sub_id}: too short or not string"

        return True, None

    @staticmethod
    def validate_file(submissions: dict[str, str]) -> dict:
        """Pre-flight check on all submissions"""
        results = {
            "total_submissions": len(submissions),
            "valid_submissions": 0,
            "invalid_submissions": 0,
            "errors": [],
        }

        for sub_id, text in submissions.items():
            is_valid, err = InputValidator.validate_submission(sub_id, text)
            if is_valid:
                results["valid_submissions"] += 1
            else:
                results["invalid_submissions"] += 1
                results["errors"].append(err)

        return results

class ValidationReport:
    """Write validation report to file"""

    @staticmethod
    def write(report: dict, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            f.write(f"Input Validation Report\n")
            f.write(f"=======================\n\n")
            f.write(f"Total submissions: {report['total_submissions']}\n")
            f.write(f"Valid: {report['valid_submissions']}\n")
            f.write(f"Invalid: {report['invalid_submissions']}\n\n")
            if report['errors']:
                f.write(f"Errors:\n")
                for err in report['errors'][:20]:
                    f.write(f"  - {err}\n")
                if len(report['errors']) > 20:
                    f.write(f"  ... and {len(report['errors']) - 20} more\n")

# ════════════════════════════════════════════════════════════════════════════════
# 3. OUTPUT VALIDATION WITH RECONCILIATION REPORT
# ════════════════════════════════════════════════════════════════════════════════

class OutputReconciler:
    """Compare input vs output and explain discrepancies"""

    @staticmethod
    def reconcile(
        input_submissions: dict[str, str],
        output_results: list[dict],
        error_log: ErrorLogger,
    ) -> dict:
        """Reconcile input vs output"""
        input_subs = set(input_submissions.keys())
        output_subs = set(r.get("submission_id") for r in output_results if isinstance(r, dict))
        errored_subs = set(e.submission_id for e in error_log.errors)

        missing = input_subs - output_subs - errored_subs
        unexpected = output_subs - input_subs

        return {
            "input_eligible": len(input_subs),
            "output_count": len(output_subs),
            "errored_count": len(errored_subs),
            "missing_count": len(missing),
            "unexpected_count": len(unexpected),
            "missing_submissions": sorted(missing),
            "unexpected_submissions": sorted(unexpected),
            "accounting": {
                "expected": len(input_subs),
                "actual": len(output_subs) + len(errored_subs),
                "unaccounted": len(missing),
            }
        }

    @staticmethod
    def write_report(reconciliation: dict, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            f.write(f"Output Reconciliation Report\n")
            f.write(f"============================\n\n")
            f.write(f"Input eligible: {reconciliation['input_eligible']}\n")
            f.write(f"Output count: {reconciliation['output_count']}\n")
            f.write(f"Errored count: {reconciliation['errored_count']}\n")
            f.write(f"Missing count: {reconciliation['missing_count']}\n")
            f.write(f"Unexpected count: {reconciliation['unexpected_count']}\n\n")
            f.write(f"Accounting:\n")
            f.write(f"  Expected: {reconciliation['accounting']['expected']}\n")
            f.write(f"  Actual (output + errored): {reconciliation['accounting']['actual']}\n")
            f.write(f"  Unaccounted: {reconciliation['accounting']['unaccounted']}\n\n")
            if reconciliation['missing_submissions']:
                f.write(f"Missing submissions (first 20):\n")
                for sub_id in reconciliation['missing_submissions'][:20]:
                    f.write(f"  - {sub_id}\n")

# ════════════════════════════════════════════════════════════════════════════════
# 4. RETRY STRATEGY WITH EXPONENTIAL BACKOFF
# ════════════════════════════════════════════════════════════════════════════════

class RetryStrategy:
    """Decide which errors to retry and with what backoff"""

    TRANSIENT_CATEGORIES = {
        ErrorCategory.TIMEOUT,
        ErrorCategory.API_ERROR,
    }
    PERMANENT_CATEGORIES = {
        ErrorCategory.JSON_PARSE_ERROR,
        ErrorCategory.SCHEMA_VALIDATION_ERROR,
        ErrorCategory.INVALID_VALUE_ERROR,
    }
    MAX_RETRIES = 2  # REDUCED from 3 (each retry adds 2-4 seconds)
    INITIAL_BACKOFF_SECS = 1  # REDUCED from 2 (1s, 2s, 4s instead of 2s, 4s, 8s)
    RATE_LIMIT_DELAY_SECS = 0.5  # NEW: Delay between API calls to avoid rate limiting

    @staticmethod
    def should_retry(error_category: ErrorCategory) -> bool:
        """Check if error is transient and should be retried"""
        return error_category in RetryStrategy.TRANSIENT_CATEGORIES

    @staticmethod
    def backoff_delay(attempt: int) -> float:
        """Return seconds to wait before retry attempt N (exponential backoff)"""
        return RetryStrategy.INITIAL_BACKOFF_SECS * (2 ** (attempt - 1))

    @staticmethod
    def should_give_up(error_record: ErrorRecord) -> bool:
        """Decide if error is permanent or max retries exhausted"""
        if error_record.category in RetryStrategy.PERMANENT_CATEGORIES:
            return True
        if error_record.retry_count >= RetryStrategy.MAX_RETRIES:
            return True
        return False

# ════════════════════════════════════════════════════════════════════════════════
# 4b. RATE LIMITER (Prevents API throttling)
# ════════════════════════════════════════════════════════════════════════════════

class AdaptiveThrottle:
    """
    TCP-style slow-start + AIMD congestion control for API concurrency and pacing.

    Concurrency (coarse): starts at initial_workers, doubles each ROUND_SIZE successes
    (slow start) until ssthresh, then +1/round (congestion avoidance). On error:
    ssthresh = active//2, demote toward ssthresh, switch to additive.

    Delay (fine): additive decrease on success, multiplicative increase on error.

    Two locks prevent deadlock: _rate_lock is held during sleep (serializes pacing);
    _concur_lock is never held during sleep (release_slot never blocks on sleep).
    """

    ROUND_SIZE = 10  # successes per concurrency-promotion round

    def __init__(
        self,
        initial_workers: int = 2,
        max_workers: int = 6,
        delay_secs: float = 5.0,
        min_secs: float = 1.5,
        max_secs: float = 30.0,
        additive_dec: float = 0.05,
        timeout_mult: float = 2.0,
        error_mult: float = 1.5,
    ):
        import random, time
        # Concurrency state
        self._active = initial_workers
        self._max = max_workers
        self._ssthresh = max_workers      # start in pure slow-start
        self._in_slow_start = True
        self._round_successes = 0
        self._pending_demotes = 0         # slots to retire on next release_slot()
        self._semaphore = Semaphore(initial_workers)
        self._concur_lock = Lock()
        # Rate state
        self._delay = delay_secs
        self._min = min_secs
        self._max_delay = max_secs
        self._add_dec = additive_dec
        self._timeout_mult = timeout_mult
        self._error_mult = error_mult
        self._last_call = 0.0
        self._rate_lock = Lock()
        self._time = time
        self._random = random

    # ── Slot management ──────────────────────────────────────────────────────

    def acquire_slot(self) -> None:
        """Block until a concurrency slot is available."""
        self._semaphore.acquire()

    def release_slot(self) -> None:
        """Return slot after work; retires it instead if demotions are pending."""
        with self._concur_lock:
            if self._pending_demotes > 0 and self._active > 1:
                self._pending_demotes -= 1
                self._active -= 1
                # Semaphore NOT released — slot retired.
            else:
                self._semaphore.release()

    # ── Rate pacing ──────────────────────────────────────────────────────────

    def wait_if_needed(self) -> None:
        """Sleep to enforce current inter-call delay, ±10% jitter (serialized)."""
        with self._rate_lock:
            jitter = self._delay * (1.0 + self._random.uniform(-0.1, 0.1))
            elapsed = self._time.time() - self._last_call
            if elapsed < jitter:
                self._time.sleep(jitter - elapsed)
            self._last_call = self._time.time()

    # ── Feedback ─────────────────────────────────────────────────────────────

    def record_success(self) -> None:
        """Additive delay decrease + slow-start/congestion-avoidance promotion."""
        with self._rate_lock:
            self._delay = max(self._min, self._delay - self._add_dec)
        with self._concur_lock:
            self._round_successes += 1
            if self._round_successes < self.ROUND_SIZE:
                return
            self._round_successes = 0
            if self._active >= self._max:
                return
            if self._in_slow_start and self._active < self._ssthresh:
                # Double: add min(_active, remaining_headroom) slots
                to_add = min(self._active, self._max - self._active)
                for _ in range(to_add):
                    self._active += 1
                    self._semaphore.release()
                if self._active >= self._ssthresh:
                    self._in_slow_start = False
            else:
                self._in_slow_start = False
                self._active += 1
                self._semaphore.release()

    def record_error(self, category=None) -> None:
        """Multiplicative delay increase + halve concurrency, enter additive mode."""
        with self._rate_lock:
            mult = self._timeout_mult if (
                category is not None and
                getattr(category, "value", "") in ("TIMEOUT", "API_ERROR")
            ) else self._error_mult
            self._delay = min(self._max_delay, self._delay * mult)
        with self._concur_lock:
            new_target = max(1, self._active // 2)
            demotes = self._active - new_target
            # Grab free slots immediately; defer the rest to release_slot()
            grabbed = 0
            for _ in range(demotes):
                if self._semaphore.acquire(blocking=False):
                    self._active -= 1
                    grabbed += 1
                else:
                    break
            self._pending_demotes += demotes - grabbed
            self._ssthresh = new_target
            self._in_slow_start = False
            self._round_successes = 0

    @property
    def active_workers(self) -> int:
        return self._active

# Keep RateLimiter as an alias for any external callers
RateLimiter = AdaptiveThrottle

# ════════════════════════════════════════════════════════════════════════════════
# 5. HEALTH CHECK MODULE
# ════════════════════════════════════════════════════════════════════════════════

class HealthChecker:
    """Pre-flight health checks before starting processing"""

    @staticmethod
    def check_claude_cli(claude_cmd: str) -> tuple[bool, str]:
        """Verify Claude CLI is installed and callable"""
        try:
            result = subprocess.run(
                [claude_cmd, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return True, f"Claude CLI found: {result.stdout.strip()}"
            else:
                return False, f"Claude CLI error: {result.stderr[:100]}"
        except FileNotFoundError:
            return False, f"Claude CLI not found: {claude_cmd}"
        except Exception as e:
            return False, f"Claude CLI check failed: {str(e)}"

    @staticmethod
    def check_api_connectivity(claude_cmd: str) -> tuple[bool, str]:
        """Test API connectivity with small API call"""
        try:
            result = subprocess.run(
                [claude_cmd, "--print", "--model", "haiku", "Say OK"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0 and "OK" in result.stdout:
                return True, "API connectivity OK"
            else:
                return False, f"Test call failed: {result.stderr[:100]}"
        except subprocess.TimeoutExpired:
            return False, "Test call timed out (API may be down)"
        except Exception as e:
            return False, f"API test failed: {str(e)}"

    @staticmethod
    def check_output_directory(output_dir: Path) -> tuple[bool, str]:
        """Verify output directory is writable"""
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            test_file = output_dir / ".health_check_test"
            test_file.write_text("ok")
            test_file.unlink()
            return True, f"Output directory writable: {output_dir}"
        except Exception as e:
            return False, f"Output directory not writable: {str(e)}"

    @staticmethod
    def run_all(claude_cmd: str, output_dir: Path) -> dict:
        """Run all health checks"""
        checks = {
            "claude_cli": HealthChecker.check_claude_cli(claude_cmd),
            "api_connectivity": HealthChecker.check_api_connectivity(claude_cmd),
            "output_directory": HealthChecker.check_output_directory(output_dir),
        }

        all_pass = all(status for status, _ in checks.values())
        return {
            "all_pass": all_pass,
            "checks": {name: msg for name, (status, msg) in checks.items()},
        }

# ════════════════════════════════════════════════════════════════════════════════
# 6. IDEMPOTENT CHECKPOINTS FOR SAFE RESUMPTION
# ════════════════════════════════════════════════════════════════════════════════

class CheckpointManager:
    """Safe resumption via checksums and atomic writes (thread-safe)"""

    _checkpoint_lock = Lock()  # Class-level lock for thread-safe checkpoint writes

    @staticmethod
    def compute_checksum(sub_id: str, edit_name: str) -> str:
        """Compute checksum of input to detect changes"""
        canonical = f"{sub_id}:{edit_name}"
        return hashlib.sha256(canonical.encode()).hexdigest()[:8]

    _FIELDS = [
        "submission_id", "edit_name", "input_checksum", "output_checksum",
        "timestamp", "classification", "rating", "quote", "reasoning",
    ]

    @staticmethod
    def load_checkpoints(checkpoint_path: Path) -> dict:
        """Load checkpoints: {(sub_id, edit_name): {classification, rating, quote, reasoning, ...}}"""
        if not checkpoint_path.exists():
            return {}

        checkpoints = {}
        try:
            with checkpoint_path.open(encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    key = (row["submission_id"], row["edit_name"])
                    checkpoints[key] = {
                        "input_checksum":  row.get("input_checksum", ""),
                        "output_checksum": row.get("output_checksum", ""),
                        "classification":  row.get("classification", "Unrelated") or "Unrelated",
                        "rating":          int(row["rating"]) if row.get("rating", "").isdigit() else None,
                        "quote":           row.get("quote", ""),
                        "reasoning":       row.get("reasoning", ""),
                    }
        except Exception as e:
            logger.warning(f"Failed to load checkpoints: {e}")

        return checkpoints

    @staticmethod
    def save_checkpoint(
        sub_id: str,
        edit_name: str,
        input_hash: str,
        output_hash: str,
        checkpoint_path: Path,
        classification: str = "Unrelated",
        rating=None,
        quote: str = "",
        reasoning: str = "",
    ) -> None:
        """Write checkpoint with full result data (thread-safe, direct append)"""
        with CheckpointManager._checkpoint_lock:
            checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                if not checkpoint_path.exists():
                    with checkpoint_path.open("w", newline="", encoding="utf-8") as f:
                        csv.DictWriter(f, fieldnames=CheckpointManager._FIELDS).writeheader()
                with checkpoint_path.open("a", newline="", encoding="utf-8") as f:
                    csv.DictWriter(f, fieldnames=CheckpointManager._FIELDS).writerow({
                        "submission_id":  sub_id,
                        "edit_name":      edit_name,
                        "input_checksum": input_hash,
                        "output_checksum": output_hash,
                        "timestamp":      datetime.now().isoformat(),
                        "classification": classification,
                        "rating":         rating if rating is not None else "",
                        "quote":          quote,
                        "reasoning":      reasoning,
                    })
            except PermissionError as e:
                logger.warning(f"Could not write checkpoint: {e} - continuing anyway")
            except Exception as e:
                logger.warning(f"Checkpoint write error: {e} - continuing anyway")

# ════════════════════════════════════════════════════════════════════════════════
# 7. REAL-TIME PROGRESS DASHBOARD
# ════════════════════════════════════════════════════════════════════════════════

class ProgressDashboard:
    """Real-time progress tracking with colored ANSI dashboard"""

    # ANSI color codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

    # Unicode box drawing
    BOX_H = "─"
    BOX_V = "│"
    BOX_TL = "┌"
    BOX_TR = "┐"
    BOX_BL = "└"
    BOX_BR = "┘"
    BOX_T = "┬"
    BOX_B = "┴"
    BOX_L = "├"
    BOX_R = "┤"
    BOX_CROSS = "┼"

    def __init__(self, total_rows: int):
        self.total = max(1, total_rows)
        self.processed = 0
        self.successes = 0
        self.errors_by_category = {}
        self.start_time = datetime.now()
        self.last_update = self.start_time
        self.last_printed_line = 0  # Track how many lines to clear
        self.lock = Lock()  # Thread-safe updates

    def record_success(self):
        with self.lock:
            self.processed += 1
            self.successes += 1

    def record_error(self, category: ErrorCategory):
        with self.lock:
            self.processed += 1
            cat_key = category.value
            self.errors_by_category[cat_key] = self.errors_by_category.get(cat_key, 0) + 1

    def should_print(self) -> bool:
        """Print every 30 rows or every 3 seconds"""
        now = datetime.now()
        return (
            self.processed % max(1, max(30, self.total // 15)) == 0 or
            (now - self.last_update).total_seconds() >= 3
        )

    def _progress_bar(self, width: int = 25) -> str:
        """Generate colored progress bar"""
        if self.total == 0:
            return "█" * width

        filled = int(width * self.processed / self.total)
        empty = width - filled

        bar = "█" * filled + "░" * empty
        percentage = (self.processed / self.total) * 100

        if percentage < 33:
            color = self.RED
        elif percentage < 66:
            color = self.YELLOW
        else:
            color = self.GREEN

        return f"{color}{bar}{self.RESET}"

    def print_snapshot(self) -> None:
        """Print colored, real-time updating dashboard"""
        now = datetime.now()
        self.last_update = now
        elapsed = now - self.start_time

        success_rate = (self.successes / self.processed * 100) if self.processed > 0 else 0
        error_count = self.processed - self.successes
        pending = self.total - self.processed

        if self.processed > 0:
            rate = self.processed / elapsed.total_seconds()
            eta_secs = pending / rate if rate > 0 else 0
            eta = now + timedelta(seconds=eta_secs)
            eta_str = eta.strftime("%H:%M:%S")
        else:
            rate = 0
            eta_str = "—"

        # Format error summary with colors
        error_items = []
        for cat, count in sorted(self.errors_by_category.items()):
            error_items.append(f"{self.RED}{cat}{self.RESET}={self.BOLD}{count}{self.RESET}")
        error_summary = " • ".join(error_items) if error_items else f"{self.GREEN}none{self.RESET}"

        # Format elapsed time nicely
        elapsed_str = str(elapsed).split('.')[0]

        # Color-coded status
        if error_count == 0:
            status_color = self.GREEN
            status_text = "✓ RUNNING"
        else:
            status_color = self.YELLOW
            status_text = "⚠ RUNNING"

        # Build dashboard
        width = 70
        h_line = self.BOX_H * width

        output = []
        output.append(f"{self.CYAN}{self.BOX_TL}{h_line}{self.BOX_TR}{self.RESET}")

        # Title
        title = " Sentiment Analysis Progress "
        title_pad = width - len(title)
        output.append(f"{self.CYAN}{self.BOX_V}{self.RESET}{self.BOLD}{self.CYAN}{title}{self.RESET}{' ' * title_pad}{self.CYAN}{self.BOX_V}{self.RESET}")

        # Divider
        output.append(f"{self.CYAN}{self.BOX_L}{self.BOX_H * width}{self.BOX_R}{self.RESET}")

        # Status line
        status_line = f"{status_color}{status_text}{self.RESET}"
        output.append(f"{self.CYAN}{self.BOX_V}{self.RESET} {status_line:<30} {self.CYAN}{self.BOX_V}{self.RESET}")

        # Progress bar line
        pbar = self._progress_bar(25)
        pct_text = f"{(self.processed/self.total)*100:5.1f}%"
        prog_line = f"Progress: {pbar} {pct_text}"
        output.append(f"{self.CYAN}{self.BOX_V}{self.RESET} {prog_line:<58} {self.CYAN}{self.BOX_V}{self.RESET}")

        # Stats lines
        output.append(f"{self.CYAN}{self.BOX_L}{self.BOX_H * width}{self.BOX_R}{self.RESET}")

        # Processed
        processed_text = f"{self.BOLD}{self.processed:,}{self.RESET}/{self.total:,}"
        line = f"Processed: {processed_text:<20}"
        output.append(f"{self.CYAN}{self.BOX_V}{self.RESET} {line:<60} {self.CYAN}{self.BOX_V}{self.RESET}")

        # Success
        success_text = f"{self.GREEN}{self.BOLD}{self.successes:,}{self.RESET} ({success_rate:5.1f}%)"
        line = f"Success:   {success_text:<20}"
        output.append(f"{self.CYAN}{self.BOX_V}{self.RESET} {line:<60} {self.CYAN}{self.BOX_V}{self.RESET}")

        # Errors
        error_text = f"{self.RED}{self.BOLD}{error_count:,}{self.RESET}" if error_count > 0 else f"{self.GREEN}{error_count}{self.RESET}"
        line = f"Errors:    {error_text:<20}"
        output.append(f"{self.CYAN}{self.BOX_V}{self.RESET} {line:<60} {self.CYAN}{self.BOX_V}{self.RESET}")

        # Error breakdown
        if error_items:
            output.append(f"{self.CYAN}{self.BOX_V}{self.RESET} {error_summary:<60} {self.CYAN}{self.BOX_V}{self.RESET}")

        output.append(f"{self.CYAN}{self.BOX_L}{self.BOX_H * width}{self.BOX_R}{self.RESET}")

        # Timing lines
        elapsed_text = f"{self.BLUE}{self.BOLD}{elapsed_str}{self.RESET}"
        line = f"Elapsed:   {elapsed_text:<20}"
        output.append(f"{self.CYAN}{self.BOX_V}{self.RESET} {line:<60} {self.CYAN}{self.BOX_V}{self.RESET}")

        rate_text = f"{self.YELLOW}{self.BOLD}{rate:.2f}{self.RESET} rows/sec"
        line = f"Rate:      {rate_text:<20}"
        output.append(f"{self.CYAN}{self.BOX_V}{self.RESET} {line:<60} {self.CYAN}{self.BOX_V}{self.RESET}")

        eta_text = f"{self.BOLD}{eta_str}{self.RESET}"
        line = f"ETA:       {eta_text:<20}"
        output.append(f"{self.CYAN}{self.BOX_V}{self.RESET} {line:<60} {self.CYAN}{self.BOX_V}{self.RESET}")

        output.append(f"{self.CYAN}{self.BOX_BL}{h_line}{self.BOX_BR}{self.RESET}")

        # Print with carriage return to update in place
        dashboard = "\n".join(output)
        print(f"\r{dashboard}", end="", flush=True)
        print()  # Move to next line after dashboard
