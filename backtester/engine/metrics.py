import numpy as np
import pandas as pd


def calculate_sharpe_ratio(returns, risk_free_rate=0.01, periods_per_year=252):
    """
    Calculate the Sharpe Ratio for a series of returns.
    
    Args:
        returns (pd.Series): Series of daily returns
        risk_free_rate (float): Annual risk-free rate
        periods_per_year (int): Number of periods in a year (e.g., 252 for daily data)
    
    Returns:
        float: Sharpe Ratio
    """
    excess_returns = returns - risk_free_rate / periods_per_year
    return np.sqrt(periods_per_year) * excess_returns.mean() / excess_returns.std()


def calculate_max_drawdown(equity_curve):
    """
    Calculate the maximum drawdown from an equity curve.
    
    Args:
        equity_curve (pd.Series): Series of equity values
    
    Returns:
        float: Maximum drawdown as a percentage
    """
    rolling_max = equity_curve.expanding().max()
    drawdowns = (equity_curve - rolling_max) / rolling_max
    return drawdowns.min()


def calculate_win_rate(trade_history):
    """
    Calculate the win rate from a trade history.
    
    Args:
        trade_history (pd.DataFrame): DataFrame containing trade history with 'value' column
    
    Returns:
        float: Win rate as a percentage
    """
    if trade_history.empty:
        return 0.0
    profitable_trades = trade_history[trade_history['value'] > 0]
    return len(profitable_trades) / len(trade_history)


def calculate_cagr(equity_curve, periods_per_year=252):
    """
    Calculate the Compound Annual Growth Rate (CAGR) from an equity curve.
    
    Args:
        equity_curve (pd.Series): Series of equity values
        periods_per_year (int): Number of periods in a year (e.g., 252 for daily data)
    
    Returns:
        float: CAGR as a percentage
    """
    if len(equity_curve) < 2:
        return 0.0
    total_return = (equity_curve.iloc[-1] / equity_curve.iloc[0]) - 1
    years = len(equity_curve) / periods_per_year
    return (1 + total_return) ** (1 / years) - 1


def calculate_volatility(returns, periods_per_year=252):
    """
    Calculate the annualized volatility from a series of returns.
    
    Args:
        returns (pd.Series): Series of daily returns
        periods_per_year (int): Number of periods in a year (e.g., 252 for daily data)
    
    Returns:
        float: Annualized volatility as a percentage
    """
    return returns.std() * np.sqrt(periods_per_year)


def generate_performance_report(equity_curve, trade_history, risk_free_rate=0.01, periods_per_year=252):
    """
    Generate a comprehensive performance report for the backtest.
    
    Args:
        equity_curve (pd.Series): Series of equity values
        trade_history (pd.DataFrame): DataFrame containing trade history
        risk_free_rate (float): Annual risk-free rate
        periods_per_year (int): Number of periods in a year (e.g., 252 for daily data)
    
    Returns:
        dict: Dictionary containing performance metrics
    """
    returns = equity_curve.pct_change().dropna()
    
    report = {
        'Sharpe Ratio': calculate_sharpe_ratio(returns, risk_free_rate, periods_per_year),
        'Max Drawdown': calculate_max_drawdown(equity_curve),
        'Win Rate': calculate_win_rate(trade_history),
        'CAGR': calculate_cagr(equity_curve, periods_per_year),
        'Volatility': calculate_volatility(returns, periods_per_year)
    }
    
    return report 