from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd
import numpy as np

@dataclass
class Trade:
    timestamp: datetime
    type: str  # 'BUY' or 'SELL'
    price: float
    quantity: float
    value: float
    commission: float = 0.0

class Portfolio:
    def __init__(self, initial_cash: float = 100000.0, commission: float = 0.001):
        """
        Initialize the portfolio with initial cash and commission rate.
        
        Args:
            initial_cash (float): Initial cash amount
            commission (float): Commission rate per trade (e.g., 0.001 for 0.1%)
        """
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.commission = commission
        self.positions: Dict[str, float] = {}  # symbol -> quantity
        self.trades: List[Trade] = []
        self.equity_history: List[Dict] = []
        
    def execute_trade(self, symbol: str, timestamp: datetime, 
                     price: float, quantity: float, trade_type: str) -> None:
        """
        Execute a trade and update portfolio state.
        
        Args:
            symbol (str): Trading symbol
            timestamp (datetime): Trade timestamp
            price (float): Trade price
            quantity (float): Trade quantity
            trade_type (str): 'BUY' or 'SELL'
        """
        if trade_type not in ['BUY', 'SELL']:
            raise ValueError("trade_type must be 'BUY' or 'SELL'")
            
        commission_amount = price * quantity * self.commission
        trade_value = price * quantity
        
        if trade_type == 'BUY':
            if trade_value + commission_amount > self.cash:
                raise ValueError("Insufficient cash for trade")
            self.cash -= (trade_value + commission_amount)
            self.positions[symbol] = self.positions.get(symbol, 0) + quantity
        else:  # SELL
            if symbol not in self.positions or self.positions[symbol] < quantity:
                raise ValueError("Insufficient position for sell")
            self.cash += (trade_value - commission_amount)
            self.positions[symbol] -= quantity
            if self.positions[symbol] == 0:
                del self.positions[symbol]
        
        trade = Trade(
            timestamp=timestamp,
            type=trade_type,
            price=price,
            quantity=quantity,
            value=trade_value,
            commission=commission_amount
        )
        self.trades.append(trade)
        
    def update_equity(self, timestamp: datetime, current_prices: Dict[str, float]) -> None:
        """
        Update portfolio equity based on current prices.
        
        Args:
            timestamp (datetime): Current timestamp
            current_prices (Dict[str, float]): Current prices for each position
        """
        position_value = sum(
            quantity * current_prices[symbol]
            for symbol, quantity in self.positions.items()
        )
        total_equity = self.cash + position_value
        
        self.equity_history.append({
            'timestamp': timestamp,
            'cash': self.cash,
            'position_value': position_value,
            'total_equity': total_equity
        })
        
    def get_equity_curve(self) -> pd.DataFrame:
        """
        Get the portfolio equity curve as a DataFrame.
        
        Returns:
            pd.DataFrame: DataFrame containing equity history
        """
        if not self.equity_history:
            return pd.DataFrame()
            
        df = pd.DataFrame(self.equity_history)
        df.set_index('timestamp', inplace=True)
        return df
    
    def get_trade_history(self) -> pd.DataFrame:
        """
        Get the trade history as a DataFrame.
        
        Returns:
            pd.DataFrame: DataFrame containing trade history
        """
        if not self.trades:
            return pd.DataFrame()
            
        trades_data = [
            {
                'timestamp': trade.timestamp,
                'type': trade.type,
                'price': trade.price,
                'quantity': trade.quantity,
                'value': trade.value,
                'commission': trade.commission
            }
            for trade in self.trades
        ]
        return pd.DataFrame(trades_data) 