from .strategy_base import StrategyBase

class TrendFollowing(StrategyBase):

    def generate_signal(self, df, i):
        fast = df['close'].rolling(self.params['fast_ma']).mean()
        slow = df['close'].rolling(self.params['slow_ma']).mean()

        if fast.iloc[i] > slow.iloc[i]:
            return 1   # BUY
        elif fast.iloc[i] < slow.iloc[i]:
            return -1  # SELL
        return 0