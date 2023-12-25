import math

class Solver:
    """! класс для решения диф. уровнений в частных производных методом прогонки"""
    alpha = []
    betta = []
    U = None
    a = None
    b = None
    c = None
    Nx = None
    Nt = None

    def __init__(self, fi1, fi2, eps, ps1=None, ps2=None, f=None, k=0) -> None:
        """! инициализация класса

        @param type тип граничного условия
        """
        self.solver_type = FirstSolver

        self.fi1 = fi1
        self.fi2 = fi2
        self.eps = eps
        self.type = self.solver_type.type
        self.ps1 = ps1
        self.ps2 = ps2
        self.f = f
        self.k = k


        if type[0] == 3 and ps1 is None:
            raise ValueError('необходима функция ps1')
        if type[1] == 3 and ps2 is None:
            raise ValueError('необходима функция ps2')
        
    
    def set_solver_type(self, solver):
        self.solver_type = solver
        self.type = self.solver_type.type


    def _init_a_b_c(self, dt, h):
        self.a, self.b, self.c = self.solver_type._init_a_b_c(self.solver_type.sigm, dt, h, self.k)
    
    def _finde_alpha_betta(self, Nx, h, t):
        """! поиск значений из левого граничного условия

        @param Nx количтво тераций по кординате х
        """
        
        if self.type[0] == 1:
            self.alpha = [0] * (Nx - 1)
            self.betta = [self.fi1(t) ] * (Nx - 1)
        if self.type[0] == 2:
            self.alpha = [1] * Nx
            self.betta = [ -h * self.fi1(t)] * (Nx - 1)
        if self.type[0] == 3:
            self.alpha = [1 / (1 + h * self.fi1(t))] * (Nx - 1)
            self.betta = [ -h * self.ps1(t) / (1 + h * self.fi1(t))] * (Nx - 1)

    def _execute(self, dt, h):
        """! расчет сетки

        """
        for n in range(0, self.Nt - 1):
            next_n = n + 1
            self._finde_alpha_betta(self.Nx, h, next_n * dt)
            
            for j in range(1, self.Nx - 1):
                self.betta[j] = (self._eps_n(self.U[n][j], dt, h, n, j) - self.c * self.betta[j - 1]) / (self.b + self.c * self.alpha[j - 1])
                self.alpha[j] = -self.a / (self.b + self.c * self.alpha[j - 1])
                 
            if self.type[1] == 1:
                self.U[next_n][-1] = self.fi2(dt * next_n)
            if self.type[1] == 2:
                self.U[next_n][-1] = (h * self.fi2(dt * next_n) + self.betta[-1]) / (1 - self.alpha[-1])
            if self.type[1] == 3:
                self.U[next_n][-1] = (h * self.ps2(dt * next_n) + self.betta[-1]) / (1 -self.alpha[-1] -h * self.fi2(dt * next_n))
            for j in range(self.Nx - 2, -1, -1):
                self.U[next_n][j] = self.alpha[j] * self.U[next_n][j + 1] + self.betta[j]

    def _prepare_data(self, dt, L, Tmax, h):
        """! подготовка данных

        """
        self.Nx = int(L / h + 1)
        self.Nt = int(Tmax / dt + 1)
        self.U = [[0.0 for i in range(self.Nx)] for j in range(self.Nt)]

        for j in range (0, self.Nx):
            self.U[0][j] = self.eps(h * j)

    def _eps_n(self, u, dt=None, h=None, n=None, j=None):
        """! Правая часть уравнения

        @param u значение сетки в определенной точке
        @param dt шаг по времени
        @param t время 
        @param x координата

        @return  число
        """
        return self.solver_type._eps_n(self.f, u, dt, h, n, j)


    def _validate_data(self, dt, h, Tmax, L):
        """! проверка данных
        """
        if dt < 0:
            raise ValueError('Значение не может быть отрицательным')
        if h < 0:
            raise ValueError('Значение не может быть отрицательным')
        if Tmax < 0:
            raise ValueError('Значение не может быть отрицательным')
        if L < 0:
            raise ValueError('Значение не может быть отрицательным')

    def _solve(self, dt, L, Tmax, h,):
        """! основная функции прогонки 

        @param L длина
        @param Tmax время

        @return  2 мерный массив сетки решений
        """
        self._validate_data(dt, h, Tmax, L)
        self._prepare_data(dt, L, Tmax, h)
        self._init_a_b_c(dt, h)
        self._execute(dt, h)
               
        return self.U


class FirstSolver:

    type = [1, 3]
    sigm = 10.0 ** -6

    def _init_a_b_c(sigm, dt, h, k):
        return -sigm * dt/h**2, 1 + 2 * sigm * dt/h**2 + k * dt, -sigm * dt/h**2

    def _eps_n(f, u, dt=None, h=None, n=None, j=None):
        x = h * j
        t = dt * n
        tmp = u
        if f:
            try:
                tmp += dt * f(t, x)
            except:
                raise ValueError('Невозможно расчитать')
        return tmp
    

class SecondSolver:

    type = [1, 1]
    sigm = 4.5 / 100

    def _init_a_b_c(sigm, dt, h, k):
        q = pow(math.pi, 1 / 2) * 0.5 * pow(dt, 1/2)
        return -q * sigm / h ** 2, 1 + 2 * q * sigm / h ** 2,  -q * sigm / h ** 2


    def _eps_n(f, u, dt=None, h=None, n=None, j=None):
        x = h * j
        t = dt * n
        q = pow(math.pi, 1/2) * 0.5 * pow(dt, 1/2)
        tmp = u * 0.5
        if f:
            try:
                tmp += q * f(dt, n, x)
            except:
                raise ValueError('Невозможно расчитать')
        return tmp


if __name__ == "__main__":
    D = 10.0 ** -6    
    L = 0.1
    T  = 10000.0
    Re = 8
    Pr = 400
    d = 10.0 * 10 ** -3
    cs = 10.0
    B = D * (1 + 1/2 * (0.55 * pow(Re, 1/2) * pow(Pr, 1/3))) / d

    def eps(x):
        return 200 + 50.0 * x
    def fi1(x):
        return 200.0
    def fi2(x):
        return -B / D
    def ps2(x):
        return  B * cs / D

    solver = Solver(fi1, fi2, eps, ps2=ps2)
    solver.set_solver_type(FirstSolver)
    U = solver._solve(1000, L, T, 0.01)
    # print(*U, sep='\n')

    print('\n\n------------------------------------------------------------\n\n')

    k = 4.5
    D = k / 100

    def eps(t):
        return 0
    def fi1(t):
        return 0
    def fi2(t):
        return k * t ** 2
    def f(dt, n, x):
        return k * ((x) ** 2 * pow(dt, 3/2) / pow(math.pi, 1/2) * ((n + 2) ** 2 - 4/3) - 2 * D *(n * dt) ** 2) 

    L = 1
    T = 1
    solver = Solver(fi1, fi2, eps, f=f)
    solver.set_solver_type(SecondSolver)
    U = solver._solve(0.01, L, T, 0.1)
    # print(*U, sep='\n')

# if __name__ == "__main__":
#     solver = Solver(fi1, fi2, eps, types, sigm, ps2=ps2)
#     print(*solver._solve(1000, L, T, 0.01), sep='\n')