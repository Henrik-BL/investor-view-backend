from hcnb_stock_data.models.stock_data import StockData


class StockScoreService:

    def __init__(self):
        self.points = 0
        self.max_points = 0
        self.score_list = []

    def score_stock(self, stock_data: StockData):
        self._reset_points()
        self._score_revenue_growth(stock_data)
        self._score_quarterly_revenue_cagr(stock_data)
        self._score_yearly_revenue_cagr(stock_data)
        self._score_earnings_growth(stock_data)
        self._score_quarterly_net_income_cagr(stock_data)
        self._score_yearly_net_income_cagr(stock_data)
        self._score_quarterly_free_cashflow_cagr(stock_data)
        self._score_yearly_free_cashflow_cagr(stock_data)
        self._score_current_ratio(stock_data)
        self._score_debt_to_equity(stock_data)
        self._score_last_quarter_margin(stock_data)
        self._score_margin_difference_yoy(stock_data)
        self._score_yearly_outstanding_shares_cagr(stock_data)
        self._score_yearly_diluted_outstanding_shares_cagr(stock_data)

        score_percentage = round((self.points / self.max_points) * 10 if self.max_points > 0 else 0, 2)

        return {
            "score": score_percentage,
            "points": self.points,
            "max_points": self.max_points,
            "score_list": self.score_list,
        }

    def _reset_points(self):
        self.points = 0
        self.max_points = 0
        self.score_list = []

    def _score_revenue_growth(self, stock_data: StockData):
        self.max_points += 3
        if stock_data.revenue_growth is None:
            self.score_list.append(["Revenue Growth", None, 0, 3])
            return

        if 10 <= stock_data.revenue_growth <= 20:
            self.points += 1
            self.score_list.append(["Revenue Growth",  stock_data.revenue_growth, 1, 3])
        elif 20 < stock_data.revenue_growth <= 30:
            self.points += 2
            self.score_list.append(["Revenue Growth", stock_data.revenue_growth, 2, 3])
        elif 30 < stock_data.revenue_growth:
            self.points += 3
            self.score_list.append(["Revenue Growth", stock_data.revenue_growth, 3, 3])
        else:
            self.score_list.append(["Revenue Growth", stock_data.revenue_growth, 0, 3])

    def _score_quarterly_revenue_cagr(self, stock_data: StockData):
        self.max_points += 3
        if stock_data.quarterly_revenue_cagr is None:
            self.score_list.append(["Quarterly Revenue CAGR", None, 0, 3])
            return

        if 1 <= stock_data.quarterly_revenue_cagr <= 4:
            self.points += 1
            self.score_list.append(["Quarterly Revenue CAGR",  stock_data.quarterly_revenue_cagr, 1, 3])
        elif 4 < stock_data.quarterly_revenue_cagr <= 10:
            self.points += 2
            self.score_list.append(["Quarterly Revenue CAGR", stock_data.quarterly_revenue_cagr, 2, 3])
        elif 10 < stock_data.quarterly_revenue_cagr:
            self.points += 3
            self.score_list.append(["Quarterly Revenue CAGR", stock_data.quarterly_revenue_cagr, 3, 3])
        else:
            self.score_list.append(["Quarterly Revenue CAGR", stock_data.quarterly_revenue_cagr, 0, 3])

    def _score_yearly_revenue_cagr(self, stock_data: StockData):
        self.max_points += 3
        if stock_data.yearly_revenue_cagr is None:
            self.score_list.append(["Yearly Revenue CAGR", None, 0, 3])
            return

        if 10 <= stock_data.yearly_revenue_cagr <= 15:
            self.points += 1
            self.score_list.append(["Yearly Revenue CAGR",  stock_data.yearly_revenue_cagr, 1, 3])
        elif 15 < stock_data.yearly_revenue_cagr <= 20:
            self.points += 2
            self.score_list.append(["Yearly Revenue CAGR", stock_data.yearly_revenue_cagr, 2, 3])
        elif 20 < stock_data.yearly_revenue_cagr:
            self.points += 3
            self.score_list.append(["Yearly Revenue CAGR", stock_data.yearly_revenue_cagr, 3, 3])
        else:
            self.score_list.append(["Yearly Revenue CAGR", stock_data.yearly_revenue_cagr, 0, 3])

    def _score_earnings_growth(self, stock_data: StockData):
        self.max_points += 3
        if stock_data.earnings_growth is None:
            self.score_list.append(["Earnings Growth", None, 0, 3])
            return
        if 10 <= stock_data.earnings_growth <= 20:
            self.points += 1
            self.score_list.append(["Earnings Growth",  stock_data.earnings_growth, 1, 3])
        elif 20 < stock_data.earnings_growth <= 30:
            self.points += 2
            self.score_list.append(["Earnings Growth", stock_data.earnings_growth, 2, 3])
        elif 30 < stock_data.earnings_growth:
            self.points += 3
            self.score_list.append(["Earnings Growth", stock_data.earnings_growth, 3, 3])
        else:
            self.score_list.append(["Earnings Growth", stock_data.earnings_growth, 0, 3])

    def _score_quarterly_net_income_cagr(self, stock_data: StockData):
        self.max_points += 3
        if stock_data.quarterly_net_income_cagr is None:
            self.score_list.append(["Quarterly Net Income CAGR", None, 0, 3])
            return
        if 1 <= stock_data.quarterly_net_income_cagr <= 4:
            self.points += 1
            self.score_list.append(["Quarterly Net Income CAGR",  stock_data.quarterly_net_income_cagr, 1, 3])
        elif 4 < stock_data.quarterly_net_income_cagr <= 10:
            self.points += 2
            self.score_list.append(["Quarterly Net Income CAGR", stock_data.quarterly_net_income_cagr, 2, 3])
        elif 10 < stock_data.quarterly_net_income_cagr:
            self.points += 3
            self.score_list.append(["Quarterly Net Income CAGR", stock_data.quarterly_net_income_cagr, 3, 3])
        else:
            self.score_list.append(["Quarterly Net Income CAGR", stock_data.quarterly_net_income_cagr, 0, 3])

    def _score_yearly_net_income_cagr(self, stock_data: StockData):
        self.max_points += 3
        if stock_data.yearly_net_income_cagr is None:
            self.score_list.append(["Yearly Net Income CAGR", None, 0, 3])
            return
        if 10 <= stock_data.yearly_net_income_cagr <= 15:
            self.points += 1
            self.score_list.append(["Yearly Net Income CAGR",  stock_data.yearly_net_income_cagr, 1, 3])
        elif 15 < stock_data.yearly_net_income_cagr <= 20:
            self.points += 2
            self.score_list.append(["Yearly Net Income CAGR", stock_data.yearly_net_income_cagr, 2, 3])
        elif 20 < stock_data.yearly_net_income_cagr:
            self.points += 3
            self.score_list.append(["Yearly Net Income CAGR", stock_data.yearly_net_income_cagr, 3, 3])
        else:
            self.score_list.append(["Yearly Net Income CAGR", stock_data.yearly_net_income_cagr, 0, 3])

    def _score_quarterly_free_cashflow_cagr(self, stock_data: StockData):
        self.max_points += 3
        if stock_data.quarterly_free_cashflow_cagr is None:
            self.score_list.append(["Quarterly Free Cash Flow CAGR", None, 0, 3])
            return
        if 1 <= stock_data.quarterly_free_cashflow_cagr <= 4:
            self.points += 1
            self.score_list.append(["Quarterly Free Cash Flow CAGR",  stock_data.quarterly_free_cashflow_cagr, 1, 3])
        elif 4 < stock_data.quarterly_free_cashflow_cagr <= 10:
            self.points += 2
            self.score_list.append(["Quarterly Free Cash Flow CAGR", stock_data.quarterly_free_cashflow_cagr, 2, 3])
        elif 10 < stock_data.quarterly_free_cashflow_cagr:
            self.points += 3
            self.score_list.append(["Quarterly Free Cash Flow CAGR", stock_data.quarterly_free_cashflow_cagr, 3, 3])
        else:
            self.score_list.append(["Quarterly Free Cash Flow CAGR", stock_data.quarterly_free_cashflow_cagr, 0, 3])

    def _score_yearly_free_cashflow_cagr(self, stock_data: StockData):
        self.max_points += 3
        if stock_data.yearly_free_cashflow_cagr is None:
            self.score_list.append(["Yearly Free Cash Flow CAGR", None, 0, 3])
            return
        if 10 <= stock_data.yearly_free_cashflow_cagr <= 15:
            self.points += 1
            self.score_list.append(["Yearly Free Cash Flow CAGR",  stock_data.yearly_free_cashflow_cagr, 1, 3])
        elif 15 < stock_data.yearly_free_cashflow_cagr <= 20:
            self.points += 2
            self.score_list.append(["Yearly Free Cash Flow CAGR", stock_data.yearly_free_cashflow_cagr, 2, 3])
        elif 20 < stock_data.yearly_free_cashflow_cagr:
            self.points += 3
            self.score_list.append(["Yearly Free Cash Flow CAGR", stock_data.yearly_free_cashflow_cagr, 3, 3])
        else:
            self.score_list.append(["Yearly Free Cash Flow CAGR", stock_data.yearly_free_cashflow_cagr, 0, 3])

    def _score_current_ratio(self, stock_data: StockData):
        self.max_points += 3
        if stock_data.current_ratio is None:
            self.score_list.append(["Current Ratio", None, 0, 3])
            return

        if 1.5 <= stock_data.current_ratio < 2.0:
            self.points += 1
            self.score_list.append(["Current Ratio", stock_data.current_ratio, 1, 3])
        elif 2.0 <= stock_data.current_ratio < 3.0:
            self.points += 2
            self.score_list.append(["Current Ratio", stock_data.current_ratio, 2, 3])
        elif 3.0 <= stock_data.current_ratio:
            self.points += 3
            self.score_list.append(["Current Ratio", stock_data.current_ratio, 3, 3])
        else:
            self.score_list.append(["Current Ratio", stock_data.current_ratio, 0, 3])

    def _score_debt_to_equity(self, stock_data: StockData):
        self.max_points += 3
        if stock_data.debt_to_equity is None:
            self.score_list.append(["Debt to Equity", None, 0, 3])
            return

        if stock_data.debt_to_equity < 10:
            self.points += 3
            self.score_list.append(["Debt to Equity", stock_data.debt_to_equity, 3, 3])
        elif stock_data.debt_to_equity < 50:
            self.points += 2
            self.score_list.append(["Debt to Equity", stock_data.debt_to_equity, 2, 3])
        elif 50 <= stock_data.debt_to_equity < 100:
            self.points += 1
            self.score_list.append(["Debt to Equity", stock_data.debt_to_equity, 1, 3])
        else:
            self.score_list.append(["Debt to Equity", stock_data.debt_to_equity, 0, 3])

    def _score_last_quarter_margin(self, stock_data: StockData):
        self.max_points += 3
        if stock_data.last_quarter_margin is None:
            self.score_list.append(["Last Quarter Margin", None, 0, 3])
            return
        if 0 <= stock_data.last_quarter_margin < 10:
            self.points += 1
            self.score_list.append(["Last Quarter Margin", stock_data.last_quarter_margin, 1, 3])
        elif 10 <= stock_data.last_quarter_margin < 20:
            self.points += 2
            self.score_list.append(["Last Quarter Margin", stock_data.last_quarter_margin, 2, 3])
        elif 20 <= stock_data.last_quarter_margin:
            self.points += 3
            self.score_list.append(["Last Quarter Margin", stock_data.last_quarter_margin, 3, 3])
        else:
            self.score_list.append(["Last Quarter Margin", stock_data.last_quarter_margin, 0, 3])

    def _score_margin_difference_yoy(self, stock_data: StockData):
        self.max_points += 2
        if stock_data.margin_difference_yoy is None:
            self.score_list.append(["Margin Difference YoY", None, 0, 2])
            return
        if 0 <= stock_data.margin_difference_yoy:
            self.points += 2
            self.score_list.append(["Margin Difference YoY", stock_data.margin_difference_yoy, 2, 2])
        else:
            self.score_list.append(["Margin Difference YoY", stock_data.margin_difference_yoy, 0, 2])

    def _score_yearly_outstanding_shares_cagr(self, stock_data: StockData):
        self.max_points += 1

        if stock_data.yearly_outstanding_shares_cagr is None:
            self.score_list.append(["Yearly Outstanding Shares CAGR", None, 0, 1])
            return

        if stock_data.yearly_outstanding_shares_cagr <= 0:
            self.points += 1
            self.score_list.append([ "Yearly Outstanding Shares CAGR", stock_data.yearly_outstanding_shares_cagr, 1, 1])
        else:
            self.score_list.append(["Yearly Outstanding Shares CAGR", stock_data.yearly_outstanding_shares_cagr, 0, 1])

    def _score_yearly_diluted_outstanding_shares_cagr(self, stock_data: StockData):
        self.max_points += 1

        if stock_data.yearly_diluted_outstanding_shares_cagr is None:
            self.score_list.append(["Yearly Diluted Outstanding Shares CAGR", None, 0, 1])
            return

        if stock_data.yearly_diluted_outstanding_shares_cagr <= 0:
            self.points += 1
            self.score_list.append(["Yearly Diluted Outstanding Shares CAGR", stock_data.yearly_diluted_outstanding_shares_cagr, 1, 1])
        else:
            self.score_list.append(["Yearly Diluted Outstanding Shares CAGR", stock_data.yearly_diluted_outstanding_shares_cagr, 0, 1])

