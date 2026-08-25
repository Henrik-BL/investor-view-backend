import json

from hcnb_stock_data.hcnb_stock_data import HcnbStockData

from buy_sell_signals_service import BuySellSignalsService
from stock_scorer import CompanyScorer

hcnb_stock_data = HcnbStockData()

# main_portfolio_service = MainPortfolioService(hcnb_stock_data)

buy_sell_signals_service = BuySellSignalsService(hcnb_stock_data)


stock_data = hcnb_stock_data.get_stock_data("PLTR")

# print(json.dumps(stock_data.__dict__, indent=4))


company_scorer = CompanyScorer(stock_data)

rev = company_scorer.score()

print(rev)