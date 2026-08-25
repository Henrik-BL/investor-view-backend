from hcnb_stock_data.models.stock_data import StockData


class CompanyScorer:

    def __init__(self, stock_data: StockData):
        self.stock_data = stock_data

    @staticmethod
    def clamp(value, minimum=0, maximum=10):
        return max(minimum, min(maximum, value))

    @staticmethod
    def score_higher(value, thresholds):
        score = 0

        for threshold, threshold_score in thresholds:
            if value >= threshold:
                score = threshold_score
            else:
                break

        return score

    @staticmethod
    def score_lower(value, thresholds):
        for maximum, score in thresholds:
            if value <= maximum:
                return score

        return 0

    # --------------------------------------------------
    # REVENUE
    # --------------------------------------------------

    def revenue_score(self):
        revenue_growth = self.stock_data.revenue_growth or 0
        yearly_cagr = self.stock_data.yearly_revenue_cagr or 0
        quarterly_cagr = self.stock_data.quarterly_revenue_cagr or 0

        growth_score = self.score_higher(
            revenue_growth,
            [
                (0, 0),
                (5, 2),
                (10, 4),
                (20, 6),
                (30, 7),
                (50, 8),
                (75, 9),
                (100, 10),
            ],
        )

        yearly_score = self.score_higher(
            yearly_cagr,
            [
                (0, 0),
                (5, 2),
                (10, 4),
                (15, 6),
                (20, 7),
                (30, 8),
                (40, 9),
                (50, 10),
            ],
        )

        quarterly_score = self.score_higher(
            quarterly_cagr,
            [
                (0, 0),
                (5, 2),
                (10, 4),
                (15, 6),
                (20, 7),
                (30, 8),
                (40, 9),
                (50, 10),
            ],
        )

        score = (
            growth_score * 0.40
            + yearly_score * 0.30
            + quarterly_score * 0.20
            + 7.0 * 0.10
        )

        return self.clamp(score)

    # --------------------------------------------------
    # PROFITABILITY
    # --------------------------------------------------

    def profitability_score(self):

        reports = getattr(self.stock_data, "quarterly_reports", [])

        if not reports:
            return 0

        latest = reports[-1]

        revenue = latest.get("revenue", 0)
        net_margin = latest.get("net_margin", 0) or 0
        free_cashflow = latest.get("free_cashflow", 0) or 0

        fcf_margin = (
            free_cashflow / revenue * 100
            if revenue
            else 0
        )

        margin_score = self.score_higher(
            net_margin,
            [
                (0, 0),
                (5, 2),
                (10, 4),
                (15, 5),
                (20, 6),
                (30, 7),
                (40, 8),
                (50, 9),
                (60, 10),
            ],
        )

        fcf_score = self.score_higher(
            fcf_margin,
            [
                (0, 0),
                (5, 2),
                (10, 4),
                (15, 5),
                (20, 6),
                (30, 7),
                (40, 8),
                (50, 9),
                (60, 10),
            ],
        )

        earnings_growth = getattr(self.stock_data, "earnings_growth", 0) or 0

        earnings_score = self.score_higher(
            earnings_growth,
            [
                (-50, 0),
                (0, 3),
                (10, 5),
                (20, 6),
                (50, 7),
                (100, 8),
                (200, 9),
                (300, 10),
            ],
        )

        margin_expansion = getattr(self.stock_data, "margin_difference_yoy", 0) or 0

        expansion_score = self.score_higher(
            margin_expansion,
            [
                (-20, 0),
                (-10, 2),
                (0, 5),
                (5, 6),
                (10, 7),
                (15, 8),
                (20, 9),
                (30, 10),
            ],
        )

        score = (
            margin_score * 0.30
            + fcf_score * 0.20
            + earnings_score * 0.15
            + expansion_score * 0.15
            + 8.0 * 0.20
        )

        return self.clamp(score)

    # --------------------------------------------------
    # FINANCIAL STABILITY
    # --------------------------------------------------

    def financial_stability_score(self):

        current_ratio = getattr(self.stock_data, "current_ratio", 0) or 0

        debt_to_equity = getattr(self.stock_data, "debt_to_equity", 0) or 0

        quarterly_debt_cagr = getattr(self.stock_data, "quarterly_total_debt_cagr", 0) or 0

        yearly_debt_cagr = getattr(self.stock_data, "yearly_total_debt_cagr", 0) or 0

        dilution = getattr(self.stock_data, "yearly_diluted_outstanding_shares_cagr", 0) or 0

        fcf_growth = getattr(self.stock_data, "yearly_free_cashflow_cagr", 0) or 0

        liquidity_score = self.score_higher(
            current_ratio,
            [
                (0, 0),
                (0.75, 2),
                (1, 4),
                (1.5, 6),
                (2, 7),
                (3, 8),
                (5, 9),
                (7, 10),
            ],
        )

        debt_score = self.score_lower(
            debt_to_equity,
            [
                (0.25, 10),
                (0.5, 9),
                (1, 8),
                (2, 7),
                (3, 5),
                (5, 3),
                (10, 1),
            ],
        )

        debt_trend = (
            quarterly_debt_cagr
            + yearly_debt_cagr
        ) / 2

        debt_growth_score = self.score_lower(
            debt_trend,
            [
                (-20, 10),
                (-10, 9),
                (0, 8),
                (5, 6),
                (10, 4),
                (20, 2),
                (50, 0),
            ],
        )

        dilution_score = self.score_lower(
            dilution,
            [
                (0, 10),
                (1, 9),
                (2, 8),
                (3, 7),
                (5, 5),
                (8, 3),
                (12, 1),
            ],
        )

        fcf_growth_score = self.score_higher(
            fcf_growth,
            [
                (-20, 0),
                (0, 3),
                (10, 5),
                (25, 6),
                (50, 7),
                (75, 8),
                (100, 9),
                (150, 10),
            ],
        )

        score = (
            liquidity_score * 0.20
            + debt_score * 0.20
            + fcf_growth_score * 0.20
            + debt_growth_score * 0.15
            + dilution_score * 0.10
            + 8.0 * 0.15
        )

        return self.clamp(score)

    # --------------------------------------------------
    # VALUATION
    # --------------------------------------------------

    def valuation_score(self):

        pe = getattr(self.stock_data, "pe", None)
        forward_pe = getattr(self.stock_data, "forward_pe", None)
        peg = getattr(self.stock_data, "peg", None)
        ps = getattr(self.stock_data, "ps", None)

        if pe is None:
            return 0

        pe_score = self.score_lower(
            pe,
            [
                (10, 10),
                (15, 9),
                (20, 8),
                (25, 7),
                (35, 6),
                (50, 5),
                (75, 3),
                (100, 2),
                (150, 1),
            ],
        )

        forward_score = (
            self.score_lower(
                forward_pe,
                [
                    (10, 10),
                    (15, 9),
                    (20, 8),
                    (25, 7),
                    (35, 6),
                    (50, 5),
                    (75, 3),
                    (100, 2),
                    (150, 1),
                ],
            )
            if forward_pe is not None
            else 5
        )

        peg_score = (
            self.score_lower(
                peg,
                [
                    (0.5, 10),
                    (1, 9),
                    (1.5, 8),
                    (2, 6),
                    (2.5, 5),
                    (3, 3),
                    (4, 1),
                ],
            )
            if peg is not None
            else 5
        )

        ps_score = (
            self.score_lower(
                ps,
                [
                    (2, 10),
                    (4, 9),
                    (6, 8),
                    (10, 7),
                    (15, 6),
                    (25, 4),
                    (40, 2),
                    (60, 1),
                ],
            )
            if ps is not None
            else 5
        )

        score = (
            pe_score * 0.30
            + forward_score * 0.30
            + peg_score * 0.25
            + ps_score * 0.15
        )

        return self.clamp(score)

    # --------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------

    def score(self):

        revenue = self.revenue_score()
        profitability = self.profitability_score()
        stability = self.financial_stability_score()
        valuation = self.valuation_score()

        business_quality = (
            revenue * 0.35
            + profitability * 0.40
            + stability * 0.25
        )

        investment_score = (
            business_quality * 0.75
            + valuation * 0.25
        )

        return {
            "ticker": getattr(self.stock_data, "ticker", None),
            "name": getattr(self.stock_data, "name", None),
            "scores": {
                "revenue": round(revenue, 2),
                "profitability": round(profitability, 2),
                "financial_stability": round(stability, 2),
                "valuation": round(valuation, 2),
                "business_quality": round(business_quality, 2),
                "investment_score": round(investment_score, 2),
            },
        }