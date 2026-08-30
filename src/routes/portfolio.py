from flask import Blueprint, jsonify
from pathlib import Path

from portfolio_candidates_service import PortfolioCandidatesService
from ..extensions import hcnb_stock_data_app
from ..main_portfolio_service import MainPortfolioService

portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/api/portfolio')

PORTFOLIO_FILE_PATH = Path(__file__).resolve().parents[1] / 'portfolio_data' / 'main_portfolio.json'

@portfolio_bp.route('/overview', methods=['GET'])
def portfolio_overview():
    main_portfolio_service = MainPortfolioService(hcnb_stock_data_app)
    portfolio_overview_json = main_portfolio_service.get_portfolio_overview()
    return jsonify(portfolio_overview_json), 200

@portfolio_bp.route('/candidates', methods=['GET'])
def portfolio_candidates():
    portfolio_candidates_service = PortfolioCandidatesService(hcnb_stock_data_app)
    portfolio_candidates_list = portfolio_candidates_service.get_main_portfolio_candidates()
    return jsonify(portfolio_candidates_list), 200
