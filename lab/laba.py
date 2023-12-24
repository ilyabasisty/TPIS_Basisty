class Solver:
    """! класс для решения диф. уровнений в частных производных методом прогонки"""
    alpha = []
    betta = []

    def __init__(self, fi1, fi2, eps, type, sigm, ps1=None, ps2=None, f=None) -> None:
        """! инициализация класса

        @param type тип граничного условия
        """
        self.fi1 = fi1
        self.fi2 = fi2
        self.eps = eps
        self.type = type
        self.sigm = sigm
        self.ps1 = ps1
        self.ps2 = ps2
        self.f = f

        if type[0] == 3 and ps1 is None:
            raise ValueError('необходима функция ps1')
        if type[1] == 3 and ps2 is None:
            raise ValueError('необходима функция ps2')
    
    def _eps_n(self, u, dt=None, t=None, x=None):
        """! Правая часть уравнения

        @param u значение сетки в определенной точке
        @param dt шаг по времени
        @param t время 
        @param x координата
        @return tmp число
        """
        tmp = u
        if self.f:
            try:
                tmp += dt * self.f(t, x)
            except:
                raise ValueError('Невозможно расчитать')
        return tmp

    def _find_alpha_betta(self, Nx, h, t):
        """! поиск значений из левого граничного условия

        @param Nx количество итераций по кординате х
        """
        if self.type[0] == 1:
            alpha = [0] * (Nx - 1)
            betta = [self.fi1(t) ] * (Nx - 1)
        if self.type[0] == 2:
            alpha = [1] * Nx
            betta = [ -h * self.fi1(t)] * (Nx - 1)
        if self.type[0] == 3:
            alpha = [1 / (1 + h * self.fi1(t))] * (Nx - 1)
            betta = [ -h * self.ps1(t) / (1 + h * self.fi1(t))] * (Nx - 1)
        return alpha, betta

    def _solve(self, dt, L, Tmax, h,):
        """! основная функции прогонки

        @param L длина
        @param Tmax время
        @return  2-х мерный массив сетки решений
        """
        Nx = int(L / h + 1)
        Nt = int(Tmax / dt + 1)
        U = [[0.0 for i in range(Nx)] for j in range(Nt)]

        for j in range (0, Nx):
            U[0][j] = self.eps(h * j)

        a= -self.sigm * dt/h**2
        b= 1 + 2 * self.sigm * dt/h**2
        c= -self.sigm * dt/h**2
        
        for n in range(0, Nt - 1):
            next_n = n + 1
            alpha, betta = self._find_alpha_betta(Nx, h, next_n * dt)
            
            for j in range(1, Nx - 1):
                betta[j] = (self._eps_n(U[n][j], dt, dt * n, h * j) - c * betta[j - 1]) / (b + c * alpha[j - 1])
                alpha[j] = -a / (b + c * alpha[j - 1])
            if self.type[1] == 1:
                U[next_n][-1] = self.fi2(dt * next_n)
            if self.type[1] == 2:
                U[next_n][-1] = (h * self.fi2(dt * next_n) + betta[-1]) / (1 - alpha[-1])
            if self.type[1] == 3:
                U[next_n][-1] = (h * self.ps2(dt * next_n) + betta[-1]) / (1 -alpha[-1] -h * self.fi2(dt * next_n))
            
            for j in range(Nx - 2, -1, -1):
                U[next_n][j] = alpha[j] * U[next_n][j + 1] + betta[j]
               
        return U
    

D = 10.0 ** -6    
sigm = D
L = 0.1
T  = 10000.0
Re = 8
Pr = 400
d = 10.0 * 10 ** -3
cs = 10.0
B = D * (1 + 1/2 * (0.55 * pow(Re, 1/2) * pow(Pr, 1/3))) / d
types = [1, 3]

def eps(x):
    return 200 + 50.0 * x
def fi1(x):
    return 200.0
def fi2(x):
    return -B / D
def ps2(x):
    return  B * cs / D




if __name__ == "__main__":
    solver = Solver(fi1, fi2, eps, types, sigm, ps2=ps2)
    print(*solver._solve(1000, L, T, 0.01), sep='\n')