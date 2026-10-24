# ⚡ env-validator: CLI Environment Variable Validator & CI Linter

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](#)
[![CI/CD Ready](https://img.shields.io/badge/CI%2FCD-Ready%20(Exit%20Codes)-orange.svg)](#)

> **A zero-dependency CLI tool to validate local `.env` files against `.env.example` templates, catch missing environment variables, detect leaked production tokens, and prevent catastrophic deployment crashes.**

---

## 💥 The Problem It Solves

How many times has a production deployment failed or a team member spent 3 hours debugging because someone added a new secret to `.env` without documenting it in `.env.example`?

`env-validator` solves this instantly by acting as a fast linter in your development workflow, Git pre-commit hooks, and CI/CD pipelines.

---

## 🌟 Key Features

- ✅ **Zero Dependencies:** Pure Python standard library. Runs anywhere instantly without `pip install` overhead.
- 🔍 **Missing Keys Detection:** Flags any variable defined in your template that is missing from local `.env`.
- 🚨 **Secret Leak Protection:** Scans `.env.example` for accidentally committed live Stripe keys (`sk_live_...`), GitHub PAT tokens, or AWS credentials.
- ⚙️ **Auto-Template Generator:** Run with `--generate` to automatically create a clean `.env.example` from an existing `.env`.
- 🚦 **CI/CD Native:** Returns exit code `0` on success and `1` on failure, making it ideal for GitHub Actions and Git pre-commit hooks.

---

## 🚀 Quick Usage

### 1. Validate Your Environment
```bash
python env_validator.py --env .env --example .env.example
```

### 2. Strict Mode (Fail on Empty Values)
```bash
python env_validator.py --strict
```

### 3. Generate a Clean `.env.example` from `.env`
```bash
python env_validator.py --generate
```

---

## 🛠️ GitHub Actions CI Integration

Add this step to your `.github/workflows/test.yml`:

```yaml
- name: Validate Environment Variables
  run: |
    python env_validator.py --env .env.test --example .env.example
```

---

## ⚖️ License
Distributed under the MIT License. See `LICENSE` for details.
