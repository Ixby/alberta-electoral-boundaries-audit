"""
Master QA Trigger

Executes the full PyTest mathematical/logic suite followed by the 
live data integrity check (run_audit.py). Outputs a unified Markdown
report containing the results of both chains with a timestamp.
"""
import subprocess
import datetime
from pathlib import Path

def main():
    root_dir = Path(__file__).resolve().parent
    logs_dir = root_dir / "tests" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = logs_dir / f"unified_qa_report_{timestamp}.md"
    
    print("Running Master QA Trigger...")
    
    # 1. Run the PyTest Suite
    print("-> 1/2: Executing PyTest Logic Suite...")
    pytest_cmd = ["python", "-m", "pytest", "tests/", "-v", "--disable-warnings"]
    try:
        pytest_result = subprocess.run(pytest_cmd, cwd=root_dir, capture_output=True, text=True, check=False)
        pytest_output = pytest_result.stdout
    except Exception as e:
        pytest_output = f"Error running pytest: {str(e)}"
        
    # 2. Run the Data Integrity Audit
    print("-> 2/2: Executing Data Integrity Audit (run_audit.py)...")
    audit_cmd = ["python", "run_audit.py"]
    try:
        audit_result = subprocess.run(audit_cmd, cwd=root_dir, capture_output=True, text=True, check=False)
        audit_output = audit_result.stdout
    except Exception as e:
        audit_output = f"Error running run_audit.py: {str(e)}"
        
    # 3. Compile Unified Report
    print(f"-> Compiling unified report: {report_path.name}")
    
    markdown_content = f"""# Master QA & Audit Report
**Timestamp:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This document contains the unified output of both the Mathematical/Logic QA Suite (PyTest) and the Live Data Integrity Audit.

## Part 1: Mathematical Test Suite (PyTest)
The mathematical test suite verifies the correctness of the analytical scripts (compactness, partisan symmetry, municipal splits, core retention, etc.).

```text
{pytest_output.strip()}
```

## Part 2: Data Integrity Audit (run_audit.py)
The data integrity audit checks the actual 2026 shapefiles for topological validity, coverage gaps, naming collisions, and vote assignment consistency.

```text
{audit_output.strip()}
```
"""
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    print("\n[SUCCESS] Master QA Complete.")
    print(f"[FILE] Unified Report generated at: {report_path.resolve()}")

if __name__ == "__main__":
    main()
