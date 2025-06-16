from typing import Dict, Any, Optional
from datetime import datetime
import yaml
import os

class StrategyConfig:
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the strategy configuration.
        
        Args:
            config_path (Optional[str]): Path to the YAML configuration file
        """
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        
        if config_path and os.path.exists(config_path):
            self.load_config(config_path)
        else:
            self.set_default_config()
    
    def set_default_config(self) -> None:
        """Set default configuration values."""
        self.config = {
            'strategy': {
                'name': 'MovingAverageCrossover',
                'parameters': {
                    'short_window': 20,
                    'long_window': 50
                }
            },
            'backtest': {
                'start_date': '2020-01-01',
                'end_date': datetime.now().strftime('%Y-%m-%d'),
                'initial_capital': 100000,
                'commission': 0.001
            },
            'data': {
                'symbol': 'AAPL',
                'data_source': 'csv',
                'file_path': 'data/raw/stock_data.csv'
            }
        }
    
    def load_config(self, config_path: str) -> None:
        """
        Load configuration from a YAML file.
        
        Args:
            config_path (str): Path to the YAML configuration file
        """
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def save_config(self, config_path: Optional[str] = None) -> None:
        """
        Save configuration to a YAML file.
        
        Args:
            config_path (Optional[str]): Path to save the configuration file
        """
        if config_path is None:
            config_path = self.config_path
            
        if config_path is None:
            raise ValueError("No config path provided")
            
        with open(config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    def get_strategy_config(self) -> Dict[str, Any]:
        """
        Get the strategy configuration.
        
        Returns:
            Dict[str, Any]: Strategy configuration
        """
        return self.config.get('strategy', {})
    
    def get_backtest_config(self) -> Dict[str, Any]:
        """
        Get the backtest configuration.
        
        Returns:
            Dict[str, Any]: Backtest configuration
        """
        return self.config.get('backtest', {})
    
    def get_data_config(self) -> Dict[str, Any]:
        """
        Get the data configuration.
        
        Returns:
            Dict[str, Any]: Data configuration
        """
        return self.config.get('data', {})
    
    def update_strategy(self, strategy_name: str, parameters: Dict[str, Any]) -> None:
        """
        Update the strategy configuration.
        
        Args:
            strategy_name (str): Name of the strategy
            parameters (Dict[str, Any]): Strategy parameters
        """
        self.config['strategy'] = {
            'name': strategy_name,
            'parameters': parameters
        }
    
    def update_backtest(self, **kwargs) -> None:
        """
        Update the backtest configuration.
        
        Args:
            **kwargs: Backtest parameters to update
        """
        self.config['backtest'].update(kwargs)
    
    def update_data(self, **kwargs) -> None:
        """
        Update the data configuration.
        
        Args:
            **kwargs: Data parameters to update
        """
        self.config['data'].update(kwargs) 