import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # IQ Option Credentials
    IQ_EMAIL = os.getenv("IQ_EMAIL")
    IQ_PASSWORD = os.getenv("IQ_PASSWORD")
    IQ_MODE = os.getenv("IQ_MODE", "PRACTICE")  # PRACTICE or REAL
    
    # Telegram Config
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    
    # Trading Settings
    TRADE_AMOUNT = float(os.getenv("TRADE_AMOUNT", 1.0))
    STOP_LOSS = float(os.getenv("STOP_LOSS", 10.0))
    TAKE_PROFIT = float(os.getenv("TAKE_PROFIT", 20.0))
    MAX_TRADES = int(os.getenv("MAX_TRADES", 3))
    
    # Strategy Settings
    TIMEFRAME = int(os.getenv("TIMEFRAME", 60))  # in seconds
    ASSETS = os.getenv("ASSETS", "EURUSD,GBPUSD,USDJPY").split(",")
    
    @classmethod
    def validate(cls):
        missing = []
        if not cls.IQ_EMAIL: missing.append("IQ_EMAIL")
        if not cls.IQ_PASSWORD: missing.append("IQ_PASSWORD")
        if not cls.TELEGRAM_TOKEN: missing.append("TELEGRAM_TOKEN")
        return missing
