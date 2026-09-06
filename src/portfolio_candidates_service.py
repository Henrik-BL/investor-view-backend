from hcnb_stock_data.hcnb_stock_data import HcnbStockData

from .future_valuation_service import FutureValuationService
from .buy_sell_signals_service import BuySellSignalsService
from .stock_score_service import StockScoreService


class PortfolioCandidatesService:

    def __init__(self, hcnb_stock_data: HcnbStockData):
        self.hcnb_stock_data = hcnb_stock_data
        self.stock_score_service = StockScoreService()
        self.buy_sell_signals_service = BuySellSignalsService(self.hcnb_stock_data)
        self.future_valuation_service = FutureValuationService()

    def get_main_portfolio_candidates(self):
        all_tickers = self.hcnb_stock_data.get_all_tickers()
        candidate_list = []

        for ticker in all_tickers:
            stock_data = self.hcnb_stock_data.get_stock_data(ticker, False)
            stock_score = self.stock_score_service.score_stock(stock_data)
            buy_sell_signal = self.buy_sell_signals_service.get_buy_sell_signal(stock_data)
            future_stock_valuation = self.future_valuation_service.get_valuation(stock_data)

            candidate_list.append({
                "ticker": ticker,
                "stock_score": stock_score,
                "buy_sell_signal": buy_sell_signal,
                "last_quarter_pe": stock_data.last_quarter_pe,
                "forward_pe": stock_data.forward_pe,
                "future_stock_valuation": future_stock_valuation
            })

        return candidate_list
