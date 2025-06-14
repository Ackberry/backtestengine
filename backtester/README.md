# Backtesting Engine for Trading Strategies

A modular Python-based backtesting engine for simulating and evaluating trading strategies over historical data.

## Features

- Load and process historical OHLCV data
- Implement and test trading strategies
- Track portfolio performance and trade history
- Calculate key performance metrics
- Visualize results

## Project Structure

```
backtester/
├── data/
│   ├── raw/                     # Raw historical data (CSV)
│   └── processed/               # Processed data and results
├── strategies/
│   └── moving_average.py        # MA Crossover strategy
├── engine/
│   ├── backtest.py             # Core simulation logic
│   └── portfolio.py            # Portfolio management
├── utils/
│   └── data_loader.py          # Data loading utilities
├── main.py                     # Example usage
└── requirements.txt            # Dependencies
```

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your historical OHLCV data in `data/raw/sample_data.csv` with the following columns:
   - Date
   - Open
   - High
   - Low
   - Close
   - Volume

2. Run the backtest:
```bash
python main.py
```

## Current Implementation

The current implementation includes:

- Data loading and processing
- Moving Average Crossover strategy (20/50-day)
- Portfolio management with commission handling
- Basic backtesting engine
- Trade and equity tracking

## Development Roadmap

### Phase 1 - Core Backtest Engine (Completed)
- [x] Data loading
- [x] Portfolio management
- [x] Moving Average strategy
- [x] Basic backtesting

### Phase 2 - Performance Analytics (Next)
- [ ] Performance metrics
- [ ] Visualization tools
- [ ] Report generation

### Phase 3 - Modular Strategy System
- [ ] Base strategy class
- [ ] Additional strategies
- [ ] Strategy configuration

### Phase 4 - CLI/UI Interface
- [ ] Command-line interface
- [ ] Optional web UI

### Phase 5 - Live Data Integration
- [ ] Real-time data feeds
- [ ] Paper trading simulation

## Contributing

Feel free to submit issues and enhancement requests! 