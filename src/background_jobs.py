import datetime
import logging
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from hcnb_stock_data.hcnb_stock_data import HcnbStockData


_scheduler = None
_logger = logging.getLogger(__name__)


def hourly_update_all_tickers():
    """Update all tickers in the hcnb_stock_data store.
    This function is safe to run repeatedly; it will attempt to update each
    ticker and log errors rather than raise.
    """

    hcnb_stock_data = HcnbStockData()

    print("Background job: hourly_update_all_tickers")

    tickers = hcnb_stock_data.get_all_tickers() or []

    print(tickers)

    # _logger.info("Background job: hourly_update_all_tickers")

    # try:
    #     # Give external library a hint to allow updates (similar to the manual endpoint)
    #     try:
    #         hcnb_stock_data.update_limit_hours = 1
    #     except Exception:
    #         # not all versions may expose this attribute; ignore if absent
    #         pass
    #
    #     tickers = hcnb_stock_data.get_all_tickers() or []
    #     total = len(tickers)
    #     for index, ticker in enumerate(tickers, start=1):
    #         try:
    #             hcnb_stock_data.get_stock_data(ticker, True)
    #         except Exception as exc:
    #             print("Failed to update ticker %s (%d/%d): %s", ticker, index, total, exc)
    #            #  _logger.exception("Failed to update ticker %s (%d/%d): %s", ticker, index, total, exc)
    #
    #     _logger.info("Background job: completed update of %d tickers", total)
    # except Exception:
    #     print("Unexpected error in background hourly_update_all_tickers")
        # _logger.exception("Unexpected error in background hourly_update_all_tickers")


# hourly_update_all_tickers()

def register_background_jobs():
    """Create and start a BackgroundScheduler that runs the hourly job.

    The job is scheduled to run immediately at startup and then every hour.
    Calling this function multiple times in the same process is safe.
    """
    global _scheduler
    if _scheduler is not None:
        _logger.debug("Background scheduler already registered")
        return _scheduler

    _scheduler = BackgroundScheduler()
    # run immediately and then every hour
    _scheduler.add_job(
        hourly_update_all_tickers,
        trigger="interval",
        hours=1,
        next_run_time=datetime.datetime.now(),
        id="hourly_update_all_tickers",
        replace_existing=True,
    )

    _scheduler.start()
    atexit.register(lambda: _scheduler.shutdown(wait=False))
    _logger.info("Background scheduler started (hourly updates)")
    return _scheduler

