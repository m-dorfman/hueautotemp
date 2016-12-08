# NOT YET IN USE
# EARLY INTERPOLATION DEMO


from __future__ import division

from numpy import arange, array, linspace, ones, zeros
from scipy.linalg import solve_banded

import fast_cubic_spline as _spline

def do_plot():
    from matplotlib import pyplot as plt

    line_actual = plt.plot(grid_hat, f(grid_hat), label='actual')
    line_approx = plt.plot(grid_hat, fhat, '-.', label='interpolated')
    plt.setp(line_actual, linewidth=1, linestyle='--')
    plt.setp(line_approx, linewidth=2, linestyle='-.')
    plt.legend()
    plt.show()

def coef_do(a, b, y, c=None, alpha=0, beta=0):
    n_val = y.shape[0] - 1
    h = (b - a) / n_val

    if c is None:
        c = zeros((n_val + 3,))
        ifreturn = True
    else:
        assert (c.shape[0] == n_val + 3)
        ifreturn = False

    c[1] = 1 / 6 * (y[0] - (alpha * h ** 2) / 6)
    c[n_val + 1] = 1 / 6 * (y[n_val] - (beta * h ** 2) / 6)

    # ab matrix here is just compressed banded matrix
    ab = ones((3, n_val - 1))
    ab[0, 0] = 0
    ab[1, :] = 4
    ab[-1, -1] = 0

    B = y[1:-1].copy()
    B[0] -= c[1]
    B[-1] -= c[n_val
               + 1]

    c[2:-2] = solve_banded((1, 1), ab, B)

    c[0] = alpha * h ** 2 / 6 + 2 * c[1] - c[2]
    c[-1] = beta * h ** 2 / 6 + 2 * c[-2] - c[-3]

    if ifreturn:
        return (c)


# aliases
interpolate = _spline.interpolate
interpolate_2d = _spline.interpolate_2d

if __name__ == '__main__':
    #single dim interpol
    f = lambda x: x ** 2

    a = -1
    b = 1
    n_val_ini = 49  # there are n + 1 grid points (0,..., n)

    h = (b - a) / n_val_ini
    grid = arange(n_val_ini + 1) * h + a

    y = f(grid)
    alpha = 0
    beta = 0

    c = coef_do(a, b, y)

    grid_hat = linspace(a, b, 100)
    fhat = array([interpolate(x, a, b, c) for x in grid_hat])

    do_plot()
