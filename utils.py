from inspect import isgeneratorfunction, isgenerator


class Missing:
    """Представляет экземпляр пропущенного поля"""

    def __repr__(self):
        return "<sgen.missing>"


class ValuesStorage(list):
    """Представляет хранилище для значений полей"""

    def __contains__(self, item):
        present = list(filter(
            lambda value: type(value) == type(item) and value == item,
            self
        ))

        return bool(present)


def is_generator(obj) -> bool:
    """Возвращает True если obj является генератором"""

    return isgeneratorfunction(obj) or isgenerator(obj)


def is_iterable_but_not_string(obj) -> bool:
    """Возвращает True если obj итерируемый, но не строка"""

    return (hasattr(obj, "__iter__") and not hasattr(obj, "strip")) or is_generator(obj)
