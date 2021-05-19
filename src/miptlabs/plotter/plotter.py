import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure


class NothingDrawError(Exception):
    def __init__(self, text):
        self.txt = text


def _set_ticks_fontsize(axes, xfontsize, yfontsize):
    """
    Устанавливает размер шрифта подписям по осям
    :param axes: объект графика
    :param xfontsize: размер шрифта по оси x
    :param yfontsize: размер шрифта по оси y
    :return: None
    """
    for item in axes.get_xticklabels():
        item.set_fontsize(xfontsize)

    for item in axes.get_yticklabels():
        item.set_fontsize(yfontsize)


def _get_default_params():
    """
    Генерирует значения размеров шрифта по умолчанию
    :return:
    """
    params = dict()

    params['figsize'] = (10, 8)
    params['dpi'] = 100

    params['legend_loc'] = 'best'

    params['xticks_fontsize'] = 16
    params['yticks_fontsize'] = 16
    params['xlabel_fontsize'] = 22
    params['ylabel_fontsize'] = 22
    params['legend_fontsize'] = 20
    params['title_fontsize'] = 26

    return params


def _update_params(params, kwargs):
    """
    Обновляет значения параметров построения графика с учётом переданных дополнитеьных параметров
    :param params:
    :param kwargs:
    :return:
    """

    targets = ('figsize', 'dpi', 'legend_loc',
               'xticks_fontsize', 'yticks_fontsize',
               'xlabel_fontsize', 'ylabel_fontsize',
               'legend_fontsize', 'title_fontsize')

    for target in targets:
        if target in kwargs:
            params[target] = kwargs.pop(target)

    if kwargs:
        print(f'Лишние аргументы', kwargs)


def _get_default_color(i=0):
    """
    :return: первый цвет в цикле цветов matplotlib, точнее тускло-синий
    """
    return plt.rcParams['axes.prop_cycle'].by_key()['color'][i % 10]


def _enable_minor_ticks(axes):
    """
    Включает побочную сетку на графике
    :param axes:
    :return:
    """
    axes.minorticks_on()
    axes.grid(which='major', color='k', linewidth=0.8)
    axes.grid(which='minor', color='k', linestyle=':')


def pretty_plot(x, y, xerr=None, yerr=None,
                xlabel=None, ylabel=None, title=None, legend=None,
                minot_ticks=True, color=None, points=True, line=False,
                axes=None, **kwargs):
    """
    Рисует график, с требованиями лабников.
    По умолчания не соединяет точки
    TODO: пока не умеет выносить степень. в будущем это появится.
    TODO: может поменяться интерфейс
    для отображения можно искользовать:
    matplotlib.pyplot.show(), или pretty_plot(...).figure.show(), или show(), определнный ниже
    для сохранения можно использовать:
    matplotlib.pyplot.savefig(filename), или pretty_plot(...).figure.savefig(filename), или savefig(fig, filename), определнный ниже
    :param x: координаты по оси x
    :param y: координаты по оси y
    :param xerr: погрешности по оси x. Либо одно число (применится к все точкам), либо список (применится к соответсвующей точке).
    :param yerr: погрешности по оси y. Либо одно число (применится к все точкам), либо список (применится к соответсвующей точке).
    :param xlabel: подпись по оси x
    :param ylabel: подпись по оси y
    :param title: название графика
    :param legend: легенда
    :param minot_ticks: нужна ли впсомогательная сетка
    :param color: цвет графика. Если None, то будет синий
    :param points: нужно ли рисвоать точки
    :param line: нужно ли соединить ломаной все точки
    :param axes: объект графика. Можно ппередать, чтобы дорисовать всё на существующем графике
    :param kwargs: дополнительные агрменты:
    :Keyword Arguments:
    * *figsize* (``tuple[int]``) --
      размер графика в дюймах, по умолчанию 10 на 8
    * *dpi* (``int``) --
      количество пикселей на дюйм, по умолчанию 100
    * *legend_loc* (``str``) --
      положение легенды (см. документацию matplotlib), по умолчанию best
    * *xticks_fontsize* (``int``) --
      размер шрифта подписей оси x, по умолчанию 16
    * *yticks_fontsize* (``int``) --
      размер шрифта подписей оси y, по умолчанию 16
    * *xlabel_fontsize* (``int``) --
      размер шрифта обозначения оси x, по умолчанию 22
    * *ylabel_fontsize* (``int``) --
      размер шрифта обозначения оси y, по умолчанию 22
    * *title_fontsize* (``int``) --
      размер шрифта заголовка, по умолчанию 26
    * *legend_fontsize* (``int``) --
      размер шрифта легенды, по умолчанию 22
    :return: объект только что нарисованного графика
    """

    if not points and not line and not xerr and not yerr:
        raise NothingDrawError("Хотябы один из параметров points, line, xerr, yerr должен быть True,"
                               " чтобы что-то нарисовалось")

    # ----------------Инициализация----------------

    # Инициализирует параметры
    params = _get_default_params()

    # Обновляет параметры
    _update_params(params, kwargs)

    # Устанавливает стандартный цвет, если не передан другой
    if color is None:
        color = _get_default_color()

    # Создаёт новые объект графика и фигуры, если не переданы существующие
    if axes is None:
        figure, axes = plt.subplots(figsize=params['figsize'], dpi=params['dpi'])
        axes: Axes = axes
        if minot_ticks:
            _enable_minor_ticks(axes)

    # ----------------Рисование----------------

    # Нужно для костыля, чтобы легенда отрисовыволась лишь один раз
    label = legend

    # Рисует точки, если нужно
    if points:
        axes.scatter(x, y, c=color, label=label)
        label = None

    # Рисует кресты погрешностей, если нужно
    if xerr or yerr:
        axes.errorbar(x, y, fmt='none', xerr=xerr, yerr=yerr, c=color, label=label)
        label = None

    # Соединяет точки ломаной, если нужно
    if line:
        axes.plot(x, y, c=color, label=label)
        label = None

    # ----------------Шрифты----------------

    # Устанавливает размер шрифта для подписей по осям
    _set_ticks_fontsize(axes, params['xticks_fontsize'], params['yticks_fontsize'])

    # Устанавливает размер шрифта для разных элементов
    axes.set_xlabel(xlabel, fontsize=params['xlabel_fontsize'])
    axes.set_ylabel(ylabel, fontsize=params['ylabel_fontsize'])
    axes.set_title(title, fontsize=params['title_fontsize'])

    # Рисует легенду, если нужно
    if legend:
        axes.legend(loc='best', fontsize=params['legend_fontsize'])

    return axes


def pretty_plot_many(xs, ys, xerrs=None, yerrs=None,
                     xlabel=None, ylabel=None, title=None, legends=None,
                     minot_ticks=True, colors=None, points=True, line=False,
                     axes=None, **kwargs):
    r"""
    :param xs: наборы координат по оси x
    :param ys: наборы координат по оси y
    :param xerrs: наборы погрешностей по оси x.
    Либо одно число (применится к все точкам), либо список (применится к соответсвующей точке).
    :param yerrs: наборы погрешностей по оси y.
    Либо одно число (применится к все точкам), либо список (применится к соответсвующей точке).
    :param xlabel: наборы подписей по оси x
    :param ylabel: наборы подписей по оси y
    :param title: название графика
    :param legends: легенды
    :param minot_ticks: нужна ли впсомогательная сетка
    :param colors: наборы цветов графика. Если None, то будет синий
    :param points: нужно ли рисвоать точки
    :param line: нужно ли соединить ломаной все точки
    :param axes: объект графика. Можно ппередать, чтобы дорисовать всё на существующем графике
    :param kwargs: дополнительные агрменты:
    :Keyword Arguments:
    * *figsize* (``tuple[int]``) --
      размер графика в дюймах, по умолчанию 10 на 8
    * *dpi* (``int``) --
      количество пикселей на дюйм, по умолчанию 100
    * *legend_loc* (``str``) --
      положение легенды (см. документацию matplotlib), по умолчанию best
    * *xticks_fontsize* (``int``) --
      размер шрифта подписей оси x, по умолчанию 16
    * *yticks_fontsize* (``int``) --
      размер шрифта подписей оси y, по умолчанию 16
    * *xlabel_fontsize* (``int``) --
      размер шрифта обозначения оси x, по умолчанию 22
    * *ylabel_fontsize* (``int``) --
      размер шрифта обозначения оси y, по умолчанию 22
    * *title_fontsize* (``int``) --
      размер шрифта заголовка, по умолчанию 26
    * *legend_fontsize* (``int``) --
      размер шрифта легенды, по умолчанию 22
    :return: объект только что нарисованного графика
    """

    # ----------------Инициализация----------------

    # Инициализирует параметры
    params = _get_default_params()

    # Обновляет параметры
    _update_params(params, kwargs)

    # Создаёт новые объект графика и фигуры, если не переданы существующие
    if axes is None:
        figure, axes = plt.subplots(figsize=params['figsize'], dpi=params['dpi'])

        if minot_ticks:
            _enable_minor_ticks(axes)

    # Создаём кортежы из None длины = количеству графиков

    if legends is None:
        legends = tuple([None] * len(xs))

    if colors is None:
        colors = tuple([None] * len(xs))

    if xerrs is None:
        xerrs = tuple([None] * len(xs))

    if yerrs is None:
        yerrs = tuple([None] * len(xs))

    # ----------------Рисование----------------

    for num, (x, y, xerr, yerr, legend, color) in enumerate(zip(xs, ys, xerrs, yerrs, legends, colors)):

        # Устанавливает стандартный цвет, если не передан другой
        if color is None:
            color = _get_default_color(num)

        # Рисует точки, если нужно
        if points:
            axes.scatter(x, y, c=color, label=legend)

        # Рисует кресты погрешностей
        axes.errorbar(x, y, fmt='none', xerr=xerr, yerr=yerr, c=color)

        # Соединяет точки ломаной, если нужно
        if line:
            axes.plot(x, y, c=color)

    # ----------------Шрифты----------------

    # Устанавливает размер шрифта для подписей по осям
    _set_ticks_fontsize(axes, params['xticks_fontsize'], params['yticks_fontsize'])

    # Устанавливает размер шрифта для разных элементов
    axes.set_xlabel(xlabel, fontsize=params['xlabel_fontsize'])
    axes.set_ylabel(ylabel, fontsize=params['ylabel_fontsize'])
    axes.set_title(title, fontsize=params['title_fontsize'])

    # Рисует легенду, если нужно
    if legends:
        axes.legend(loc='best', fontsize=params['legend_fontsize'], )

    return axes


def show(*args, **kwargs):
    """
    Рисует все сгенерированные графики. По-сути обертка над matplotlib.pyplot.show
    :param args:
    :param kwargs:
    :return:
    """
    return plt.show(*args, **kwargs)


def savefig(obj, filename, *, transparent=None, **kwargs):
    """
    Сохраняет фигуру. По-сути обертка над встроенной функцие сохранения
    :param obj:
    :param filename:
    :param transparent:
    :param kwargs:
    :return:
    """
    figure = obj if isinstance(obj, Figure) else obj.figure

    figure.savefig(filename, transparent=transparent, **kwargs)
