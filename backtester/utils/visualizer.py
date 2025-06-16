import matplotlib.pyplot as plt
import pandas as pd


def plot_equity_curve(equity_curve, title='Equity Curve'):
    """
    Plot the equity curve.
    
    Args:
        equity_curve (pd.Series): Series of equity values
        title (str): Title for the plot
    """
    plt.figure(figsize=(10, 6))
    plt.plot(equity_curve.index, equity_curve.values, label='Equity')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Equity')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_drawdown_curve(equity_curve, title='Drawdown Curve'):
    """
    Plot the drawdown curve.
    
    Args:
        equity_curve (pd.Series): Series of equity values
        title (str): Title for the plot
    """
    rolling_max = equity_curve.expanding().max()
    drawdowns = (equity_curve - rolling_max) / rolling_max
    plt.figure(figsize=(10, 6))
    plt.plot(drawdowns.index, drawdowns.values, label='Drawdown')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Drawdown')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_trade_markers(equity_curve, trade_history, title='Trade Markers'):
    """
    Plot the equity curve with buy and sell markers.
    
    Args:
        equity_curve (pd.Series): Series of equity values
        trade_history (pd.DataFrame): DataFrame containing trade history with 'timestamp' and 'type' columns
        title (str): Title for the plot
    """
    plt.figure(figsize=(10, 6))
    plt.plot(equity_curve.index, equity_curve.values, label='Equity')
    
    for _, trade in trade_history.iterrows():
        if trade['type'] == 'BUY':
            plt.scatter(trade['timestamp'], equity_curve[trade['timestamp']], color='green', marker='^', label='Buy')
        else:
            plt.scatter(trade['timestamp'], equity_curve[trade['timestamp']], color='red', marker='v', label='Sell')
    
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Equity')
    plt.legend()
    plt.grid(True)
    plt.show() 