"""
Cloudflare League of Entropy (Drand) Canonical Seed Generator
-------------------------------------------------------------
To ensure cryptographic impartiality of the MCMC simulations, the primary
audit seed is derived from a public, verifiable randomness beacon (drand)
rather than a hardcoded integer chosen by the author.

This prevents adversarial claims of "cherry-picking" the seed.

Pre-registered Round: 5500000 (pre-dates the audit run)
Randomness Hex: 45922177bf69644aa0b8f8043695221eacad1147dfde0967c72fbf3756ffacac
Signature: a3e407621f675ed8e1dae35703167315197c559ce6d1ebea264e571f8202a3ad793298926a84fae9e779f20b5c1732e5012baad520ae12274b89eb2618b1e1b9353cd028a83e849adcb5eb771b7b8c040aef407742a2299bc8cc68f2897ccd02

Any reviewer can query https://drand.cloudflare.com/public/5500000 to verify
this payload against the League of Entropy's public key.

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""

import hashlib

CANONICAL_ROUND = 5500000
CANONICAL_RANDOMNESS = (
    "45922177bf69644aa0b8f8043695221eacad1147dfde0967c72fbf3756ffacac"
)


def get_canonical_seed(salt: str = "") -> int:
    """
    Derives a 32-bit integer seed from the canonical drand randomness.
    The salt parameter allows deriving distinct seeds for different
    chains while strictly anchoring them to the same public beacon.
    """
    payload = CANONICAL_RANDOMNESS + salt
    # Use SHA256 to hash the randomness + salt
    h = hashlib.sha256(payload.encode("utf-8")).digest()
    # Extract the first 4 bytes as a 32-bit unsigned integer
    seed_int = int.from_bytes(h[:4], byteorder="big")
    # Limit to 0 - (2**32 - 1)
    return seed_int % (2**32)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Drand canonical seed")
    parser.add_argument("--salt", default="", help="Salt to append to randomness")
    args = parser.parse_args()
    seed = get_canonical_seed(args.salt)
    print(f"Drand Round: {CANONICAL_ROUND}")
    print(f"Salt: '{args.salt}'")
    print(f"Derived Seed: {seed}")
