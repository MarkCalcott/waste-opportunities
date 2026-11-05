# Terminal setup

Run a multiagent system using the command line and a personnel API key.

## Requirements

- Python 3.11 or newer (`python3 --version`)
- An Anthropic API key from https://console.anthropic.com/settings/keys
- A little credit on the account (billing page) — new keys start rate-limited

## 1. Get a key

Go to https://console.anthropic.com/settings/keys and create one. It starts
with `sk-ant-`. If the account is new, add a small amount of credit under
Billing — otherwise the first call comes back 429.

## 2. Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-cli.txt
```

## 3. Configure

Open `.env` and paste your key into `ANTHROPIC_API_KEY`. NB: Safeguard keys and don't upload to a public repository.

Leave `ANTHROPIC_MODEL` commented unless you want a model other
than `claude-sonnet-4-6`.

## 4. Preflight

```bash
python preflight.py
```

Three checks to ensure things are working. Get all three green before running the command line tool.

## 5. Run

Wairarapa vineyard, grape marc, straight through all four tiers.

```bash
python cli.py --example --stream 1
```

Other examples:

```bash
python cli.py                    # type your own operation, blank line to finish
python cli.py --example          # example, but you pick the stream
python cli.py --example --json   # raw profile output, then stop
```
