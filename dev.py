import json

from hcnb_stock_data.hcnb_stock_data import HcnbStockData

from src.main_portfolio_service import MainPortfolioService

hcnb_stock_data = HcnbStockData()

main_portfolio_service = MainPortfolioService(hcnb_stock_data)


result = main_portfolio_service.get_portfolio_overview()

print(json.dumps(result, indent=4))
