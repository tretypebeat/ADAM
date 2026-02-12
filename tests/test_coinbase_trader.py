import base64

import pytest

from coinbase_trader import AutonomousTrader, CoinbaseExchangeClient


class FakeClient:
    def __init__(self, prices: list[float]) -> None:
        self.prices = prices
        self.index = 0
        self.orders: list[dict] = []

    def get_ticker(self, product_id: str) -> dict:
        price = self.prices[self.index]
        if self.index < len(self.prices) - 1:
            self.index += 1
        return {"price": str(price), "product_id": product_id}

    def place_market_order(self, product_id: str, side: str, funds=None, size=None) -> dict:
        payload = {"product_id": product_id, "side": side, "funds": funds, "size": size}
        self.orders.append(payload)
        return payload


def test_signature_matches_expected_value() -> None:
    secret = base64.b64encode(b"secret").decode("utf-8")
    client = CoinbaseExchangeClient("key", secret, "pass")

    signature = client._signature("1700000000", "GET", "/products/BTC-USD/ticker")

    assert signature == "YDOydtsTSmMWxUU0eN8iStRWgTs7tgOPkaOF2CunGS0="


def test_decide_buy_hold_sell_flow_in_dry_run() -> None:
    fake = FakeClient([90.0, 95.0, 120.0])
    trader = AutonomousTrader(fake, "BTC-USD", buy_below=100.0, sell_above=110.0, quote_budget=100.0, dry_run=True)

    first = trader.step()
    second = trader.step()
    third = trader.step()

    assert first.action == "buy"
    assert second.action == "hold"
    assert third.action == "sell"
    assert fake.orders == []


def test_live_mode_places_orders() -> None:
    fake = FakeClient([90.0, 120.0])
    trader = AutonomousTrader(fake, "BTC-USD", buy_below=100.0, sell_above=110.0, quote_budget=50.0, dry_run=False)

    trader.step()
    trader.step()

    assert len(fake.orders) == 2
    assert fake.orders[0]["side"] == "buy"
    assert fake.orders[0]["funds"] == 50.0
    assert fake.orders[1]["side"] == "sell"
    assert fake.orders[1]["size"] is not None


def test_threshold_validation() -> None:
    fake = FakeClient([100.0])
    with pytest.raises(ValueError, match="buy_below must be less than sell_above"):
        AutonomousTrader(fake, "BTC-USD", buy_below=100.0, sell_above=100.0, quote_budget=100.0)
