import numpy as np
from Node import Node

"""Equity option pricer"""


class BinomialTreePricer():
    def __init__(self, put_call, long_short, american_european, time_to_maturity, volatility, risk_free_rate, spot_price, strike_price, dividend_yield, n_levels=10):
        self.put_call = put_call
        self.long_short = long_short
        self.american_european = american_european
        self.n_levels = n_levels
        self.volatility = volatility
        self.timestep = time_to_maturity / n_levels
        self.risk_free_rate = risk_free_rate
        self.spot_price = spot_price
        self.strike_price = strike_price
        self.dividend_yield = dividend_yield
        self.u = np.exp(volatility * np.sqrt(self.timestep))
        self.d = np.exp((-1) * volatility * np.sqrt(self.timestep))
        self.a = np.exp((risk_free_rate - dividend_yield) * self.timestep)
        self.p = (self.a - self.d)/(self.u - self.d)
        self.root = self.buildTree(0, spot_price)

    def buildTree(self, level, spot_price):
        root = Node(spot_price)
        if (level < self.n_levels):
            root.up = self.buildTree(level + 1, self.u * spot_price)
            root.down = self.buildTree(level + 1, self.d * spot_price)
        return root

    def price(self):
        if (self.long_short == 'long'):
            mul = 1
        else:
            mul = -1
        return mul * self._price_node(self.root)

    def _price_node(self, node):
        if (node.up is None):
            return self._option_value(self.put_call, node)
        else:
            option_value = np.exp(-(self.risk_free_rate - self.dividend_yield) * self.timestep) * (self.p * self._price_node(node.up) + (1 - self.p) * self._price_node(node.down))
            if (self.american_european == 'american'):
                option_value_alt = self._option_value(self.put_call, node)
            else:
                option_value_alt = option_value

            if (self.put_call == 'put'):
                return max(option_value, option_value_alt)
            else:
                return min(option_value, option_value_alt)

    def _option_value(self, put_call, node):
        if (self.put_call == 'put'):
            option_value = max(self.strike_price - node.spot_price, 0)
        else:
            option_value = max(node.spot_price - self.strike_price, 0)
        return option_value


# (put_call, long_short, american_european, time_to_maturity, volatility, risk_free_rate, spot_price, strike_price, dividend_yield, n_levels=10):
a = BinomialTreePricer('put', 'long', 'american', 2, 0.3, 0.05, 50, 52, 0.0, n_levels=10)
print(a.price())
print('Strike price: %.4f' % a.strike_price)
print('Discount factor per step: %.4f' % np.exp(-(a.risk_free_rate - a.dividend_yield) * a.timestep))
print('Time step: %.4f' % a.timestep)
print('Growth factor per step: %.4f' % a.a)
print('Probability of up move: %.4f' % a.p)
print('Up step size: %.4f' % a.u)
print('Down step size: %.4f' % a.d)
