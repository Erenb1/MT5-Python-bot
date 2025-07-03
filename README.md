
# MetaTrader 5 Trading Bot

This project is a professional Python-based trading bot that uses crossover and EMA slope strategies to trade on MT5.

## Features
- EMA and FastEMA crossover strategy
- ATR-based SL/TP calculation
- Modular structure for extensibility
- Auto-login and candle timer sync

## Setup
1. Install requirements:
```bash
pip install pandas MetaTrader5 ta-lib
```

2. Add your MT5 credentials in `config.py`

3. Run the bot:
```bash
python main.py
```

## Files
- `main.py` - Main loop with login and signal check
- `strategies.py` - Signal generation logic
- `trade.py` - Position management
- `utils.py` - Helper functions
- `config.py` - User credentials and symbols
"# MT5-Python-bot" 
