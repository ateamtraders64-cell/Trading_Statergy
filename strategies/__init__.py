# Strategies Package
__version__ = '1.0.0'

from .base import (
    Strategy,
    Signal,
    Trade,
    TrendFollowing,
    MeanReversion,
    StrategyFactory
)

__all__ = [
    'Strategy',
    'Signal',
    'Trade',
    'TrendFollowing',
    'MeanReversion',
    'StrategyFactory'
]
