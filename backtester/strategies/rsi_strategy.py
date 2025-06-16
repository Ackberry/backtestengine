import pandas as pd
import numpy as np
from typing import Dict, Any
from .base_strategy import BaseStrategy

class RSIStrategy(BaseStrategy):
    def __init__(self, parameters: Dict[str, Any]):
        """
        Initialize the RSI strategy.
        
        Args:
            parameters (Dict[str, Any]): Dictionary containing:
                - period (int): RSI calculation period
                - overbought (float): Overbought threshold (default: 70)
                - oversold (float): Oversold threshold (default: 30)
        """
        super().__init__(parameters)
        self.period = parameters.get('period', 14)
        self.overbought = parameters.get('overbought', 70)
        self.oversold = parameters.get('oversold', 30)
        
    def validate_parameters(self) -> bool:
        """
        Validate the strategy parameters.
        
        Returns:
            bool: True if parameters are valid, False otherwise
        """
        if not isinstance(self.period, int) or self.period <= 0:
            return False
        if not isinstance(self.overbought, (int, float)) or not isinstance(self.oversold, (int, float)):
            return False
        if self.overbought <= self.oversold:
            return False
        if self.overbought <= 50 or self.oversold >= 50:
            return False
        return True
        
    def calculate_rsi(self, data: pd.DataFrame) -> pd.Series:
        """
        Calculate the Relative Strength Index (RSI).
        
        Args:
            data (pd.DataFrame): DataFrame with OHLCV data
            
        Returns:
            pd.Series: RSI values
        """
        # Calculate price changes
        delta = data['Close'].diff()
        
        # Separate gains and losses
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        
        # Calculate RS and RSI
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on RSI.
        
        Args:
            data (pd.DataFrame): DataFrame with OHLCV data
            
        Returns:
            pd.DataFrame: DataFrame with signals (1 for buy, -1 for sell, 0 for hold)
        """
        # Calculate RSI
        data['RSI'] = self.calculate_rsi(data)
        
        # Generate signals
        data['Signal'] = 0
        data.loc[data['RSI'] < self.oversold, 'Signal'] = 1  # Buy signal
        data.loc[data['RSI'] > self.overbought, 'Signal'] = -1  # Sell signal
        
        # Generate actual trading signals (only when signal changes)
        data['Position'] = data['Signal'].diff()
        
        return data 