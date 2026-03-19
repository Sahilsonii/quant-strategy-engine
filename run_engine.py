import pandas as pd
import json
import argparse
import importlib

from engine.regimes.logic import detect_regime

# ---------------------------
# Dynamic Strategy Loader
# ---------------------------
def load_strategy(strategy_name, strategy_config):
    module = importlib.import_module(f"engine.strategies.{strategy_name}")
    class_name = strategy_config["logic_id"]
    strategy_class = getattr(module, class_name)
    return strategy_class(strategy_config["params"])

# ---------------------------
# Main Function
# ---------------------------
def main(config_path):

    # Load config
    with open(config_path) as f:
        config = json.load(f)

    # Load data
    df = pd.read_csv(config["data_file"])

    # Regime to strategy mapping
    regime_map = {
        "trend": "trend_following",
        "range": "range_play",
        "volatile": "volatility_breakout",
        "low_vol": "mean_reversion"
    }

    trades = []
    position = None

    # Start after enough data
    for i in range(50, len(df)-1):

        regime = detect_regime(df, i, config["regime_classifier"])
        strat_name = regime_map[regime]

        strat_config = config["strategies"][strat_name]
        strategy = load_strategy(strat_name, strat_config)

        signal = strategy.generate_signal(df, i)

        next_open = df['open'].iloc[i+1]
        date = df.index[i]

        # ENTRY
        if position is None and signal == 1:
            position = {
                "entry_dt": date,
                "entry_price": next_open,
                "qty": 1,
                "side": "LONG",
                "strategy_used": strat_name,
                "regime": regime,
                "entry_index": i
            }

        # EXIT
        elif position is not None and signal == -1:
            exit_price = next_open
            pnl = exit_price - position["entry_price"]

            trades.append({
                "entry_dt": position["entry_dt"],
                "entry_price": position["entry_price"],
                "qty": 1,
                "side": position["side"],
                "strategy_used": position["strategy_used"],
                "regime": position["regime"],
                "exit_dt": date,
                "exit_price": exit_price,
                "pnl": pnl,
                "bars_held": i - position["entry_index"]
            })

            position = None

    # Save output
    df_trades = pd.DataFrame(trades)
    df_trades = df_trades.sort_values("entry_dt")

    df_trades.to_excel("outputs/orders.xlsx", index=False)

    print("✅ Engine run complete! Check outputs/orders.xlsx")

# ---------------------------
# CLI ENTRY
# ---------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    main(args.config)