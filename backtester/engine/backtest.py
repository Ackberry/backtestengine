from typing import Dict, Any
import pandas as pd
from datetime import datetime

from backtester.strategies.moving_average import MovingAverageCrossover
from backtester.engine.portfolio import Portfolio

class Backtest:
    def __init__(self, data: pd.DataFrame, strategy: MovingAverageCrossover,
                 initial_cash: float = 100000.0, commission: float = 0.001):
        """
        Initialize the backtest with data, strategy, and portfolio parameters.
        
        Args:
            data (pd.DataFrame): Historical OHLCV data
            strategy (MovingAverageCrossover): Trading strategy
            initial_cash (float): Initial portfolio cash
            commission (float): Commission rate per trade
        """
        self.data = data
        self.strategy = strategy
        self.portfolio = Portfolio(initial_cash=initial_cash, commission=commission)
        self.results = None
        
    def run(self) -> Dict[str, Any]:
        """
        Run the backtest simulation.
        
        Returns:
            Dict[str, Any]: Backtest results including equity curve and trade history
        """
        # Generate trading signals
        signals = self.strategy.generate_signals(self.data)
        
        # Iterate through each day
        for timestamp, row in signals.iterrows():
            if pd.isna(row['Position']):
                continue
                
            # Update portfolio equity
            current_prices = {'symbol': row['Close']}  # Assuming single symbol for now
            self.portfolio.update_equity(timestamp, current_prices)
            
            # Execute trades based on signals
            if row['Position'] != 0:
                trade_type = 'BUY' if row['Position'] > 0 else 'SELL'
                quantity = self.strategy.calculate_position_size(
                    row['Close'],
                    self.portfolio.cash
                )
                
                try:
                    self.portfolio.execute_trade(
                        symbol='symbol',  # Assuming single symbol for now
                        timestamp=timestamp,
                        price=row['Close'],
                        quantity=quantity,
                        trade_type=trade_type
                    )
                except ValueError as e:
                    print(f"Trade execution failed: {e}")
        
        # Get final results
        equity_curve = self.portfolio.get_equity_curve()
        trade_history = self.portfolio.get_trade_history()
        
        self.results = {
            'equity_curve': equity_curve,
            'trade_history': trade_history,
            'final_equity': equity_curve['total_equity'].iloc[-1] if not equity_curve.empty else self.portfolio.initial_cash,
            'total_trades': len(trade_history) if not trade_history.empty else 0
        }
        
        return self.results
    
    def get_results(self) -> Dict[str, Any]:
        """
        Get the backtest results.
        
        Returns:
            Dict[str, Any]: Backtest results
        """
        if self.results is None:
            raise ValueError("Backtest has not been run yet")
        return self.results 