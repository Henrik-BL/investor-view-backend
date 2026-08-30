from hcnb_stock_data.hcnb_stock_data import HcnbStockData
from stock_score_service import StockScoreService



hcnb_stock_data = HcnbStockData()
stock_score_service = StockScoreService()

tickers = hcnb_stock_data.get_all_tickers()

result_list = []

for ticker in tickers:
    stock_data = hcnb_stock_data.get_stock_data(ticker, False)
    result = stock_score_service.score_stock(stock_data)
    result_list.append([ticker, result['score'],  result])

result_list.sort(key=lambda x: x[1], reverse=True)


print("Ticker\tScore\tDetails")

for result in result_list:


    ticker, score, details = result
    print(f"{ticker}\t{score}")