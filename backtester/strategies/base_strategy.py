from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any, Optional

class BaseStrategy(ABC):
    """
    Abstract base class for all trading strategies.
    All strategy implementations must inherit from this class.
    """
    
    def __init__(self, parameters: Dict[str, Any]):
        """
        Initialize the strategy with its parameters.
        
        Args:
            parameters (Dict[str, Any]): Dictionary of strategy parameters
        """
        self.parameters = parameters
        self.position = 0  # Current position (1 for long, -1 for short, 0 for no position)
        self.signals = None  # Will store the generated signals
        
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on the strategy logic.
        
        Args:
            data (pd.DataFrame): OHLCV data
            
        Returns:
            pd.DataFrame: DataFrame with signals (1 for buy, -1 for sell, 0 for hold)
        """
        pass
    
    @abstractmethod
    def validate_parameters(self) -> bool:
        """
        Validate the strategy parameters.
        
        Returns:
            bool: True if parameters are valid, False otherwise
        """
        pass
    
    def get_position(self) -> int:
        """
        Get the current position.
        
        Returns:
            int: Current position (1 for long, -1 for short, 0 for no position)
        """
        return self.position
    
    def update_position(self, signal: int) -> None:
        """
        Update the current position based on the signal.
        
        Args:
            signal (int): Trading signal (1 for buy, -1 for sell, 0 for hold)
        """
        self.position = signal 