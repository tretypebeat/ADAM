# ADAM

**ADAM was beckoned, not built**.

ADAM now includes two command-line tools:

1. `adam.py` — mood-aware coding companion.
2. `coinbase_trader.py` — autonomous threshold trader for Coinbase Exchange.

## ADAM companion

ADAM is a tiny Python CLI companion that meets your current coding mood with practical guidance and immediate next steps.

### What ADAM does

- mood-aware coaching for coding sessions
- task-aware next-step suggestions
- concise output optimized for fast check-ins

Supported moods:

- focused
- curious
- tired
- stuck
- excited

### ADAM quick start

```bash
python adam.py --name Ada --mood curious --task "debug failing test"
```

### Explain what ADAM is

```bash
python adam.py --about
```

## Coinbase autonomous trader

`coinbase_trader.py` runs a simple threshold strategy:

- buys when price is below or equal to `--buy-below` and no position is open
- sells when price is above or equal to `--sell-above` and a position is open
- defaults to **paper mode** (no live orders)

### Trader quick start (paper mode)

```bash
python coinbase_trader.py --product BTC-USD --buy-below 50000 --sell-above 53000 --budget 100 --iterations 3
```

### Trader live mode (real orders)

Set credentials first:

```bash
export COINBASE_API_KEY="..."
export COINBASE_API_SECRET="..."
export COINBASE_API_PASSPHRASE="..."
```

Then run:

```bash
python coinbase_trader.py --product BTC-USD --buy-below 50000 --sell-above 53000 --budget 100 --iterations 10 --live
```

## Run tests

```bash
python -m pytest -q
```
