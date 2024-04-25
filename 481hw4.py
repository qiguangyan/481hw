def github() -> str:
    """
    github link
    """

    return "https://github.com/qiguangyan/481hw/blob/main/481hw4.py"


import pandas as pd

def load_data() -> pd.DataFrame:
    """
    Loads the Tesla stock price history

    Returns:
        pd.DataFrame: A DataFrame containing the stock price history
    """
    return pd.read_csv('https://lukashager.netlify.app/econ-481/data/TSLA.csv')

import matplotlib.pyplot as plt

def plot_close(df: pd.DataFrame, start: str = '2010-06-29', end: str = '2024-04-15') -> None:
    """
    Plot the closing price of Tesla stock between optional start and end dates
    
    Parameters:
        df (pd.DataFrame): DataFrame containing Tesla stock price data
        start (str): Start date for the plot, default '2010-06-29'
        end (str): End date for the plot, default '2024-04-15'

    """

    filtered_df = df.loc[(df['Date'] >= start) & (df['Date'] <= end)]

    # Plotting the data
    plt.plot(filtered_df['Date'], filtered_df['Close'], label='Close Price')
    plt.title(f'Tesla Stock Closing Prices from {start} to {end}')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend()
    plt.show()

import numpy as np
import statsmodels.api as sm


def autoregress(df: pd.DataFrame) -> float:
    """
    Calculate the t-statistics
    """
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    df['Delta_x'] = df['Close'].diff()
    df = df.dropna()
    df['Delta_x_lagged'] = df['Delta_x'].shift(1)
    df = df.dropna()

    X = df['Delta_x_lagged']
    y = df['Delta_x']
    X = sm.add_constant(X, has_constant='add')
    model = sm.OLS(y, X, hasconst=False)
    results = model.fit(cov_type='HC1')

    t_stat = results.tvalues[0]
    return t_stat


def autoregress_logit(df: pd.DataFrame) -> float:
    """
    Calculate the t-statistics
    """
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    df['Delta_x'] = df['Close'].diff()
    df = df.dropna()
    df['Delta_x_lagged'] = df['Delta_x'].shift(1)
    df = df.dropna()
    df['Positive_change'] = (df['Delta_x'] > 0).astype(int)

    X = df['Delta_x_lagged']
    y = df['Positive_change']
    X = sm.add_constant(X, prepend=False)  # add a column of ones for the intercept
    model = sm.Logit(y, X)
    results = model.fit(disp=0)  # disp=0 turns off the summary output when fitting

    t_stat = results.tvalues['Delta_x_lagged']
    return t_stat



def plot_delta(df: pd.DataFrame) -> None:
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    df['Delta_x'] = df['Close'].diff()

    plt.plot(df['Date'], df['Delta_x'], label='Change in Closing Price (delta x_t)')
    plt.title('Daily Change in Tesla Stock Closing Prices')
    plt.xlabel('Date')
    plt.ylabel('Change in Closing Price')
    plt.legend()
    plt.show()
