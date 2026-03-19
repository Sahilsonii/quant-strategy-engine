from .strategy_base import StrategyBase

class VolatilityBreakout(StrategyBase):

    def generate_signal(self, df, i):
        atr = (df['high'] - df['low']).rolling(self.params['atr_window']).mean()

        if df['high'].iloc[i] > df['high'].iloc[i-1] + atr.iloc[i] * self.params['multiplier']:
            return 1
        elif df['low'].iloc[i] < df['low'].iloc[i-1] - atr.iloc[i] * self.params['multiplier']:
            return -1
        return 0