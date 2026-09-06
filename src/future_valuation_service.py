from hcnb_stock_data.models.stock_data import StockData


class FutureValuationService:
    FUTURE_4_QUARTERS = 4
    FUTURE_8_QUARTERS = 8
    QUARTERS_PER_YEAR = 4

    def get_valuation(self, stock_data: StockData) -> dict:
        return {
            "future_4_quarters": self._calculate_future_pe(
                stock_data=stock_data,
                quarters=self.FUTURE_4_QUARTERS,
            ),
            "future_8_quarters": self._calculate_future_pe(
                stock_data=stock_data,
                quarters=self.FUTURE_8_QUARTERS,
            ),
        }

    @staticmethod
    def calculate_future_value(value: float, growth_rate: float, periods: int) -> float:
        if periods < 0:
            raise ValueError("periods cannot be negative")

        if growth_rate <= -100:
            raise ValueError("growth_rate must be greater than -100%")

        return value * (1 + growth_rate / 100) ** periods

    def _calculate_future_pe(self, stock_data: StockData, quarters: int) -> float:
        if (
                stock_data.last_quarter_revenue is None
                or stock_data.quarterly_revenue_cagr is None
                or stock_data.last_quarter_margin is None
                or stock_data.market_cap is None
        ):
            return float("inf")

        future_quarterly_revenue = self.calculate_future_value(
            value=stock_data.last_quarter_revenue,
            growth_rate=stock_data.quarterly_revenue_cagr,
            periods=quarters,
        )

        future_annual_revenue = (
                future_quarterly_revenue * self.QUARTERS_PER_YEAR
        )

        future_annual_net_income = (
                future_annual_revenue
                * stock_data.last_quarter_margin
                / 100
        )

        if future_annual_net_income <= 0:
            return float("inf")

        return round(stock_data.market_cap / future_annual_net_income, 2)
