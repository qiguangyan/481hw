def github() -> str:
    """
    
    returns:
        str: github link
    """

    return "https://github.com/qiguangyan/481hw/blob/main/481hw2.py"

import numpy as np

def simulate_data(seed: int = 481) -> tuple:
    """
    Generates 1000 simulated observations from
    y_i = 5 + 3 x_{i1} + 2 x_{i2} + 6 x_{i3} + epsilon_i
    where x_{i1}, x_{i2}, x_{i3} from N(0, 2) and epsilon_i from N(0, 1)
    
    parameters:
    seed (int): seed for rng (default 481).
    
    returns:
    tuple: 
    y (np.array): (1000, 1) y_i
    X (np.array): (1000, 3) x_{i1}, x_{i2}, x_{i3}
    """
    
    np.random.seed(seed)
    X = np.random.normal(0, np.sqrt(2), size=(1000, 3))
    epsilon = np.random.standard_normal(1000)
    y = 5 + 3 * X[:, 0] + 2 * X[:, 1] + 6 * X[:, 2] + epsilon
    
    return y.reshape(1000, -1), X

from scipy.optimize import minimize

def mle_func(beta, X, y):
    """
    objective funciton for MLE
    """
    return 0.5 * np.sum((y - (X @ beta)) ** 2)

def estimate_mle(y: np.array, X: np.array) -> np.array:
    """
    estimates the MLE parameters
    
    Parameters:
    y (np.array): y
    X (np.array): x_{i1}, x_{i2}, x_{i3}
    
    Returns:
    np.array: estimated coefficients beta_0, beta_1, beta_2, beta_3
    """
    X_inters = np.hstack([np.ones((1000, 1)), X])
    result = minimize(mle_func, np.zeros(4), args=(X_inters, y.flatten()), method = 'Nelder-Mead')
    return result.x.reshape(4, 1)

def ols_func(beta, X, y):
    """
    objective function for OLS
    """
    return np.sum((y - X @ beta) ** 2)

def estimate_ols(y: np.array, X: np.array) -> np.array:
    """
    estimates the OLS parameters
    
    Parameters:
    y (np.array): y
    X (np.array): x_{i1}, x_{i2}, x_{i3}
    
    Returns:
    np.array: estimated coefficients beta_0, beta_1, beta_2, beta_3
    """
    X_inters = np.hstack([np.ones((1000, 1)), X])
    result = minimize(ols_func, np.zeros(4), args=(X_inters, y.flatten()), method = 'Nelder-Mead')
    return result.x.reshape(4, 1)