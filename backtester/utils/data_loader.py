import pandas as pd
from pathlib import Path
from typing import Union, Optional

class DataLoader:
    def __init__(self, data_dir: Union[str, Path]):
        """
        Initialize the DataLoader with the data directory path.
        
        Args:
            data_dir (Union[str, Path]): Path to the data directory
        """
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / 'raw'
        self.processed_dir = self.data_dir / 'processed'
        
        # Create directories if they don't exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
    
    def load_csv(self, filename: str) -> pd.DataFrame:
        """
        Load OHLCV data from a CSV file.
        
        Args:
            filename (str): Name of the CSV file in the raw directory
            
        Returns:
            pd.DataFrame: DataFrame containing OHLCV data with datetime index
        """
        file_path = self.raw_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Ensure required columns exist
        required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Convert Date column to datetime index
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        
        # Sort by date
        df.sort_index(inplace=True)
        
        return df
    
    def save_processed_data(self, df: pd.DataFrame, filename: str) -> None:
        """
        Save processed data to the processed directory.
        
        Args:
            df (pd.DataFrame): DataFrame to save
            filename (str): Name of the output file
        """
        output_path = self.processed_dir / filename
        df.to_csv(output_path) 