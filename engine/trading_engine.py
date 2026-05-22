from utils.logger import logger
from core.config import Config
import time

class TradingEngine:
    def __init__(self, connector):
        self.connector = connector
        self.active_trades = {}

    def execute_trade(self, asset, action, amount, duration):
        """
        action: 'call' or 'put'
        duration: in minutes
        """
        if not self.connector.is_connected:
            logger.error("Cannot execute trade: Not connected to API.")
            return None

        logger.info(f"Executing {action.upper()} trade on {asset} for ${amount}")
        
        check, id = self.connector.api.buy(amount, asset, action, duration)
        
        if check:
            logger.info(f"Trade successful! ID: {id}")
            return id
        else:
            logger.error(f"Trade failed: {id}")
            return None

    def check_win(self, trade_id):
        if not self.connector.is_connected:
            return None
        return self.connector.api.check_win_v3(trade_id)
