import numpy as np
import matplotlib.pyplot as plt


class Market:
    def __init__(self,mu,sigma,p0):
        self.mu = mu
        self.sigma = sigma
        self.p0 = p0

    def generate_prices(self,seed=0):
        np.random.seed(seed)
        returns = np.random.normal(loc=self.mu, scale=self.sigma, size=100)
        price = self.p0*(1+returns).cumprod()
        return price