from iqoptionapi.api import IQOptionAPI as IQ_Option
from utils.logger import logger
from core.config import Config
import time

class IQConnector:
    def __init__(self):
        self.api = None
        self.is_connected = False

    def connect(self):
        try:
            logger.info(f"Attempting to connect to IQ Option ({Config.IQ_MODE} mode)...")
            self.api = IQ_Option(Config.IQ_EMAIL, Config.IQ_PASSWORD)
            
            check, reason = self.api.connect()
            if not check:
                logger.error(f"Connection failed: {reason}")
                return False
            
            self.api.change_balance(Config.IQ_MODE)
            self.is_connected = True
            logger.info("Successfully connected to IQ Option.")
            return True
        except Exception as e:
            logger.error(f"Error during connection: {e}")
            return False

    def reconnect(self):
        logger.warning("Reconnecting to IQ Option...")
        return self.connect()

    def get_balance(self):
        if not self.is_connected:
            return 0
        return self.api.get_balance()

    def get_candles(self, asset, timeframe, count):
        if not self.is_connected:
            return []
        return self.api.get_candles(asset, timeframe, count, time.time())
