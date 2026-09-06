from hcnb_stock_data.hcnb_stock_data import HcnbStockData
from hcnb_stock_data.models.stock_data import StockData


class BuySellSignalsService:

    def __init__(self, hcnb_stock_data: HcnbStockData):
        self.fear_greed_data = hcnb_stock_data.get_fear_greed_index()
        self.buy_points = 0
        self.sell_points = 0
        self.buy_points_calculated = []
        self.sell_points_calculated = []
        self.neutral_or_missing_data = []
        self.points_limit = 5

    def get_buy_sell_signal(self, stock_data: StockData):
        self.buy_points = 0
        self.sell_points = 0

        self.buy_points_calculated = []
        self.sell_points_calculated = []
        self.neutral_or_missing_data = []

        self._set_fear_greed_points()
        self._set_rsi_14_points(stock_data)
        self._set_ma_50_points(stock_data)
        self._set_ma_225_points(stock_data)
        self._set_price_change(stock_data)

        return {
            "buy_points": self.buy_points,
            "sell_points": self.sell_points,
            "buy_points_calculated": self.buy_points_calculated,
            "sell_points_calculated": self.sell_points_calculated,
            "neutral_or_missing_data": self.neutral_or_missing_data,
            "points_limit": self.points_limit
        }

    def _set_fear_greed_points(self):
        if self.fear_greed_data is None:
            self.neutral_or_missing_data.append(["Fear & Greed Index", "Missing", 1, self.fear_greed_data])
            return

        if self.fear_greed_data < 25:
            self.buy_points += 2
            self.buy_points_calculated.append(["Fear & Greed Index", "Buy", 2, self.fear_greed_data])
        elif 25 <= self.fear_greed_data <= 45:
            self.buy_points += 1
            self.buy_points_calculated.append(["Fear & Greed Index", "Buy", 1, self.fear_greed_data])
        elif 55 <= self.fear_greed_data <= 75:
            self.sell_points += 1
            self.sell_points_calculated.append(["Fear & Greed Index", "Sell", 1, self.fear_greed_data])
        elif 75 <= self.fear_greed_data:
            self.sell_points += 2
            self.sell_points_calculated.append(["Fear & Greed Index", "Sell", 2, self.fear_greed_data])
        else:
            self.neutral_or_missing_data.append(["Fear & Greed Index", "Neutral", 1, self.fear_greed_data])

    def _set_rsi_14_points(self, stock_data: StockData):
        if stock_data.rsi_14 < 30:
            val = 2 if stock_data.rsi_14 < 20 else 1
            self.buy_points += val
            self.buy_points_calculated.append(["RSI 14", "Buy", val, stock_data.rsi_14])
        elif stock_data.rsi_14 > 70:
            val = 2 if stock_data.rsi_14 > 80 else 1
            self.sell_points += val
            self.sell_points_calculated.append(["RSI 14", "Sell", val, stock_data.rsi_14])
        else:
            self.neutral_or_missing_data.append(["RSI 14", "Neutral", 1, stock_data.rsi_14])

    def _set_ma_50_points(self, stock_data: StockData):
        diff = stock_data.sma_50_diff
        if diff < -10:
            self.buy_points += 1
            self.buy_points_calculated.append(["SMA 50 diff", "Buy", 1, diff])
        elif diff >= 10:
            self.sell_points += 1
            self.sell_points_calculated.append(["SMA 50 diff", "Sell", 1, diff])
        else:
            self.neutral_or_missing_data.append(["SMA 50 diff", "Neutral", 1, diff])

    def _set_ma_225_points(self, stock_data: StockData):
        diff = stock_data.sma_225_diff
        if -40 <= diff <= -10:
            self.buy_points += 1
            self.buy_points_calculated.append(["SMA 225 diff", "Buy", 1, diff])
        elif diff < -40:
            self.buy_points += 2
            self.buy_points_calculated.append(["SMA 225 diff", "Buy", 2, diff])
        elif 50 <= diff < 80:
            self.sell_points += 1
            self.sell_points_calculated.append(["SMA 225 diff", "Sell", 1, diff])
        elif diff >= 80:
            self.sell_points += 2
            self.sell_points_calculated.append(["SMA 225 diff", "Sell", 2, diff])
        else:
            self.neutral_or_missing_data.append(["SMA 225 diff", "Neutral", 1, diff])

    def _set_price_change(self, stock_data: StockData):
        diff = stock_data.change
        if -5 <= diff <= -2:
            self.buy_points += 1
            self.buy_points_calculated.append(["Change", "Buy", 1, diff])
        elif diff < -5:
            self.buy_points += 2
            self.buy_points_calculated.append(["Change", "Buy", 2, diff])
        elif 2 <= diff < 5:
            self.sell_points += 1
            self.sell_points_calculated.append(["Change", "Sell", 1, diff])
        elif diff >= 5:
            self.sell_points += 2
            self.sell_points_calculated.append(["Change", "Sell", 2, diff])
        else:
            self.neutral_or_missing_data.append(["Change", "Neutral", 1, diff])
