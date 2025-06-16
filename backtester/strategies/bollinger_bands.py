import pandas as pd
import numpy as np
from typing import Dict, Any
from .base_strategy import BaseStrategy

class BollingerBandsStrategy(BaseStrategy):
    def __init__(self, parameters: Dict[str, Any]):
        """
        Initialize the Bollinger Bands strategy.
        
        Args:
            parameters (Dict[str, Any]): Dictionary containing:
                - period (int): Moving average period for Bollinger Bands
                - std_dev (float): Number of standard deviations for bands
                - use_volume (bool): Whether to use volume in signal generation
        """
        super().__init__(parameters)
        self.period = parameters.get('period', 20)
        self.std_dev = parameters.get('std_dev', 2.0)
        self.use_volume = parameters.get('use_volume', False)
        
    def validate_parameters(self) -> bool:
        """
        Validate the strategy parameters.
        
        Returns:
            bool: True if parameters are valid, False otherwise
        """
        if not isinstance(self.period, int) or self.period <= 0:
            return False
        if not isinstance(self.std_dev, (int, float)) or self.std_dev <= 0:
            return False
        if not isinstance(self.use_volume, bool):
            return False
        return True
        
    def calculate_bollinger_bands(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate Bollinger Bands for the given data.
        
        Args:
            data (pd.DataFrame): DataFrame with OHLCV data
            
        Returns:
            pd.DataFrame: DataFrame with Bollinger Bands added
        """
        data = data.copy()  # Avoid SettingWithCopyWarning
        # Calculate middle band (SMA)
        data['Middle_Band'] = data['Close'].rolling(window=self.period).mean()
        
        # Calculate standard deviation
        data['Std_Dev'] = data['Close'].rolling(window=self.period).std()
        
        # Calculate upper and lower bands
        data['Upper_Band'] = data['Middle_Band'] + (data['Std_Dev'] * self.std_dev)
        data['Lower_Band'] = data['Middle_Band'] - (data['Std_Dev'] * self.std_dev)
        
        # Calculate bandwidth and %B as single columns
        data['Bandwidth'] = (data['Upper_Band'] - data['Lower_Band']) / data['Middle_Band']
        data['Percent_B'] = (data['Close'] - data['Lower_Band']) / (data['Upper_Band'] - data['Lower_Band'])
        
        return data
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on Bollinger Bands.
        
        Args:
            data (pd.DataFrame): DataFrame with OHLCV data
            
        Returns:
            pd.DataFrame: DataFrame with signals (1 for buy, -1 for sell, 0 for hold)
        """
        # Calculate Bollinger Bands
        data = self.calculate_bollinger_bands(data)
        
        # Initialize signals
        data['Signal'] = 0
        
        # Generate signals based on price touching bands
        data.loc[data['Close'] <= data['Lower_Band'], 'Signal'] = 1  # Buy signal
        data.loc[data['Close'] >= data['Upper_Band'], 'Signal'] = -1  # Sell signal
        
        if self.use_volume:
            # Add volume confirmation
            volume_ma = data['Volume'].rolling(window=self.period).mean()
            data.loc[data['Volume'] < volume_ma, 'Signal'] = 0  # Cancel signals on low volume
        
        # Generate actual trading signals (only when signal changes)
        data['Position'] = data['Signal'].diff()
        
        return data
    
    def get_bandwidth(self, data: pd.DataFrame) -> pd.Series:
        """
        Get the Bollinger Bandwidth for volatility analysis.
        
        Args:
            data (pd.DataFrame): DataFrame with OHLCV data
            
        Returns:
            pd.Series: Bollinger Bandwidth values
        """
        data = self.calculate_bollinger_bands(data)
        return data['Bandwidth']
    
    def get_percent_b(self, data: pd.DataFrame) -> pd.Series:
        """
        Get the %B indicator for relative price position.
        
        Args:
            data (pd.DataFrame): DataFrame with OHLCV data
            
        Returns:
            pd.Series: %B values
        """
        data = self.calculate_bollinger_bands(data)
        return data['Percent_B'] 