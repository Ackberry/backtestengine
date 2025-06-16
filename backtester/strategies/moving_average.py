import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any
from .base_strategy import BaseStrategy

class MovingAverageCrossover(BaseStrategy):
    def __init__(self, parameters: Dict[str, Any]):
        """
        Initialize the Moving Average Crossover strategy.
        
        Args:
            parameters (Dict[str, Any]): Dictionary containing:
                - short_window (int): Short-term moving average window
                - long_window (int): Long-term moving average window
        """
        super().__init__(parameters)
        self.short_window = parameters.get('short_window', 20)
        self.long_window = parameters.get('long_window', 50)
        
    def validate_parameters(self) -> bool:
        """
        Validate the strategy parameters.
        
        Returns:
            bool: True if parameters are valid, False otherwise
        """
        if not isinstance(self.short_window, int) or not isinstance(self.long_window, int):
            return False
        if self.short_window >= self.long_window:
            return False
        if self.short_window <= 0 or self.long_window <= 0:
            return False
        return True
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on moving average crossover.
        
        Args:
            data (pd.DataFrame): DataFrame with OHLCV data
            
        Returns:
            pd.DataFrame: DataFrame with signals (1 for buy, -1 for sell, 0 for hold)
        """
        # Calculate moving averages
        data['SMA_short'] = data['Close'].rolling(window=self.short_window).mean()
        data['SMA_long'] = data['Close'].rolling(window=self.long_window).mean()
        
        # Generate signals
        data['Signal'] = 0
        data.loc[data['SMA_short'] > data['SMA_long'], 'Signal'] = 1  # Buy signal
        data.loc[data['SMA_short'] < data['SMA_long'], 'Signal'] = -1  # Sell signal
        
        # Generate actual trading signals (only when signal changes)
        data['Position'] = data['Signal'].diff()
        
        return data
    
    def calculate_position_size(self, price: float, portfolio_value: float, 
                              risk_per_trade: float = 0.02) -> float:
        """
        Calculate the position size based on portfolio value and risk per trade.
        
        Args:
            price (float): Current price
            portfolio_value (float): Current portfolio value
            risk_per_trade (float): Maximum risk per trade as a fraction of portfolio
            
        Returns:
            float: Number of shares to trade
        """
        position_value = portfolio_value * risk_per_trade
        return position_value / price 