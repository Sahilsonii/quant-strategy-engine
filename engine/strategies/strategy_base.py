class StrategyBase:
    def __init__(self, params):
        self.params = params

    def generate_signal(self, df, i):
        raise NotImplementedError("Must implement generate_signal method")