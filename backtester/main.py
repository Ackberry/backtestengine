import pandas as pd
from backtester.utils.data_loader import DataLoader
from backtester.strategies.moving_average import MovingAverageCrossover
from backtester.engine.backtest import Backtest

import os

def main():
    # Adjust path to match the actual directory structure
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    data_loader = DataLoader(data_dir)
    
    # Load sample data (you'll need to provide your own data file)
    try:
        data = data_loader.load_csv('sample_data.csv')
    except FileNotFoundError:
        print(f"Please place your OHLCV data in {os.path.join(data_dir, 'raw', 'sample_data.csv')}")
        print("Required columns: Date, Open, High, Low, Close, Volume")
        return
    
    # Initialize strategy
    strategy = MovingAverageCrossover(short_window=20, long_window=50)
    
    # Initialize and run backtest
    backtest = Backtest(
        data=data,
        strategy=strategy,
        initial_cash=100000.0,
        commission=0.001
    )
    
    # Run the backtest
    results = backtest.run()
    
    # Print results
    print("\nBacktest Results:")
    print(f"Final Equity: ${results['final_equity']:,.2f}")
    print(f"Total Trades: {results['total_trades']}")
    
    # Save results
    results['equity_curve'].to_csv(os.path.join(data_dir, 'processed', 'equity_curve.csv'))
    results['trade_history'].to_csv(os.path.join(data_dir, 'processed', 'trade_history.csv'))
    print(f"\nResults saved to {os.path.join(data_dir, 'processed')}/")

if __name__ == "__main__":
    main() 