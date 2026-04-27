"""
Cloudflare League of Entropy (Drand) Canonical Seed Generator
-------------------------------------------------------------
To ensure cryptographic impartiality of the MCMC simulations, the primary
audit seed is derived from a public, verifiable randomness beacon (drand)
rather than a hardcoded integer chosen by the author.

This prevents adversarial claims of "cherry-picking" the seed.

Pre-registered Round: 6062459 (April 27, 2026)
Randomness Hex: b2adf1576dfe55c16f878d05e3624f4b0a4a6fffbd4d3576a3fedf7cd67024c7
Signature: b5f206c7dce67033711158bb2ae366a57c4dcc89b04531d1ce09cd9ae5c1921ae485bd247c53fdb8d93475252e529d19104acae9257a5c823b67b0065124e4de763f42e7472d40376cd20d7660048d1bc6a3bdf9a2fe8e0c58f8e679586e1f5b

Any reviewer can query https://drand.cloudflare.com/public/6062459 to verify
this payload against the League of Entropy's public key.
"""

import hashlib

CANONICAL_ROUND = 6062459
CANONICAL_RANDOMNESS = "b2adf1576dfe55c16f878d05e3624f4b0a4a6fffbd4d3576a3fedf7cd67024c7"

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
    seed_int = int.from_bytes(h[:4], byteorder='big')
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
