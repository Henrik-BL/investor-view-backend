from hcnb_stock_data.hcnb_stock_data import HcnbStockData

hcnb_stock_data = HcnbStockData()

tickers = hcnb_stock_data.get_all_tickers()

with open("setup_tickers.py", "w", encoding="utf-8") as f:
    f.write("from hcnb_stock_data.hcnb_stock_data import HcnbStockData\n\n")
    f.write("tickers = [\n")
    for item in tickers:
        f.write(f"    {item!r},\n")
    f.write("]\n")

    f.write("\n")

    f.write("hcnb_stock_data = HcnbStockData()\n")
    f.write("\n")
    f.write("for ticker in tickers:\n")
    f.write('    print("Update data for ticker:", ticker)\n')
    f.write("    hcnb_stock_data.get_stock_data(ticker, True)\n")