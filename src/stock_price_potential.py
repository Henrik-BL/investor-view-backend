from hcnb_stock_data.calculator import Calculator
from hcnb_stock_data.models.stock_data import StockData


class StockPricePotential:

    def __init__(self, stock_data: StockData):
        self.price = stock_data.price
        self.percentage_list = []

        # All-time high potential
        self.all_time_high = stock_data.all_time_high
        self.all_time_high_potential = Calculator.calculate_change_percentage(self.price, self.all_time_high)
        self.percentage_list.append(self.all_time_high_potential)

        # 52-week high potential
        self.fifty_two_week_high = stock_data.fifty_two_week_high
        self.fifty_two_week_high_potential = Calculator.calculate_change_percentage(self.price, self.fifty_two_week_high)
        self.percentage_list.append(self.fifty_two_week_high_potential)

        # Analyst target prices
        self.target_high_price = stock_data.target_high_price
        self.target_high_potential = Calculator.calculate_change_percentage(self.price, self.target_high_price) if self.target_high_price else None
        if self.target_high_potential is not None:
            self.percentage_list.append(self.target_high_potential)

        self.target_low_price = stock_data.target_low_price
        self.target_low_potential = Calculator.calculate_change_percentage(self.price, self.target_low_price) if self.target_low_price else None
        if self.target_low_potential is not None:
            self.percentage_list.append(self.target_low_potential)

        self.target_mean_price = stock_data.target_mean_price
        self.target_mean_potential = Calculator.calculate_change_percentage(self.price, self.target_mean_price) if self.target_mean_price else None
        if self.target_mean_potential is not None:
            self.percentage_list.append(self.target_mean_potential)

        self.target_median_price = stock_data.target_median_price
        self.target_median_potential = Calculator.calculate_change_percentage(self.price, self.target_median_price) if self.target_median_price else None
        if self.target_median_potential is not None:
            self.percentage_list.append(self.target_median_potential)

        # Calculate averages
        self.average_potential = Calculator.calculate_average(self.percentage_list)
        positive_list = [p for p in self.percentage_list if p != self.target_low_potential]
        self.positive_average_potential = Calculator.calculate_average(positive_list)


    def get_result(self):
        """Return a dictionary with all price potentials."""
        return {
            "price": self.price,
            "all_time_high_potential": {
                "percentage": self.all_time_high_potential,
                "all_time_high": self.all_time_high
            },
            "fifty_two_week_high_potential": {
                "percentage": self.fifty_two_week_high_potential,
                "fifty_two_week_high": self.fifty_two_week_high
            },
            "target_high_potential": {
                "percentage": self.target_high_potential,
                "target_high": self.target_high_price
            },
            "target_mean_potential": {
                "percentage": self.target_mean_potential,
                "target_mean": self.target_mean_price
            },
            "target_median_potential": {
                "percentage": self.target_median_potential,
                "target_median": self.target_median_price
            },
            "target_low_potential": {
                "percentage": self.target_low_potential,
                "target_low": self.target_low_price
            },
            "average_potential": self.average_potential,
            "positive_average_potential": self.positive_average_potential,
            "percentage_list": self.percentage_list
        }
