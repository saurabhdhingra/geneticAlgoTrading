# Genetic Algorithm Optimized Trading Strategy

This repository explores the application of Genetic Algorithms (GAs) to optimize parameters for a combined Bollinger Bands and Relative Strength Index (RSI) trading strategy. Inspired by natural selection, GAs are powerful optimisation and search techniques well-suited for tuning complex, non-linear problems like trading strategy parameter selection in equity and cryptocurrency markets.

## Strategy Components
The trading strategy is built upon the confluence of two widely-used technical indicators: Bollinger Bands and the Relative Strength Index (RSI).

### 1. Bollinger Bands

Bollinger Bands consist of three lines:

- A **Middle Band** (typically a Simple Moving Average - SMA).

- An **Upper Band** (a specified number of standard deviations above the middle band).

- A **Lower Band** (a specified number of standard deviations below the middle band).

They are used to measure volatility and identify potential reversal points. Price movements near the upper band suggest an overbought condition, while movements near the lower band suggest an oversold condition.

![unnamed-4](https://github.com/user-attachments/assets/22b03ddb-bce7-4614-825d-1b5baec69127)

### 2. Relative Strength Index (RSI)

RSI is a momentum oscillator that measures the speed and change of price movements, ranging from 0 to 100.

- RSI values **above 70** are typically interpreted as overbought, signalling a potential reversal to the downside.

- RSI values **below 30** are considered oversold, signalling a potential reversal to the upside.

![unnamed](https://github.com/user-attachments/assets/f8c640fa-ceb7-41bc-acee-015a9b5d32cc)

### Combined Strategy Logic

The strategy uses these indicators for confirmation, aiming for higher-conviction entry points:

- **Sell Signal**: Generated when the price is near the Upper Bollinger Band and the RSI is above the Overbought Level (e.g., 70).

- **Buy Signal**: Generated when the price is near the Lower Bollinger Band and the RSI is below the Oversold Level (e.g., 30).

![unnamed-2](https://github.com/user-attachments/assets/7d1b3aa1-e928-4757-b771-80d7b929c837)

## Optimisation with Genetic Algorithms

The core of this project is the use of a Genetic Algorithm to find the most profitable combination of parameters for the trading strategy. The algorithm is designed to backtest against historical data fetched from Binance APIs, using a fitness function to evaluate the performance of each parameter set.

The GA defines an individual (a complete strategy) by 5 genes:

1. **RSI Calculation Period Length**: (e.g., 14 periods)
2. **Bollinger Bands Calculation Period Length**: (e.g., 20 periods)
3. **RSI Overbought Level**: (e.g., 70)
4. **RSI Oversold Level**: (e.g., 30)
5. **Exit Point**: (A mechanism, such as a percentage stop-loss/take-profit, to close the trade).

After numerous generations of mutation and crossover, the algorithm yields a list of optimized parameter sets that exhibit the best historical performance.

## How to Run This Project

To get this project running locally and begin the optimization process, follow these steps:

1. **Clone the Repository**:

```
git clone https://github.com/saurabhdhingra/geneticAlgoTrading.git
cd geneticAlgoTrading
```

2. **Set Up Environment (Recommended)**: Use a virtual environment to manage dependencies.

```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. **Install Dependencies**: Install the required Python packages (e.g., 'pandas', 'numpy', 'backtrader', 'ccxt', 'deap', etc.).

```
pip install -r requirements.txt
```

4. **Configure Binance API Keys**: The project requires access to historical market data via Binance. You must set up your API Key and Secret in the appropriate configuration file (likely a config.py or by using environment variables). Check the repository for specific instructions on key placement.

5. **Run the Optimization Script**: Execute the main script to start the Genetic Algorithm optimization process.

```
python main.py
```

The script will print the results of the backtesting for the best-performing individuals (parameter sets) found after the last generation.

## Tweaking Initial Population Parameters

The effectiveness of the Genetic Algorithm heavily depends on the initial search space defined by the parameter ranges. The GA's first step is to generate a random starting population of strategies by selecting values for the 5 genes within pre-defined bounds.

To adjust the search space, you must edit the section of the code (likely in 'main.py' or a dedicated configuration file like 'config.py') where the bounds for random value generation are set.

Here is an example of the typical ranges used for the 5 genes:

```
Gene (Parameter)	        Typical Use	                    Recommended Search Range

RSI Period Length	        Sensitivity to price changes	10 to 30 (Integers)
BB Period Length	        Length of the moving average	10 to 30 (Integers)
RSI Overbought Level	    Threshold for selling signal	60 to 80 (Floats/Integers)
RSI Oversold Level          Threshold for buying signal	    20 to 40 (Floats/Integers)
Exit Point	                Profit-taking / Stop-loss %	    0.005 to 0.05 (0.5% to 5.0%)
```

To modify the search space:

- **Wider Range**: Use a wider range (e.g., RSI Period: 7 to 40) to explore more possibilities, but this will increase the time needed for the GA to converge.

- **Narrower Range**: Use a narrower range (e.g., RSI Period: 12 to 16) if you already have an idea of the optimal values, speeding up the process.

**Note**: Always ensure the data types and bounds (e.g., integer vs. float, minimum/maximum values) match the requirements of your backtesting engine. Experimenting with these ranges is key to finding a globally optimal solution.
