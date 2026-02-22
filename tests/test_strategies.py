# Unit tests for trading strategies

import pytest
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Import strategy classes
from strategies.base import Strategy, TrendFollowing, MeanReversion, StrategyFactory, Signal, Trade


class TestStrategyBase:
    """Test base Strategy class"""
    
    def test_strategy_initialization(self):
        """Test strategy can be initialized"""
        params = {'fast_period': 10, 'slow_period': 30}
        strategy = TrendFollowing(params)
        assert strategy.name == 'TrendFollowing'
        assert strategy.parameters == params
    
    def test_add_trade(self):
        """Test adding a trade"""
        params = {'fast_period': 10, 'slow_period': 30}
        strategy = TrendFollowing(params)
        
        trade = Trade(
            symbol='AAPL',
            direction='BUY',
            entry_price=150.0,
            entry_date='2026-01-01',
            quantity=100
        )
        
        strategy.add_trade(trade)
        assert len(strategy.trades) == 1
        assert strategy.trades[0].symbol == 'AAPL'
    
    def test_validate_parameters(self):
        """Test parameter validation"""
        params = {'fast_period': 10, 'slow_period': 30, 'min_confidence': 0.65}
        strategy = TrendFollowing(params)
        assert strategy.validate_parameters() == True
    
    def test_invalid_parameters(self):
        """Test with missing parameters"""
        params = {'fast_period': 10}  # Missing slow_period
        strategy = TrendFollowing(params)
        assert strategy.validate_parameters() == False


class TestSignalGeneration:
    """Test signal generation"""
    
    def test_signal_creation(self):
        """Test Signal object creation"""
        signal = Signal(
            symbol='AAPL',
            direction='BUY',
            confidence=0.85,
            price=150.0,
            timestamp='2026-01-01T10:30:00Z',
            reason='MA Crossover'
        )
        
        assert signal.symbol == 'AAPL'
        assert signal.direction == 'BUY'
        assert signal.confidence == 0.85
    
    def test_signal_validation(self):
        """Test signal direction validation"""
        valid_directions = ['BUY', 'SELL', 'HOLD']
        
        for direction in valid_directions:
            signal = Signal(
                symbol='AAPL',
                direction=direction,
                confidence=0.75,
                price=150.0,
                timestamp='2026-01-01T10:30:00Z'
            )
            assert signal.direction == direction


class TestStrategyFactory:
    """Test StrategyFactory"""
    
    def test_create_trend_following(self):
        """Test creating trend following strategy"""
        params = {'fast_period': 10, 'slow_period': 30, 'min_confidence': 0.65}
        strategy = StrategyFactory.create_strategy('trend_following', params)
        
        assert isinstance(strategy, TrendFollowing)
        assert strategy.name == 'TrendFollowing'
    
    def test_create_mean_reversion(self):
        """Test creating mean reversion strategy"""
        params = {'period': 20, 'std_dev_threshold': 2.0, 'min_confidence': 0.70}
        strategy = StrategyFactory.create_strategy('mean_reversion', params)
        
        assert isinstance(strategy, MeanReversion)
        assert strategy.name == 'MeanReversion'
    
    def test_unknown_strategy_raises_error(self):
        """Test unknown strategy raises ValueError"""
        params = {}
        with pytest.raises(ValueError):
            StrategyFactory.create_strategy('unknown_strategy', params)
    
    def test_register_custom_strategy(self):
        """Test registering custom strategy"""
        class CustomStrategy(Strategy):
            def __init__(self, parameters):
                super().__init__('CustomStrategy', parameters)
            
            def calculate_signals(self, data):
                return []
            
            def validate_parameters(self):
                return True
        
        StrategyFactory.register_strategy('custom', CustomStrategy)
        
        strategy = StrategyFactory.create_strategy('custom', {})
        assert strategy.name == 'CustomStrategy'


class TestTradeManagement:
    """Test trade management"""
    
    def test_trade_lifecycle(self):
        """Test complete trade lifecycle"""
        trade = Trade(
            symbol='AAPL',
            direction='BUY',
            entry_price=150.0,
            entry_date='2026-01-01',
            quantity=100
        )
        
        assert trade.exit_price is None
        assert trade.pnl is None
        
        # Close trade
        trade.exit_price = 155.0
        trade.exit_date = '2026-01-02'
        trade.pnl = (155.0 - 150.0) * 100
        
        assert trade.pnl == 500.0
    
    def test_performance_summary(self):
        """Test performance summary calculation"""
        params = {'fast_period': 10, 'slow_period': 30, 'min_confidence': 0.65}
        strategy = TrendFollowing(params)
        
        # Add some trades
        trade1 = Trade(
            symbol='AAPL',
            direction='BUY',
            entry_price=150.0,
            entry_date='2026-01-01',
            quantity=100,
            exit_price=155.0,
            exit_date='2026-01-02',
            pnl=500.0
        )
        
        trade2 = Trade(
            symbol='GOOGL',
            direction='BUY',
            entry_price=100.0,
            entry_date='2026-01-01',
            quantity=100,
            exit_price=98.0,
            exit_date='2026-01-02',
            pnl=-200.0
        )
        
        strategy.add_trade(trade1)
        strategy.add_trade(trade2)
        
        summary = strategy.get_performance_summary()
        assert summary['total_trades'] == 2
        assert summary['winning_trades'] == 1
        assert summary['win_rate'] == 0.5
        assert summary['total_pnl'] == 300.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
