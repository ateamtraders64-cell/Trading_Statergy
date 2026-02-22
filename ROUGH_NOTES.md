# Team Notes & Rough Work

**Purpose**: Quick notes, sketches, and rough work between team members  
**Format**: Raw, informal, stream of consciousness  
**Keep Here**: Draft ideas, sketches, partial thoughts, questions

---

## Latest Notes

### Arun's Workspace

**Strategy Architecture Thoughts - Feb 22**
```
Been thinking about how strategies need to be flexible but consistent.
Current class hierarchy seems good:
- Strategy (base)
  - TrendFollowing
  - MeanReversion
  - BrokerAdapter (future)

Maybe add:
- Composite strategy (combine multiple strategies)?
- Weighted strategies (sum of signals)?

Also wondering about state management. Strategies shouldn't keep state across
backtests, but live trading will need state. How to handle this?
```

**Risk Management Questions**
```
Looking at risk_limits.json - wondering if we need:
1. More granular time-based limits (hourly, by market session)
2. Dynamic limits based on market volatility?
3. Counterparty exposure tracking?

These are probably later though. Start simple.
```

---

### Surendar's Workspace

**Implementation Notes - Feb 22**
```
Working on backtester.py - got the basic structure down.
Still need to:
- Add slippage calculation
- Implement commission properly (different per broker)
- Test with actual data (need samples)
- Optimize for speed (vectorization where possible)

Performance question: should we use NumPy arrays or Pandas Series?
NumPy is faster, Pandas is easier to work with.
For daily data probably doesn't matter, but good to plan.
```

**Docker Setup Challenges**
```
docker-compose.yml looks good but:
- Redis config: do we need persistence?
- PostgreSQL: need init scripts for schema
- Healthchecks: might be slow for initial startup
- Volume mounts: make sure correct for development

Probably need to test locally on Mac.
```

---

## Sketches & Diagrams

### Data Flow Sketch
```
Market Data
    ↓
Validation → Cache → Database
    ↓
Signal Calculation
    ↓
Risk Check
    ↓
Order Generation
    ↓
Execution?
    ↓
Position Tracking
    ↓
Reporting
```

### Strategy Decision Tree
```
Data Available
    ↓
Calculate Indicators
    ├→ Trend Strength?
    │   ├→ Strong → TrendFollowing enabled
    │   └→ Weak → Check other signals
    │
    ├→ Volatility Level?
    │   ├→ High → Mean Reversion attractive
    │   └→ Low → (Skip?)
    │
    └→ Combine Signals → Generate trade recommendation

Not sure if this is right structure...
```

---

## Code Sketches

### Idea: Composite Strategy Pattern
```python
# Rough sketch - needs refinement

class CompositeStrategy(Strategy):
    def __init__(self, *strategies, weights=None):
        self.strategies = strategies
        self.weights = weights or [1/len(strategies)] * len(strategies)
    
    def calculate_signals(self, data):
        all_signals = []
        for strategy, weight in zip(self.strategies, self.weights):
            signals = strategy.calculate_signals(data)
            # Weight the signals somehow?
            # How to combine different signal types?
            all_signals.extend(signals)
        
        # Combine and return?
        return combined_signals

# Issue: How to weight incompatible signals?
# Do we need to normalize confidence scores?
```

### Idea: Regime Detector
```python
# Very rough sketch

class RegimeDetector:
    def __init__(self):
        self.regimes = ['bull', 'bear', 'sideways']
    
    def detect_regime(self, prices):
        # Look at trend
        # Look at volatility
        # Look at momentum
        # Classify current regime
        return regime
    
    def get_regime_probabilities(self, prices):
        # Return probability for each regime
        # e.g., {'bull': 0.6, 'bear': 0.3, 'sideways': 0.1}
        return probabilities

# Could use this to:
# - Filter strategies appropriate for regime
# - Weight strategies by suitability
# - Adjust parameters dynamically
```

---

## Questions & Blockers

**For Arun:**
1. Should CompositeStrategy be in base.py or separate file?
2. How do we handle strategy state in live vs backtest modes?
3. Risk limits - per-position or per-strategy or portfolio-level?

**For Surendar:**
1. What's the priority: backtester optimization or new features?
2. Should we build sample data generator or use real data?
3. Commission structure - how detailed should we get?

**For Both:**
1. What's MVP criteria? When do we consider v1 "done"?
2. How do we integrate with actual brokers/data feeds?
3. Testing strategy - unit tests sufficient or need integration tests too?
4. Documentation - is current level enough or need more detail?

---

## Decision Points (Waiting on)

- [ ] **Composite Strategy**: Arun - is this worth pursuing?
- [ ] **ML Integration**: Worth the effort? When?
- [ ] **Real-time Support**: Phase 1 or Phase 2?
- [ ] **Broker Integration**: Start with paper trading or add broker API soon?
- [ ] **Database Schema**: Need to design PostgreSQL schema

---

## Parking Lot (Ideas for Later)

- [ ] Multi-timeframe analysis
- [ ] Sentiment integration
- [ ] Advanced Monte Carlo simulation
- [ ] Machine Learning models
- [ ] Mobile app/dashboard
- [ ] Strategy marketplace
- [ ] Performance attribution analysis
- [ ] Custom indicators library
- [ ] Automated rebalancing schedules
- [ ] Tax-aware position management

---

## Quick Reference Links

- Ideas: `IDEAS_AND_DISCUSSIONS.md` (where we discuss structured ideas)
- This file: `ROUGH_NOTES.md` (raw, quick thoughts)
- Docs: `docs/` folder (formal documentation)
- Config: `config/` folder (parameter specifications)

---

## How to Use This File

1. **Add Quick Thoughts**: Just dump them in your workspace section
2. **Sketch Ideas**: Use code blocks and ASCII art freely
3. **Ask Questions**: List them - the other person will respond
4. **Store Rough Work**: Don't worry about polish or structure
5. **Build on Each Other**: Reference and expand on each other's notes
6. **Promote Ideas**: When idea is solid, move to IDEAS_AND_DISCUSSIONS.md

---

**Remember**: This is a working file. Total chaos is OK here. 
Structure and polish happen in other documents.

**Last Updated:** February 22, 2026  
**Contributors:** Arun, Surendar
