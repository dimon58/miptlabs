import scipy.fftpack
import scipy.fftpack
import scipy.optimize
import scipy.optimize

from .base import Approximator, MultiLinearMixin

"""
Модуль содержаший базовые апроксиматоры
"""

from statsmodels.nonparametric.smoothers_lowess import lowess

import numpy as np
import scipy.fftpack
import scipy.optimize


class Lowess(MultiLinearMixin, Approximator):
    """
    Реализует алгоритм lowess.
    Предоставляет общий и гибкий подход для приближения двумерных данных.
    Подробнее http://www.machinelearning.ru/wiki/index.php?title=%D0%90%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC_LOWESS
    Для некоторых наборов данных оченб хорошо апроксимирует кривую
    """

    def __init__(self, frac=0.35, points=100, left_offset=5, right_offset=5):
        """

        :param frac: Параметр f указывает, какая доля (fraction) данных используется в процедуре. Если f = 0.5, то только половина данных используется для оценки и влияет на результат, и тогда мы получим умеренное сглаживание. С другой стороны, если f = 0.8, то используются восемьдесят процентов данных, и сглаживание намного сильнее. Во всех случаях веса данных тем больше, чем они ближе к объекту t.
Процедура оценки использует не метод наименьших квадратов, а более устойчивый ( робастный ) метод, который принимает меры против выбросов.
        :param points: количество точек, которые будут на выходе
        :param left_offset: отступ от левой гриницы диапозона
        :param right_offset: отступ от правой гриницы диапозона
        """
        super(Lowess, self).__init__(points, left_offset, right_offset)
        self.frac = frac

    def approximate(self, x, y, xerr=0, yerr=0):
        x, y, xerr, yerr = self._prepare_before_approximation(x, y, xerr, yerr)

        # Нечто
        result = lowess(y, x, frac=self.frac)

        self._res_x = result[:, 0]
        self._res_y = result[:, 1]

        return self._res_x, self._res_y


class Fourier(MultiLinearMixin, Approximator):
    """
    # WIP #
    Апроксимация функции с помощью преобразования фурье
    """

    def approximate(self, x, y, xerr=0, yerr=0):
        x, y, xerr, yerr = self._prepare_before_approximation(x, y, xerr, yerr)

        # Fourier
        x = np.array(x)
        y = np.array(y)
        w = scipy.fftpack.rfft(y)
        # f = scipy.fftpack.rfftfreq(10000, x[1] - x[0])
        spectrum = w ** 2
        cutoff_idx = spectrum < (spectrum.max() / 20)
        w2 = w.copy()
        w2[cutoff_idx] = 0
        y = scipy.fftpack.irfft(w2)

        self._res_x = x
        self._res_y = y

        return x, y
