import yaml
import pandas as pd
import yfinance as yf
from datetime import datetime
from strategies.moving_average import MovingAverageCrossover
from strategies.rsi_strategy import RSIStrategy
from utils.config import StrategyConfig
import matplotlib.pyplot as plt

def load_data(config):
    """Load historical data using yfinance."""
    symbol = config['data']['symbol']
    start_date = config['data']['start_date']
    end_date = config['data']['end_date']
    
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

def run_strategy(strategy_class, data, parameters):
    """Run a single strategy and return its signals."""
    strategy = strategy_class(parameters)
    if not strategy.validate_parameters():
        raise ValueError(f"Invalid parameters for {strategy_class.__name__}")
    
    signals = strategy.generate_signals(data.copy())
    return signals

def plot_results(data, signals_dict, symbol):
    """Plot the results for all strategies."""
    plt.figure(figsize=(15, 10))
    
    # Plot price
    plt.subplot(2, 1, 1)
    plt.plot(data.index, data['Close'], label='Price', color='black', alpha=0.5)
    
    # Plot buy/sell signals for each strategy
    colors = ['red', 'blue']
    for (strategy_name, signals), color in zip(signals_dict.items(), colors):
        buy_signals = signals[signals['Position'] == 1]
        sell_signals = signals[signals['Position'] == -1]
        
        plt.scatter(buy_signals.index, data.loc[buy_signals.index, 'Close'],
                   marker='^', color=color, label=f'{strategy_name} Buy')
        plt.scatter(sell_signals.index, data.loc[sell_signals.index, 'Close'],
                   marker='v', color=color, label=f'{strategy_name} Sell')
    
    plt.title(f'{symbol} Price and Trading Signals')
    plt.legend()
    plt.grid(True)
    
    # Plot strategy-specific indicators
    plt.subplot(2, 1, 2)
    for (strategy_name, signals), color in zip(signals_dict.items(), colors):
        if 'RSI' in signals.columns:
            plt.plot(signals.index, signals['RSI'], label=f'{strategy_name} RSI',
                    color=color, alpha=0.7)
        elif 'SMA_short' in signals.columns:
            plt.plot(signals.index, signals['SMA_short'], label=f'{strategy_name} Short MA',
                    color=color, alpha=0.7)
            plt.plot(signals.index, signals['SMA_long'], label=f'{strategy_name} Long MA',
                    color=color, alpha=0.7)
    
    plt.title('Strategy Indicators')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

def main():
    # Load configuration
    with open('config/sample_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Load historical data
    data = load_data(config)
    
    # Initialize strategies
    strategies = {
        'MA Crossover': (MovingAverageCrossover, config['strategies']['ma_crossover']['parameters']),
        'RSI': (RSIStrategy, config['strategies']['rsi']['parameters'])
    }
    
    # Run all strategies
    signals_dict = {}
    for strategy_name, (strategy_class, parameters) in strategies.items():
        try:
            signals = run_strategy(strategy_class, data, parameters)
            signals_dict[strategy_name] = signals
            print(f"\n{strategy_name} Strategy Results:")
            print(f"Number of buy signals: {len(signals[signals['Position'] == 1])}")
            print(f"Number of sell signals: {len(signals[signals['Position'] == -1])}")
        except Exception as e:
            print(f"Error running {strategy_name}: {str(e)}")
    
    # Plot results
    plot_results(data, signals_dict, config['data']['symbol'])

if __name__ == "__main__":
    main() 