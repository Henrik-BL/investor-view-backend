import json
import ast
import logging
from pathlib import Path

from hcnb_stock_data.currency_service import CurrencyService
from hcnb_stock_data.hcnb_stock_data import HcnbStockData

from .stock_price_potential import StockPricePotential
from .buy_sell_signals_service import BuySellSignalsService

_logger = logging.getLogger(__name__)


class MainPortfolioService:

    def __init__(self, hcnb_stock_data_c: HcnbStockData):
        self.hcnb_stock_data_c = hcnb_stock_data_c
        self.currency_service = CurrencyService()
        self.buy_sell_signals_service = BuySellSignalsService(self.hcnb_stock_data_c)
        self.portfolio_file_path = Path(__file__).resolve().parents[1] / 'portfolio_data' / 'main_portfolio.json'

    def get_portfolio_overview(self):
        total_value = 0
        portfolio_holding = self._load_portfolio_holdings()
        existing_tickers = self.hcnb_stock_data_c.get_all_tickers()

        for holding in portfolio_holding:
            if holding['ticker'] not in existing_tickers:
                self.hcnb_stock_data_c.get_stock_data(holding['ticker'], True)
            stock_data = self.hcnb_stock_data_c.get_stock_data(holding['ticker'], False)
            holding_value = stock_data.price * holding['quantity']
            holding_value_sek = round(self.currency_service.convert(holding_value, stock_data.currency, "SEK"))
            holding['holding_value_sek'] = holding_value_sek
            total_value += holding_value_sek
            holding['sector'] = stock_data.sector
            holding['industry'] = stock_data.industry
            holding['buy_sell_signals'] = self.buy_sell_signals_service.get_buy_sell_signal(stock_data)
            stock_price_potential = StockPricePotential(stock_data)
            holding['stock_price_potential'] = stock_price_potential.get_result()

        for holding in portfolio_holding:
            holding['holding_value_percentage'] = round((holding['holding_value_sek'] / total_value) * 100, 2) if total_value > 0 else 0

        sector_percentage = self._calculate_group_percentage(portfolio_holding, 'sector', total_value)
        industry_percentage = self._calculate_group_percentage(portfolio_holding, 'industry', total_value)

        portfolio_holding.sort(key=lambda item: item["holding_value_sek"], reverse=True)

        return {
            "total_value_sek": total_value,
            "holdings": portfolio_holding,
            "sector_percentage": sector_percentage,
            "industry_percentage": industry_percentage
        }

    @staticmethod
    def _calculate_group_percentage(holdings: list[dict], group_key: str, total_value: float) -> list[dict]:
        grouped_data = {}

        for holding in holdings:
            group_value = holding.get(group_key) or "Unknown"
            holding_value = holding.get('holding_value_sek', 0)
            ticker = holding.get('ticker')

            if group_value not in grouped_data:
                grouped_data[group_value] = {
                    "value_sek": 0,
                    "tickers": set(),
                }

            grouped_data[group_value]["value_sek"] += holding_value
            if ticker:
                grouped_data[group_value]["tickers"].add(ticker)

        result = []
        for group_value, data in grouped_data.items():
            value_sek = data["value_sek"]
            result.append({
                group_key: group_value,
                "value_sek": value_sek,
                "percentage": round((value_sek / total_value) * 100, 2) if total_value > 0 else 0,
                "tickers": sorted(data["tickers"]),
            })

        result.sort(key=lambda item: item["percentage"], reverse=True)
        return result

    def _load_portfolio_holdings(self) -> list[dict]:
        if not self.portfolio_file_path.exists():
            return []
        with self.portfolio_file_path.open('r', encoding='utf-8') as f:
            raw_content = f.read()

        if not raw_content.strip():
            return []

        data = None
        try:
            data = json.loads(raw_content)
        except json.JSONDecodeError:
            try:
                # Backward compatibility for legacy portfolio files written as Python literals.
                data = ast.literal_eval(raw_content)
            except (ValueError, SyntaxError):
                _logger.exception("Failed to parse portfolio file: %s", self.portfolio_file_path)
                return []

        holdings = []
        if isinstance(data, dict):
            raw_holdings = data.get('holdings', [])
            if isinstance(raw_holdings, list):
                holdings = raw_holdings
        elif isinstance(data, list):
            normalized_holdings = []
            ignored_entries = 0

            for item in data:
                if isinstance(item, str):
                    ticker = item.strip()
                    if ticker:
                        normalized_holdings.append({
                            "ticker": ticker,
                            "quantity": 1,
                            "account": "",
                        })
                    continue

                if isinstance(item, dict) and item.get('ticker'):
                    normalized_holdings.append(item)
                else:
                    ignored_entries += 1

            if ignored_entries:
                _logger.warning(
                    "Ignored %d unsupported portfolio entries in %s",
                    ignored_entries,
                    self.portfolio_file_path,
                )

            holdings = normalized_holdings

        aggregated_holdings = self._get_aggregated_holdings(holdings)
        return aggregated_holdings

    @staticmethod
    def _get_aggregated_holdings(holdings: list[dict]) -> list[dict]:
        aggregated = []
        unique_tickers = []

        for holding in holdings:
            ticker = str(holding.get('ticker', '')).strip()
            if not ticker:
                continue
            if ticker not in unique_tickers:
                unique_tickers.append(ticker)

        for ticker in unique_tickers:
            quantity = 0
            accounts = []
            for holding in holdings:
                holding_ticker = str(holding.get('ticker', '')).strip()
                if holding_ticker == ticker:
                    quantity += MainPortfolioService._coerce_quantity(holding.get('quantity'))
                    accounts.append(holding.get('account', ''))

            aggregated.append({
                "ticker": ticker,
                "quantity": quantity,
                "accounts": accounts
            })

        return aggregated

    @staticmethod
    def _coerce_quantity(raw_quantity) -> float:
        if raw_quantity is None:
            return 0
        if isinstance(raw_quantity, (int, float)):
            return raw_quantity
        try:
            return float(raw_quantity)
        except (TypeError, ValueError):
            return 0
