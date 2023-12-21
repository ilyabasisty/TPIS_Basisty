import pytest

from lab.laba import Solver


@pytest.fixture(scope='session')
def solver():
    D = 10.0 ** -6    
    sigm = D
    L = 0.1
    T  = 10000.0
    Re = 8
    Pr = 400
    d = 10.0 * 10 ** -3
    cs = 10.0
    B = D * (1 + 1/2 * (0.55 * pow(Re, 1/2) * pow(Pr, 1/3))) / d
    type = ['1 рода', '3 рода']
    def eps(x):
        return 200 + 50.0 * x
    def fi1(x):
        return 200.0

    def fi2(x):
        return -B / D

    def ps2(x):
        return  B * cs / D

    solver = Solver(fi1, fi2, eps, type, sigm, ps2=ps2)

    return solver