from crypto_example import (
    example_compare_cryptos,
    example_crypto_backtest,
    example_crypto_signals,
    example_different_exchanges,
    example_fetch_crypto_data,
)


if __name__ == "__main__":
    print("=== Crypto examples ===")
    crypto_signals = example_crypto_signals()
    crypto_gain = example_crypto_backtest()
    print(f"\nCrypto signal summary: {crypto_signals}")
    if crypto_gain is None:
        print("Crypto backtest gain: n/a (insufficient data)")
    else:
        print(f"Crypto backtest gain: {crypto_gain:.2f}%")

    print("\n=== Additional crypto backtests (ETH + BNB) ===")
    crypto_comparison = example_compare_cryptos()
    print(f"\nCrypto comparison summary: {crypto_comparison}")

    # Uncomment to run additional crypto examples
    # example_fetch_crypto_data()
    # example_different_exchanges()