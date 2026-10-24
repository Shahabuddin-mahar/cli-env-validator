#!/usr/bin/env python3
"""
CLI Environment Variable Validator (env-check)
==============================================
Validates .env files against .env.example templates.
Detects missing keys, empty values, and exposed production secrets.
Zero dependencies - Works across Linux, macOS, and Windows.
"""

import argparse
import os
import re
import sys
from typing import Dict, List, Tuple

# Ensure UTF-8 stdout
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

VERSION = "1.0.0"

SECRET_PATTERNS = [
    r"sk_live_[0-9a-zA-Z]{24,}",        # Stripe Live Key
    r"ghp_[0-9a-zA-Z]{36}",              # GitHub Personal Access Token
    r"AIza[0-9A-Za-z\\-_]{35}",          # Google API Key
    r"AKIA[0-9A-Z]{16}",                 # AWS Access Key ID
    r"EAACEdEose0cBA[0-9A-Za-z]+",       # Meta Token
]

def parse_env_file(filepath: str) -> Dict[str, str]:
    env_vars = {}
    if not os.path.exists(filepath):
        return env_vars

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            # Ignore empty lines and comments
            if not line or line.startswith("#"):
                continue

            # Parse KEY=VALUE
            if "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip("'\"")
                env_vars[key] = val
    return env_vars

def check_leaked_secrets(filepath: str) -> List[Tuple[str, str]]:
    leaks = []
    if not os.path.exists(filepath):
        return leaks

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        for pattern in SECRET_PATTERNS:
            matches = re.findall(pattern, content)
            for m in matches:
                leaks.append((pattern, m[:6] + "..." + m[-4:]))
    return leaks

def generate_example_file(source_env: str, target_example: str):
    if not os.path.exists(source_env):
        print(f"[!] Source file '{source_env}' not found.")
        sys.exit(1)

    env_vars = parse_env_file(source_env)
    with open(target_example, "w", encoding="utf-8") as f:
        f.write(f"# Auto-generated template from {source_env}\n")
        f.write("# Replace dummy values with actual secrets in your local .env\n\n")
        for key in sorted(env_vars.keys()):
            f.write(f"{key}=your_{key.lower()}_here\n")
    print(f"[✓] Generated clean '{target_example}' with {len(env_vars)} keys.")

def main():
    parser = argparse.ArgumentParser(description="CLI Environment Variable Validator & CI Linter")
    parser.add_argument("--env", "-e", default=".env", help="Path to local .env file (default: .env)")
    parser.add_argument("--example", "-x", default=".env.example", help="Path to template file (default: .env.example)")
    parser.add_argument("--generate", "-g", action="store_true", help="Generate .env.example from your existing .env")
    parser.add_argument("--strict", action="store_true", help="Fail if .env has empty values")

    args = parser.parse_args()

    print(f"[*] CLI Environment Validator v{VERSION}")

    if args.generate:
        generate_example_file(args.env, args.example)
        sys.exit(0)

    if not os.path.exists(args.example):
        print(f"[!] Template file '{args.example}' not found.")
        print(f"    Tip: Run with --generate to create '{args.example}' from your '{args.env}'")
        sys.exit(1)

    example_vars = parse_env_file(args.example)
    local_vars = parse_env_file(args.env)

    # 1. Check for missing variables
    missing_keys = [k for k in example_vars if k not in local_vars]

    # 2. Check for empty variables in .env
    empty_keys = [k for k, v in local_vars.items() if not v and k in example_vars]

    # 3. Check for leaked live keys in .env.example
    example_leaks = check_leaked_secrets(args.example)

    # Report results
    has_error = False

    if example_leaks:
        print("\n🚨 [SECURITY ALERT] Live secrets detected inside template file (.env.example):")
        for p, preview in example_leaks:
            print(f"   -> Potential live token exposed: {preview}")
        has_error = True

    if missing_keys:
        print(f"\n❌ [ERROR] Missing {len(missing_keys)} required environment variable(s) in '{args.env}':")
        for k in missing_keys:
            print(f"   -> {k}")
        has_error = True

    if empty_keys and args.strict:
        print(f"\n⚠️ [WARNING] Empty values detected for required keys in '{args.env}':")
        for k in empty_keys:
            print(f"   -> {k} is empty")
        has_error = True

    if has_error:
        print("\n[!] Validation Failed! Please update your environment variables.")
        sys.exit(1)
    else:
        print(f"\n✅ [SUCCESS] All {len(example_vars)} required variables are properly defined in '{args.env}'!")
        sys.exit(0)

if __name__ == "__main__":
    main()
