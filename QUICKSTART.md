# Quick Start Guide

Get the Trading Strategy project running in 5 minutes!

## Prerequisites

- Python 3.9+
- Docker & Docker Compose (optional)
- Git

## Option 1: Local Setup (Quick)

### 1. Clone Repository
```bash
git clone <repo-url>
cd Trading_Statergy
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Tests
```bash
pytest tests/ -v
```

### 5. Quick Backtest
```python
import pandas as pd
from strategies.base import StrategyFactory
from analysis.backtester import Backtester

# Create strategy
params = {
    'fast_period': 10,
    'slow_period': 30,
    'min_confidence': 0.65
}
strategy = StrategyFactory.create_strategy('trend_following', params)

# Load sample data
data = pd.read_csv('tests/fixtures/sample_data.csv')

# Run backtest
backtester = Backtester(strategy, initial_capital=100000)
results = backtester.run(data, symbols=['AAPL'])

print(f"Total Return: {results['total_return']:.2%}")
print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
print(f"Max Drawdown: {results['max_drawdown']:.2%}")
```

## Option 2: Docker Setup (Recommended)

### 1. Clone Repository
```bash
git clone <repo-url>
cd Trading_Statergy
```

### 2. Start Containers
```bash
docker-compose up -d
```

### 3. Check Services
```bash
docker-compose ps
```

### 4. View Logs
```bash
docker-compose logs -f api
```

### 5. Stop Services
```bash
docker-compose down
```

## Project Structure

```
Trading_Statergy/
├── docs/                 # Comprehensive documentation
├── strategies/           # Trading strategy implementations
├── analysis/            # Backtesting and analysis tools
├── config/              # Configuration files
├── tests/               # Unit and integration tests
└── README.md            # Overview
```

## Key Commands

### Running Tests
```bash
# All tests
pytest tests/

# With coverage
pytest tests/ --cov=.

# Specific test
pytest tests/test_strategies.py::TestStrategyBase::test_strategy_initialization
```

### Code Quality
```bash
# Format code
black .

# Check style
flake8

# Type checking
mypy
```

### Data & Configuration
- **Strategies**: Edit `config/strategy_config.json`
- **Risk Limits**: Edit `config/risk_limits.json`
- **Data Files**: Place in `data/` directory (create if needed)

## Common Tasks

### Create New Strategy

1. **Create strategy file**
```python
# strategies/my_strategy.py
from strategies.base import Strategy, Signal

class MyStrategy(Strategy):
    def __init__(self, parameters):
        super().__init__('MyStrategy', parameters)
    
    def validate_parameters(self):
        return 'key_param' in self.parameters
    
    def calculate_signals(self, data):
        return []  # Your signal logic
```

2. **Register in factory**
```python
StrategyFactory.register_strategy('my_strategy', MyStrategy)
```

3. **Test it**
```python
strategy = StrategyFactory.create_strategy('my_strategy', {'key_param': value})
signals = strategy.calculate_signals(data)
```

### Run a Backtest

```python
from strategies.base import StrategyFactory
from analysis.backtester import Backtester

# Create strategy
strategy = StrategyFactory.create_strategy('trend_following', {
    'fast_period': 10,
    'slow_period': 30,
    'min_confidence': 0.65
})

# Create backtester
backtester = Backtester(strategy, initial_capital=100000)

# Run backtest
results = backtester.run(data, symbols=['AAPL', 'GOOGL'])

# View results
print(results)
```

### Add Risk Monitoring

```python
from analysis.risk_analyzer import RiskManager

risk_mgr = RiskManager(
    max_position_size=0.10,
    max_drawdown=0.15
)

# Check position size
position_in_capital = risk_mgr.calculate_position_size(
    account_balance=100000,
    risk=0.02
)

# Verify drawdown
is_ok = risk_mgr.check_risk_limits(
    current_equity=95000,
    peak_equity=100000
)
```

## Next Steps

1. **Read Core Documentation**
   - [Strategy Guide](docs/01_STRATEGY_GUIDE.md) - Understand strategy components
   - [Architecture](docs/02_ARCHITECTURE.md) - System architecture overview
   - [Implementation](docs/03_IMPLEMENTATION.md) - Detailed implementation guide

2. **Explore Examples**
   - Check `tests/` for real usage examples
   - Review `config/` for parameter templates

3. **Run Backtests**
   - Use sample data in `tests/fixtures/`
   - Compare strategy performance
   - Fine-tune parameters

4. **Deploy Strategy**
   - Configure in `strategy_config.json`
   - Set risk limits in `risk_limits.json`
   - Deploy using Docker

## Troubleshooting

### Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Database Issues
```bash
# Check PostgreSQL is running
psql -U admin -h localhost

# Reset database
dropdb trading_strategy
createdb trading_strategy
```

### Test Failures
```bash
# Run with verbose output
pytest tests/ -vv -s

# Run specific test
pytest tests/test_strategies.py::TestStrategyBase -v
```

## Resources

- **Documentation**: See `docs/` folder
- **Code Examples**: Check `tests/` folder
- **Configuration Templates**: See `config/` folder

## Getting Help

- Review documentation in `docs/`
- Check test examples in `tests/`
- Contact team members:
  - **Arun** (Architecture): arun@example.com
  - **Surendar** (Implementation): surendar@example.com

## What's Next?

- [ ] Run the tests
- [ ] Review the architecture
- [ ] Explore existing strategies
- [ ] Create your first strategy
- [ ] Run a backtest
- [ ] Read contributing guidelines

---

**Happy trading! 📈**
