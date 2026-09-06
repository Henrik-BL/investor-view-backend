from hcnb_stock_data.hcnb_stock_data import HcnbStockData

from future_valuation_service import FutureValuationService

hcnb_stock_data = HcnbStockData()

stock_data_2 = hcnb_stock_data.get_stock_data("PLTR")

future_valuation = FutureValuationService()

print(future_valuation.get_valuation(stock_data_2))