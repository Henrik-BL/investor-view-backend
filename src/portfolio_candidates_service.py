from hcnb_stock_data.hcnb_stock_data import HcnbStockData

from buy_sell_signals_service import BuySellSignalsService
from stock_score_service import StockScoreService


class PortfolioCandidatesService:

    def __init__(self, hcnb_stock_data: HcnbStockData):
        self.hcnb_stock_data = hcnb_stock_data
        self.stock_score_service = StockScoreService()
        self.buy_sell_signals_service = BuySellSignalsService(self.hcnb_stock_data)

    def get_main_portfolio_candidates(self):
        all_tickers = self.hcnb_stock_data.get_all_tickers()
        candidate_list = []

        for ticker in all_tickers:
            stock_data = self.hcnb_stock_data.get_stock_data(ticker, False)
            stock_score = self.stock_score_service.score_stock(stock_data)
            buy_sell_signal = self.buy_sell_signals_service.get_buy_sell_signal(stock_data)

            candidate_list.append([
                ticker,
                stock_score,
                buy_sell_signal
            ])

        return candidate_list
