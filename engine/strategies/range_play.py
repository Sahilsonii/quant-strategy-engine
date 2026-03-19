from .strategy_base import StrategyBase

class RangePlay(StrategyBase):

    def generate_signal(self, df, i):
        low = df['low'].rolling(self.params['lookback']).min()
        high = df['high'].rolling(self.params['lookback']).max()

        if df['close'].iloc[i] <= low.iloc[i]:
            return 1
        elif df['close'].iloc[i] >= high.iloc[i]:
            return -1
        return 0