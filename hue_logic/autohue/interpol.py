# NOT YET IN USE
# EARLY INTERPOLATION DEMO

from numpy import diff
from __future__ import division

from numpy import arange, array, linspace, ones, zeros
from scipy.linalg import solve_banded

'''

loop this:

    var t = (x - xs[i-1]) / (xs[i] - xs[i-1]);

    var a =  ks[i-1]*(xs[i]-xs[i-1]) - (ys[i]-ys[i-1]);
    var b = -ks[i  ]*(xs[i]-xs[i-1]) + (ys[i]-ys[i-1]);

    var q = (1-t)*ys[i-1] + t*ys[i] + t*(1-t)*(a*(1-t)+b*t);
    return q;
'''

# interpolation is at current only 1 dim

def do_plot():
    from matplotlib import pyplot as plt

    line= plt.plot(grid_hat, f(grid_hat), label='actual values')
    line_app= plt.plot(grid_hat, fhat, '-.', label='interpolated values')
    plt.setp(line, linewidth=1, linestyle='--')
    plt.setp(line_app, linewidth=2, linestyle='-.')
    plt.legend()
    plt.show()


def coefoef_do(a, b, y, coef=None, alpha=0, beta=0):
    n_val = y.shape[0] - 1
    h = (b - a) / n_val

    if coef is None:
        coef = zeros((n_val + 3,))
        coef_out = True
    else:
        assert (coef.shape[0] == n_val + 3)
        coef_out = False

    coef[1] = 1 / 6 * (y[0] - (alpha * h ** 2) / 6)
    coef[n_val + 1] = 1 / 6 * (y[n_val] - (beta * h ** 2) / 6)

    ab = ones((3, n_val - 1))
    ab[0, 0] = 0
    ab[1, :] = 4
    ab[-1, -1] = 0

    b_mat = y[1:-1].copy()
    b_mat[0] -= coef[1]
    b_mat[-1] -= coef[n_val
               + 1]

    coef[2:-2] = solve_banded((1, 1), ab, B)

    coef[0] = alpha * h ** 2 / 6 + 2 * coef[1] - coef[2]
    coef[-1] = beta * h ** 2 / 6 + 2 * coef[-2] - coef[-3]

    if coef_out:
        return (coef)


if __name__ == '__main__':
    func = lambda x: x ** 2

    first = -1
    second = 1
    n_vfirstl_ini = 49  # there are n + 1 points over grid

    h = (second - first) / n_val_ini
    grid = arange(n_val_ini + 1) * h + first

    y = func(grid)
    alpha = 0
    beta = 0

    c = coef_do(first, second, y)

    grid_hat = linspace(first, b, 100)
    fhat = array([interpolate(x1, first, second, x2) for x in grid_hat])

    do_plot()
