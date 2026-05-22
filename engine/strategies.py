import pandas as pd
import numpy as np
from utils.logger import logger

class StrategyEngine:
    @staticmethod
    def rsi(series, period=14):
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    @staticmethod
    def sma(series, period):
        return series.rolling(window=period).mean()

    def analyze(self, candles):
        """
        Analyze candles and return 'call', 'put', or 'wait'
        """
        if not candles or len(candles) < 20:
            return 'wait'

        df = pd.DataFrame(candles)
        df['close'] = df['close'].astype(float)
        
        # Simple RSI + SMA Strategy
        df['rsi'] = self.rsi(df['close'])
        df['sma_20'] = self.sma(df['close'], 20)
        
        last_rsi = df['rsi'].iloc[-1]
        last_close = df['close'].iloc[-1]
        last_sma = df['sma_20'].iloc[-1]

        if last_rsi < 30 and last_close < last_sma:
            return 'call'
        elif last_rsi > 70 and last_close > last_sma:
            return 'put'
        
        return 'wait'
