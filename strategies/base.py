# Trading Strategy Implementation Framework

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Signal:
    """Trading signal representation"""
    symbol: str
    direction: str  # 'BUY', 'SELL', 'HOLD'
    confidence: float  # 0.0 to 1.0
    price: float
    timestamp: str
    reason: str = ""

@dataclass
class Trade:
    """Executed trade record"""
    symbol: str
    direction: str
    entry_price: float
    entry_date: str
    quantity: int
    exit_price: Optional[float] = None
    exit_date: Optional[str] = None
    pnl: Optional[float] = None

class Strategy(ABC):
    """Base class for all trading strategies"""
    
    def __init__(self, name: str, parameters: Dict):
        """
        Initialize strategy
        
        Args:
            name: Strategy identifier
            parameters: Configuration parameters
        """
        self.name = name
        self.parameters = parameters
        self.trades: List[Trade] = []
        self.signals: List[Signal] = []
        
    @abstractmethod
    def calculate_signals(self, data: Dict) -> List[Signal]:
        """
        Generate trading signals from market data
        
        Args:
            data: Market data (OHLCV, indicators, etc.)
            
        Returns:
            List of trading signals
        """
        pass
    
    @abstractmethod
    def validate_parameters(self) -> bool:
        """
        Validate strategy parameters
        
        Returns:
            True if parameters valid, False otherwise
        """
        pass
    
    def add_trade(self, trade: Trade):
        """Record executed trade"""
        self.trades.append(trade)
    
    def get_performance_summary(self) -> Dict:
        """Calculate performance metrics"""
        if not self.trades:
            return {}
        
        completed_trades = [t for t in self.trades if t.exit_price is not None]
        if not completed_trades:
            return {}
        
        pnls = [t.pnl for t in completed_trades if t.pnl is not None]
        winning_trades = [p for p in pnls if p > 0]
        
        return {
            'total_trades': len(completed_trades),
            'winning_trades': len(winning_trades),
            'win_rate': len(winning_trades) / len(completed_trades) if completed_trades else 0,
            'total_pnl': sum(pnls),
            'avg_pnl': sum(pnls) / len(pnls) if pnls else 0
        }


class TrendFollowing(Strategy):
    """Trend following strategy using moving averages"""
    
    def __init__(self, parameters: Dict):
        super().__init__('TrendFollowing', parameters)
        self.validate_parameters()
    
    def validate_parameters(self) -> bool:
        """Validate required parameters"""
        required = ['fast_period', 'slow_period', 'min_confidence']
        return all(param in self.parameters for param in required)
    
    def calculate_signals(self, data: Dict) -> List[Signal]:
        """Generate signals based on moving average crossover"""
        signals = []
        
        # This is a template - actual implementation would include
        # SMA calculations, crossover detection, etc.
        
        return signals


class MeanReversion(Strategy):
    """Mean reversion strategy using Bollinger Bands"""
    
    def __init__(self, parameters: Dict):
        super().__init__('MeanReversion', parameters)
        self.validate_parameters()
    
    def validate_parameters(self) -> bool:
        """Validate required parameters"""
        required = ['period', 'std_dev_threshold', 'min_confidence']
        return all(param in self.parameters for param in required)
    
    def calculate_signals(self, data: Dict) -> List[Signal]:
        """Generate signals based on Bollinger Band deviations"""
        signals = []
        
        # This is a template - actual implementation would include
        # Bollinger Band calculations, deviation detection, etc.
        
        return signals


# Strategy factory for easy instantiation
class StrategyFactory:
    """Factory for creating strategy instances"""
    
    _strategies = {
        'trend_following': TrendFollowing,
        'mean_reversion': MeanReversion
    }
    
    @classmethod
    def create_strategy(cls, strategy_type: str, parameters: Dict) -> Strategy:
        """
        Create strategy instance
        
        Args:
            strategy_type: Type of strategy to create
            parameters: Configuration parameters
            
        Returns:
            Strategy instance
            
        Raises:
            ValueError: If strategy type not recognized
        """
        if strategy_type not in cls._strategies:
            raise ValueError(f"Unknown strategy type: {strategy_type}")
        
        strategy_class = cls._strategies[strategy_type]
        return strategy_class(parameters)
    
    @classmethod
    def register_strategy(cls, name: str, strategy_class):
        """Register new strategy type"""
        cls._strategies[name] = strategy_class
