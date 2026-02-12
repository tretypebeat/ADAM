"""Autonomous Coinbase trader with a simple threshold strategy.

Environment variables for live mode:
- COINBASE_API_KEY
- COINBASE_API_SECRET (base64-encoded)
- COINBASE_API_PASSPHRASE

Example (paper mode):
    python coinbase_trader.py --product BTC-USD --buy-below 50000 --sell-above 53000 --budget 100 --iterations 3

Example (live mode):
    python coinbase_trader.py --product BTC-USD --buy-below 50000 --sell-above 53000 --budget 100 --live
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from urllib import request


@dataclass(frozen=True)
class TradeDecision:
    action: str
    price: float
    reason: str


class CoinbaseExchangeClient:
    """Minimal Coinbase Exchange REST client for ticker + market orders."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        passphrase: str,
        base_url: str = "https://api.exchange.coinbase.com",
    ) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.base_url = base_url.rstrip("/")

    def _timestamp(self) -> str:
        return str(time.time())

    def _signature(self, timestamp: str, method: str, request_path: str, body: str = "") -> str:
        message = f"{timestamp}{method.upper()}{request_path}{body}".encode("utf-8")
        secret = base64.b64decode(self.api_secret)
        digest = hmac.new(secret, message, hashlib.sha256).digest()
        return base64.b64encode(digest).decode("utf-8")

    def _headers(self, method: str, path: str, body: str = "") -> dict[str, str]:
        ts = self._timestamp()
        return {
            "Content-Type": "application/json",
            "CB-ACCESS-KEY": self.api_key,
            "CB-ACCESS-SIGN": self._signature(ts, method, path, body),
            "CB-ACCESS-TIMESTAMP": ts,
            "CB-ACCESS-PASSPHRASE": self.passphrase,
        }

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        body = json.dumps(payload) if payload else ""
        data = body.encode("utf-8") if body else None
        req = request.Request(
            url=f"{self.base_url}{path}",
            method=method.upper(),
            data=data,
            headers=self._headers(method, path, body),
        )
        with request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}

    def get_ticker(self, product_id: str) -> dict[str, Any]:
        return self._request("GET", f"/products/{product_id}/ticker")

    def place_market_order(self, product_id: str, side: str, funds: float | None = None, size: float | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "type": "market",
            "side": side,
            "product_id": product_id,
        }
        if funds is not None:
            payload["funds"] = f"{funds:.2f}"
        if size is not None:
            payload["size"] = f"{size:.8f}"
        return self._request("POST", "/orders", payload)


class AutonomousTrader:
    """Stateful threshold trader that can run in dry-run or live mode."""

    def __init__(
        self,
        client: CoinbaseExchangeClient,
        product_id: str,
        buy_below: float,
        sell_above: float,
        quote_budget: float,
        dry_run: bool = True,
    ) -> None:
        if buy_below >= sell_above:
            raise ValueError("buy_below must be less than sell_above")
        self.client = client
        self.product_id = product_id
        self.buy_below = buy_below
        self.sell_above = sell_above
        self.quote_budget = quote_budget
        self.dry_run = dry_run
        self.base_position_size = 0.0

    def _current_price(self) -> float:
        ticker = self.client.get_ticker(self.product_id)
        return float(ticker["price"])

    def decide(self, price: float) -> TradeDecision:
        if self.base_position_size <= 0 and price <= self.buy_below:
            return TradeDecision("buy", price, f"price {price:.2f} <= buy_below {self.buy_below:.2f}")
        if self.base_position_size > 0 and price >= self.sell_above:
            return TradeDecision("sell", price, f"price {price:.2f} >= sell_above {self.sell_above:.2f}")
        return TradeDecision("hold", price, "thresholds not met")

    def step(self) -> TradeDecision:
        price = self._current_price()
        decision = self.decide(price)

        if decision.action == "buy":
            if not self.dry_run:
                self.client.place_market_order(self.product_id, "buy", funds=self.quote_budget)
            self.base_position_size = self.quote_budget / price
        elif decision.action == "sell":
            if not self.dry_run:
                self.client.place_market_order(self.product_id, "sell", size=self.base_position_size)
            self.base_position_size = 0.0

        return decision

    def run(self, interval_seconds: int, iterations: int | None = None) -> None:
        count = 0
        while iterations is None or count < iterations:
            decision = self.step()
            timestamp = datetime.now(tz=timezone.utc).isoformat()
            print(f"[{timestamp}] {self.product_id} price={decision.price:.2f} action={decision.action} ({decision.reason})")
            count += 1
            if iterations is None or count < iterations:
                time.sleep(interval_seconds)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Autonomous Coinbase threshold trader")
    parser.add_argument("--product", default="BTC-USD", help="Coinbase product id, e.g., BTC-USD")
    parser.add_argument("--buy-below", type=float, required=True, help="Buy threshold price")
    parser.add_argument("--sell-above", type=float, required=True, help="Sell threshold price")
    parser.add_argument("--budget", type=float, default=100.0, help="Quote currency budget per buy")
    parser.add_argument("--interval", type=int, default=30, help="Seconds between checks")
    parser.add_argument("--iterations", type=int, default=1, help="How many cycles to run")
    parser.add_argument("--live", action="store_true", help="Enable live trading (default is paper mode)")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    api_key = os.getenv("COINBASE_API_KEY", "")
    api_secret = os.getenv("COINBASE_API_SECRET", "")
    passphrase = os.getenv("COINBASE_API_PASSPHRASE", "")

    if args.live and not all([api_key, api_secret, passphrase]):
        raise SystemExit("Live mode requires COINBASE_API_KEY, COINBASE_API_SECRET, COINBASE_API_PASSPHRASE")

    client = CoinbaseExchangeClient(
        api_key=api_key or "paper-key",
        api_secret=api_secret or base64.b64encode(b"paper-secret").decode("utf-8"),
        passphrase=passphrase or "paper-passphrase",
    )

    trader = AutonomousTrader(
        client=client,
        product_id=args.product,
        buy_below=args.buy_below,
        sell_above=args.sell_above,
        quote_budget=args.budget,
        dry_run=not args.live,
    )
    trader.run(interval_seconds=args.interval, iterations=args.iterations)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
