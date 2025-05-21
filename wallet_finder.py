#!/usr/bin/env python3
"""
wallet_finder.py

Recursively search specified root directories for known cryptocurrency wallet files
and folders, copy them (with collision-safe naming) into a target directory,
and print each match as it's processed—skipping any single file above MAX_FILE_SIZE.

Instructions:
 1. Run this from an elevated Windows cmd (Run as Administrator)
 2. python wallet_finder.py
"""

import os
import sys
import shutil
from pathlib import Path
import argparse

# ─── Configurable Defaults ─────────────────────────────────────────────────────

# Drives (or folders) to scan; override via CLI args if desired
ROOT_PATHS = [r"E:\\"]

# Base target directory; Findings will be placed under this
BASE_TARGET_DIR = Path(r"C:\Users\Max\Projects\wallet-finder")
TARGET_DIR = BASE_TARGET_DIR / "Findings"

# Skip any single file larger than this (bytes). Default: 100 MB.
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

# File extensions to look for
EXTENSIONS = {
    ".dat", ".wallet", ".keys", ".adb", ".log", ".chain", ".json", ".bin",
    ".db", ".sqlite", ".ldb", ".seed", ".backup", ".bak", ".txt",
    # Additional / proprietary
    ".aes.json", ".crypto", ".kdb", ".kdbx", ".gpg", ".pgp",
    ".kwallet", ".bip", ".p12", ".pfx", ".pem", ".asc",
    # Exodus
    ".seco",
}

# Folder names to copy wholesale
FOLDER_NAMES = {
    "Bitcoin", ".bitcoin",
    "Electrum", ".electrum",
    "Ethereum", ".ethereum",
    "Monero", ".bitmonero", ".monero",
    ".armory",
    # Wallet GUIs & Extensions
    "MetaMask", "Jaxx", "Exodus", "Edge", "Bread",
}

# ─── Utility Functions ─────────────────────────────────────────────────────────

def ensure_target():
    """Create target directory if it doesn't exist."""
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

def make_collision_safe(dest_path: Path) -> Path:
    """Append _1, _2… on name collisions."""
    if not dest_path.exists():
        return dest_path
    base, suffix = dest_path.stem, dest_path.suffix
    parent = dest_path.parent
    counter = 1
    while True:
        new_name = f"{base}_{counter}{suffix}"
        candidate = parent / new_name
        if not candidate.exists():
            return candidate
        counter += 1

def copy_file(src: Path):
    """Copy a file, unless it's too large."""
    size = src.stat().st_size
    if size > MAX_FILE_SIZE:
        print(f"[SKIP] {src}  ({size/1024/1024:.1f} MB > {MAX_FILE_SIZE/1024/1024:.1f} MB)")
        return
    dest = TARGET_DIR / src.name
    safe_dest = make_collision_safe(dest)
    shutil.copy2(src, safe_dest)
    print(f"[FILE] {src} → {safe_dest}")

def copy_folder(src: Path):
    """
    Copy a whole folder. We don't size-check folders—
    but individual files inside will still get size-checked if re-scanned.
    """
    dest = TARGET_DIR / src.name
    safe_dest = make_collision_safe(dest)
    shutil.copytree(src, safe_dest)
    print(f"[FOLDER] {src} → {safe_dest}")

# ─── Main Scan Logic ───────────────────────────────────────────────────────────

def scan_and_collect(roots):
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root, topdown=True):
            current = Path(dirpath)

            # If this directory matches a known wallet folder, grab it all:
            if current.name in FOLDER_NAMES:
                copy_folder(current)
                dirnames.clear()  # don't descend inside
                continue

            # Otherwise, inspect each file
            for fname in filenames:
                file_path = current / fname
                for ext in EXTENSIONS:
                    if fname.lower().endswith(ext):
                        copy_file(file_path)
                        break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find and copy cryptocurrency wallet files/folders."
    )
    parser.add_argument(
        "roots", nargs="*", default=ROOT_PATHS,
        help="Root paths to scan (default: %(default)s)"
    )
    parser.add_argument(
        "--target", "-t", default=str(BASE_TARGET_DIR),
        help="Base target directory (Findings subfolder will be created)"
    )
    parser.add_argument(
        "--max-size", "-m", type=int, default=MAX_FILE_SIZE,
        help="Max file size in bytes to copy (default: %(default)s)"
    )
    args = parser.parse_args()

    ROOT_PATHS[:] = args.roots
    BASE_TARGET_DIR = Path(args.target)
    TARGET_DIR = BASE_TARGET_DIR / "Findings"
    MAX_FILE_SIZE = args.max_size

    ensure_target()
    print("=== wallet_finder starting ===")
    print(f"Scanning: {ROOT_PATHS}")
    print(f"Collecting into: {TARGET_DIR}")
    print(f"Skipping files larger than: {MAX_FILE_SIZE/1024/1024:.1f} MB\n")

    try:
        scan_and_collect(ROOT_PATHS)
        print("\n=== Scan complete! ===")
    except PermissionError as e:
        print(f"[ERROR] Permission denied: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)
