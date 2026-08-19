import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import logging

from src.routes.dividend_portfolio import dividend_portfolio_bp
from src.routes.portfolio import portfolio_bp
from src.routes.screener import screener_bp
# from src.background_jobs import register_background_jobs

cors_origins = os.environ.get("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:30080,http://investor-view-frontend:80,http://investor-view-frontend").split(",")
serve_frontend = os.environ.get("SERVE_FRONTEND", "false").lower() in ["1", "true", "yes"]
static_folder = None
if serve_frontend:
    # when building frontend, adjust this path if needed
    static_folder = os.path.join(os.path.dirname(__file__), "..", "frontend", "build")

app = Flask(__name__, static_folder=static_folder, static_url_path="")

# Configure logging so module loggers (like src.background_jobs) print to the terminal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
# Ensure the Flask logger is not quieter than our configuration
logging.getLogger('werkzeug').setLevel(logging.INFO)

CORS(app, resources={r"/api/*": {"origins": cors_origins}})

app.register_blueprint(screener_bp)
app.register_blueprint(portfolio_bp)
app.register_blueprint(dividend_portfolio_bp)

# Start background jobs: run once immediately at startup and then every hour
# try:
#     register_background_jobs()
# except Exception:
#     # If scheduling fails (missing dependency, etc.) continue running the app
#     # but log the failure when possible.
#     import logging
#
#     logging.getLogger(__name__).exception("Failed to start background jobs")

if serve_frontend:
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, "index.html")

@app.route("/api/health")
def health_check():
    return jsonify(status="ok"), 200

if __name__ == "__main__":
    # development server
    app.run(host="0.0.0.0", port=5000, debug=True)
