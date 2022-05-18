def represent_value(name, val=None, sigma=None, eps=None, units='', n=-1):
    r"""
    Форматирует значение величины для лабы в формат

    Если есть погрешности: $ name = val \\pm sigma [units], \\; \\varepsilon_{name} = eps \\% $

    Иначе: $ name = val \\pm [units] $

    :param name: Название величины
    :param val: Значение величины
    :param sigma: Абсолютная величины
    :param eps: Относительная величины
    :param units: единицы измерения
    :param n: число знаков округления, если -1, то округления нет
    :return: представление величины в формате latex для копипаста в текст лабы
    """
    # Проверка, что не все значения None
    if val is None and sigma is None and eps is None:
        raise ValueError(f'У величины {name} не переданы никакие значения')

    # Проверка, что если все не None, то выполняется тождество  val * eps == sigma
    if val is not None and sigma is not None and eps is not None and val * eps != sigma:
        raise ValueError(f'У величины {name} переданы некорректные значения')

    if units:
        units = f' \\; {units}'

    # Проверка, что есть пара не None
    if sigma is None and eps is None:
        print(f'WARNING!!! У величины {name} передано только значение.')
        return f'$ {name} = {round(val, n) if n != -1 else n}{units}$'

    if val is None and eps is None:
        raise ValueError(f'У величины {name} передана, только абсолютная погрешность')

    if val is None and sigma is None:
        raise ValueError(f'У величины {name} передана, только относительная погрешность')

    # Далее форматирование
    if eps is None and val != 0:
        eps = abs(sigma / val)

    if sigma is None:
        sigma = abs(val * eps)

    if val is None:
        if eps == 0:
            if sigma != 0:
                raise ValueError(f'У величины {name} переданы только погрешности, '
                                 f'при чем относительная равна нулю, а абсолютная нет')
            else:
                raise ValueError(f'У величины {name} переданы только погрешности, при чем относительная и '
                                 f'абсолютная равна нулю одновременно, получается неопределенность')
        else:
            print(f'WARNING!!! У величины {name} переданы только погрености, но не сама величина. '
                  f'Будет вычислено с точностью до знака Это странно.')
            val = sigma / eps

    if n != -1:
        val_ = round(val, n)
        sigma_ = round(sigma, n)
        eps_ = round(eps * 100, n)

    else:
        val_ = val
        sigma_ = sigma * 100
        eps_ = eps * 100

    return f'$ {name} = {val_} \\pm {sigma_}{units}, \\; \\varepsilon_{{{name}}} = {eps_} \\% $'
