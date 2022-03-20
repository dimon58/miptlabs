[![Documentation Status](https://readthedocs.org/projects/miptlabs/badge/?version=latest)](https://miptlabs.readthedocs.io/ru/latest/?badge=latest)


# Длинное описание, которое когда-то появится #

Для сборки:

```sh
python -m pip install --upgrade build wheel twine
python -m pip install -r requirements.txt
python -m build --no-isolation
twine upload dist/*
```

Для установки:

`pip install -i https://test.pypi.org/simple/ miptlabs`

Чтобы нарисовать что-то:

```
from miptlabs.plotter import pretty_plot, show
from numpy import linspace

# точки для построения графика
x = linspace(0, 5, 20) 
y = x * x

pretty_plot(x, y)
show()
```

![base_graph](examples/base.png)

Точки можно просто соединить написав line=True:

```
pretty_plot(x, y, line=True, legend='$y = x^2$')
```

![with_line_graph](examples/with_line.png)

Так как для данный с лаб простое соединение вряд ли подойдет, то в пакете есть разные апроксиматоры Для примера можно
взять зависимость координаты от рвемени при равноускоренном движении

```
from src.miptlabs.plotter import pretty_plot, show
from src.miptlabs.approximators import Polynomial
from numpy import linspace
import numpy as np


# точки для построения графика
x = linspace(0, 5, 20)
y = x * x + np.random.normal(size=x.shape)
ax = pretty_plot(x, y, legend='$x = t^2$ + random')


# Апроксимация
approximator = Polynomial(deg=2)
appr_x, appr_y = approximator.approximate(x, y)
# Вывод формулы для латеха
print(approximator.label('t', 'x'))
# >>> $y = 1.03t^{2}-0.205t+0.158$

№ Построение графика. Параметры говорят сами за себя
pretty_plot(appr_x, appr_y, axes=ax, points=False, line=True,
            legend=approximator.label('t', 'x'), xlabel='t, сек', ylabel='x, м', title='График $x(t)$')

ax.figure.savefig('examples/approx.png')
show()
```

![approx_graph](examples/approx.png)


