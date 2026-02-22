# Backtesting Engine

import pandas as pd
from typing import Dict, List
from datetime import datetime

class Backtester:
    """Backtesting engine for strategy evaluation"""
    
    def __init__(self, strategy, initial_capital: float, commission: float = 0.001):
        """
        Initialize backtester
        
        Args:
            strategy: Strategy instance to backtest
            initial_capital: Starting account balance
            commission: Trading commission percentage
        """
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.current_equity = initial_capital
        self.commission = commission
        self.trades = []
        self.equity_curve = []
        self.results = {}
    
    def run(self, data: pd.DataFrame, symbols: List[str]) -> Dict:
        """
        Execute backtest on historical data
        
        Args:
            data: DataFrame with OHLCV data
            symbols: List of symbols to backtest
            
        Returns:
            Dictionary with backtest results
        """
        positions = {symbol: 0 for symbol in symbols}
        position_prices = {symbol: 0 for symbol in symbols}
        
        for idx, row in data.iterrows():
            # Calculate signals
            market_data = row.to_dict()
            signals = self.strategy.calculate_signals(market_data)
            
            # Process signals
            for signal in signals:
                if signal.symbol not in symbols:
                    continue
                
                if signal.direction == 'BUY' and positions[signal.symbol] == 0:
                    positions[signal.symbol] = 1
                    position_prices[signal.symbol] = signal.price
                    
                elif signal.direction == 'SELL' and positions[signal.symbol] > 0:
                    pnl = self._calculate_pnl(
                        signal.symbol,
                        position_prices[signal.symbol],
                        signal.price,
                        positions[signal.symbol]
                    )
                    self.current_equity += pnl
                    positions[signal.symbol] = 0
            
            # Update equity curve
            self.equity_curve.append({
                'date': row.get('date', idx),
                'equity': self.current_equity
            })
        
        # Calculate metrics
        self.results = self._calculate_metrics()
        return self.results
    
    def _calculate_pnl(self, symbol: str, entry_price: float, exit_price: float, qty: int) -> float:
        """Calculate profit/loss for trade"""
        gross_pnl = (exit_price - entry_price) * qty
        commission_cost = (entry_price + exit_price) * qty * self.commission
        return gross_pnl - commission_cost
    
    def _calculate_metrics(self) -> Dict:
        """Calculate performance metrics"""
        if not self.equity_curve:
            return {}
        
        equity_values = [e['equity'] for e in self.equity_curve]
        total_return = (self.current_equity - self.initial_capital) / self.initial_capital
        
        # Calculate maximum drawdown
        cumulative = pd.Series(equity_values)
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Calculate Sharpe Ratio (simplified)
        returns = pd.Series(equity_values).pct_change().dropna()
        sharpe_ratio = returns.mean() / returns.std() * (252 ** 0.5) if returns.std() > 0 else 0
        
        return {
            'initial_capital': self.initial_capital,
            'final_equity': self.current_equity,
            'total_return': total_return,
            'total_trades': len(self.strategy.trades),
            'max_drawdown': abs(max_drawdown),
            'sharpe_ratio': sharpe_ratio,
            'num_winning_trades': len([t for t in self.strategy.trades if t.pnl > 0]) if self.strategy.trades else 0
        }
    
    def get_results(self) -> Dict:
        """Return backtest results"""
        return self.results
    
    def get_equity_curve(self) -> List[Dict]:
        """Return equity curve data"""
        return self.equity_curve


class WalkForwardAnalysis:
    """Walk-forward analysis for out-of-sample testing"""
    
    def __init__(self, backtester: Backtester, train_period: int, test_period: int):
        """
        Initialize walk-forward analysis
        
        Args:
            backtester: Backtester instance
            train_period: Training period in days
            test_period: Test period in days
        """
        self.backtester = backtester
        self.train_period = train_period
        self.test_period = test_period
        self.results = []
    
    def run(self, data: pd.DataFrame, symbols: List[str]) -> List[Dict]:
        """
        Execute walk-forward analysis
        
        Args:
            data: Full dataset
            symbols: List of symbols
            
        Returns:
            List of test period results
        """
        total_periods = len(data)
        window_size = self.train_period + self.test_period
        
        walk_num = 0
        for start in range(0, total_periods - window_size, self.test_period):
            walk_num += 1
            
            # Split data
            train_data = data.iloc[start:start + self.train_period]
            test_data = data.iloc[start + self.train_period:start + window_size]
            
            # Run backtest on test data
            test_results = self.backtester.run(test_data, symbols)
            test_results['walk_num'] = walk_num
            
            self.results.append(test_results)
        
        return self.results
    
    def get_summary(self) -> Dict:
        """Calculate average metrics across all walks"""
        if not self.results:
            return {}
        
        keys = ['total_return', 'max_drawdown', 'sharpe_ratio']
        summary = {}
        
        for key in keys:
            values = [r.get(key, 0) for r in self.results if key in r]
            if values:
                summary[f'avg_{key}'] = sum(values) / len(values)
                summary[f'min_{key}'] = min(values)
                summary[f'max_{key}'] = max(values)
        
        return summary
