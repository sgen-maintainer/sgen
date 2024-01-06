from typing import List, Any, Union
from random import randint
from datetime import datetime, date, time, timedelta

from base import ValidatorABC
from fields import Integer, Float, Field
from tests import Unique


class Length(ValidatorABC):
    """Ограничивает длину коллекции"""

    def __init__(
            self,
            min_length: int = None,
            max_length: int = None,
            min_inclusive: bool = True,
            max_inclusive: bool = True,
    ):
        """
        Представляет валидатор длинны коллекции или строки.

        :param min_length: Минимальная длинна.
        :param max_length: Максимальная длинна.
        :param min_inclusive: Включать ли минимальное значение.
        :param max_inclusive: Включать ли максимальное значение.
        """

        if not min_length and not max_length:
            raise ValueError("Один из параметров min_length, max_length является обязательным")

        if isinstance(min_length, int) and isinstance(max_length, int):
            min_ = min_length if min_inclusive else min_length + 1
            max_ = max_length if max_inclusive else max_length - 1

            if min_ >= max_:
                raise ValueError("Минимальное значение не может быть больше или равно максимальному")

        self.min_length = min_length
        self.max_length = max_length
        if isinstance(min_length, int):
            self.min_length = min_length if min_inclusive else min_length + 1
        if isinstance(max_length, int):
            self.max_length = max_length if max_inclusive else max_length - 1

    def positive(self, data_type: Field) -> List[Any]:
        """
        Генерирует позитивный набор данных согласно параметрам валидации.

        :param data_type: Тип данных подлежащих валидации.
        :return: List[Any]
        """

        values = []

        if self.min_length is not None:
            values.append(data_type.generate(self.min_length))
        if self.max_length is not None:
            values.append(data_type.generate(self.max_length))

        return values

    def negative(self, data_type: Field) -> List[Any]:
        """
        Генерирует негативный набор данных согласно параметрам валидации.

        :param data_type: Тип данных подлежащих валидации.
        :return: List[Any]
        """

        if self.min_length == 0:
            raise ValueError(
                "Неверная длинна коллекции: -1"
            )

        values = []

        if self.min_length is not None:
            values.append(data_type.generate(self.min_length - 1))
        if self.max_length is not None:
            values.append(data_type.generate(self.max_length + 1))

        return values


class Range(ValidatorABC):
    """Ограничивает диапазон значений числа"""

    def __init__(
            self,
            min_value: int | float = None,
            max_value: int | float = None,
            min_inclusive: bool = True,
            max_inclusive: bool = True,
    ):
        """
        Представляет валидатор длинны коллекции или строки.

        :param min_value: Минимальное значение.
        :param max_value: Максимальное значение.
        :param min_inclusive: Включать ли минимальное значение.
        :param max_inclusive: Включать ли максимальное значение.
        """

        if not min_value and not max_value:
            raise ValueError("Один из параметров min_value, max_value является обязательным")

        if min_value is not None and max_value is not None:
            if min_value >= max_value:
                raise ValueError("Минимальное значение не может быть больше или равно максимальному")

        self.min_value = min_value
        self.min_inclusive = min_inclusive
        self.max_value = max_value
        self.max_inclusive = max_inclusive

    def _get_min_value(self, data_type: Field, positive: bool = True) -> Union[int, float]:
        """
        Возвращает минимально допустимое значение диапазона для указанного тип данных и точности.

        :param data_type: Тип данных.
        :param positive: Позитивное или негативное значение.
        :return: Минимальная граница диапазона.
        """

        if self.min_inclusive:
            if positive:
                result = self.min_value
            else:
                result = self.min_value - data_type.get_precision()
        else:
            if positive:
                result = self.min_value + data_type.get_precision()
            else:
                result = self.min_value

        if isinstance(data_type, Float):
            return float(result)
        return result

    def _get_max_value(self, data_type: Field, positive: bool) -> Union[int, float]:
        """
        Возвращает максимально допустимое значение диапазона для указанного тип данных и точности.

        :param data_type: Тип данных.
        :param positive: Позитивное или негативное значение.
        :return: Максимальная граница диапазона.
        """

        if self.max_inclusive:
            if positive:
                result = self.max_value
            else:
                result = self.max_value + data_type.get_precision()
        else:
            if positive:
                result = self.max_value - data_type.get_precision()
            else:
                result = self.max_value

        if isinstance(data_type, Float):
            return float(result)
        return result

    def positive(self, data_type: Field) -> List[Any]:
        """
        Генерирует позитивный набор данных согласно параметрам валидации.

        :param data_type: Тип данных подлежащих валидации.
        :return: List[Any]
        """

        values = []

        if self.min_value is not None:
            values.append(self._get_min_value(data_type, positive=True))
        if self.max_value is not None:
            values.append(self._get_max_value(data_type, positive=True))

        return values

    def negative(self, data_type: Field) -> List[Any]:
        """
        Генерирует негативный набор данных согласно параметрам валидации.

        :param data_type: Тип данных подлежащих валидации.
        :return: List[Any]
        """

        values = []

        if self.min_value is not None:
            values.append(self._get_min_value(data_type, positive=False))
        if self.max_value is not None:
            values.append(self._get_max_value(data_type, positive=False))

        return values


class Equal(ValidatorABC):
    """Проверяет на равенство"""

    def __init__(self, comparable: Any):
        self.comparable = comparable

    def positive(self, data_type: Field) -> List[Any]:
        return self.comparable

    def negative(self, data_type: Field) -> List[Any]:
        if isinstance(self.comparable, int):
            return [self.comparable + randint(10, 100000)]
        elif isinstance(self.comparable, float):
            return [self.comparable + randint(1000000, 100000000) / 100]
        elif isinstance(self.comparable, str):
            return ['not_' + self.comparable]
        elif isinstance(self.comparable, bool):
            return [not self.comparable]
        elif isinstance(self.comparable, list):
            return [self.comparable * 2]
        elif isinstance(self.comparable, time) or isinstance(self.comparable, datetime):
            return [self.comparable + timedelta(minutes=randint(10, 100))]
        elif isinstance(self.comparable, date):
            return [self.comparable + timedelta(days=randint(10, 100))]
        elif isinstance(self.comparable, Unique):
            return [Unique()]
        else:
            raise TypeError(f"Неизвестный тип данных {self.comparable}")


class OneOf(ValidatorABC):
    """Проверяет на принадлежность к множеству choices"""

    def __init__(self, choices: List[Any]):
        self.choices = choices

    def positive(self, data_type: Field) -> List[Any]:
        return self.choices

    def negative(self, data_type: Field) -> List[Any]:
        result = []

        for value in self.choices:
            while True:
                # Переданный параметр data_type=Integer() не играет никакой роли. Недостаток архитектуры (?)
                new_value = Equal(comparable=value).negative(data_type=Integer())
                # Проверка на случайное попадание в одно из значений choices
                if new_value[0] not in self.choices:
                    result += new_value
                    break

        return result


class NoneOf(ValidatorABC):
    """Проверяет на непринадлежность к множеству choices"""

    def __init__(self, invalid_values: List[Any]):
        self.invalid_values = invalid_values

    def positive(self, data_type: Field) -> List[Any]:
        result = []

        for value in self.invalid_values:
            while True:
                # Переданный параметр data_type=Integer() не играет никакой роли. Недостаток архитектуры (?)
                valid_value = Equal(comparable=value).negative(data_type=Integer())
                # Проверка на случайное попадание в одно из значений invalid_values
                if valid_value[0] not in self.invalid_values:
                    result += valid_value
                    break

        return result

    def negative(self, data_type: Field) -> List[Any]:
        return self.invalid_values
