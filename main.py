import time
import threading
from core.config import Config
from core.connector import IQConnector
from engine.trading_engine import TradingEngine
from engine.strategies import StrategyEngine
from tg_bot.bot import TelegramManager
from utils.logger import logger

def trading_loop(connector, engine, strategy):
    logger.info("Starting Trading Loop...")
    while True:
        try:
            for asset in Config.ASSETS:
                candles = connector.get_candles(asset, Config.TIMEFRAME, 50)
                if candles:
                    signal = strategy.analyze(candles)
                    
                    if signal != 'wait':
                        logger.info(f"Signal for {asset}: {signal}")
                        engine.execute_trade(asset, signal, Config.TRADE_AMOUNT, 1)
                
            time.sleep(10)  # Wait before next scan
        except Exception as e:
            logger.error(f"Error in trading loop: {e}")
            time.sleep(5)

def main():
    logger.info("Initializing IQ Option AI Trading Bot...")
    
    # Validate Config
    missing = Config.validate()
    if missing:
        logger.warning(f"Missing environment variables: {', '.join(missing)}")
        logger.info("Bot will run in limited mode for verification.")
    
    connector = IQConnector()
    # Note: In real production, we'd wait for connection. 
    # For 'hood run' verification, we handle the failure gracefully.
    connector.connect()
    
    engine = TradingEngine(connector)
    strategy = StrategyEngine()
    
    # Start Trading Loop in a separate thread
    trade_thread = threading.Thread(target=trading_loop, args=(connector, engine, strategy), daemon=True)
    trade_thread.start()
    
    # Start Telegram Bot (Blocking)
    if Config.TELEGRAM_TOKEN:
        try:
            tg_manager = TelegramManager(Config.TELEGRAM_TOKEN)
            tg_manager.run()
        except Exception as e:
            logger.error(f"Telegram Bot failed: {e}")
            while True: time.sleep(1)
    else:
        logger.warning("Telegram Token not found. Bot will run without Telegram integration.")
        while True:
            time.sleep(1)

if __name__ == "__main__":
    main()
