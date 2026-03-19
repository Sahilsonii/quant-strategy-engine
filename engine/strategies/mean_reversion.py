from .strategy_base import StrategyBase

class MeanReversion(StrategyBase):

    def generate_signal(self, df, i):
        delta = df['close'].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        rs = gain.rolling(self.params['rsi_window']).mean() / loss.rolling(self.params['rsi_window']).mean()
        rsi = 100 - (100 / (1 + rs))

        if rsi.iloc[i] < self.params['rsi_buy']:
            return 1
        elif rsi.iloc[i] > self.params['rsi_sell']:
            return -1
        return 0