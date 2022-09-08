import numpy as np

class Pool:
    def __init__(self,
                address,
                token0,
                token1,
                reserves0=None,
                reserves1=None,
                fee = 0.003):
        self.fee = fee
        self.gamma = 1-self.fee
        self.address = address
        self.token0 = token0
        self.token1 = token1
        self._reserves(reserves0,reserves1)
        self.priceAB()

    def _reserves(self,reserves0,reserves1):
        self.r0 = reserves0
        self.r1 = reserves1

    def priceAB(self):
        return self.r1 / self.r0

    def execute_trade(self,swap_transaction):
        r0 = self.r0
        r1 = self.r1
        amountOut = - (r0 * r1) / (r0 + amountIn * self.gamma) + r1
        self.r0 += amountIn
        self.r1 -= amountOut
    def _update(self,amountIn):
        r0 = self.r0
        r1 = self.r1
        amountOut = - (r0 * r1) / (r0 + amountIn * self.gamma) + r1
        self.r0 += amountIn
        self.r1 -= amountOut
    def _update_inverse(self,amountIn):
        r0 = self.r0
        r1 = self.r1
        amountOut = - (r0 * r1) / (r1 + amountIn * self.gamma) + r0
        self.r0 -= amountOut
        self.r1 += amountIn
    def max_arb(self,m_priceAB):
        r0 = self.r0
        r1 = self.r1
        gamma = self.gamma
        pAB = self.priceAB()
        if pAB > m_priceAB:
            p = 1 / m_priceAB
            arb_qt = (-gamma*r0 + np.sqrt(gamma**3*p*r0*r1))/gamma**2
            profits = p * (- (r0 * r1) / (r0 + arb_qt * self.gamma) + r1)-arb_qt
            self._update(arb_qt)
        else:
            p = m_priceAB
            arb_qt = (-gamma*p*r1 + np.sqrt(gamma**3*p**3*r0*r1))/(gamma**2*p**2)
            profits = (- (r0 * r1) / (r0 + arb_qt * self.gamma) + r1)-arb_qt
            self._update_inverse(p * arb_qt)
        if profits <0:
            arb_qt = 0
            profits = 0

        return arb_qt, profits

