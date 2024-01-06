from typing import Iterable, Callable, Any, List, Union
from string import ascii_letters
from random import choice, randint

from base import FieldABC, ValidatorABC
from utils import is_iterable_but_not_string, Missing, ValuesStorage


class Field(FieldABC):
    """Базовый класс для типов данных"""

    def __init__(
        self,
        validate: (
            ValidatorABC
            | Iterable[ValidatorABC]
            | None
        ) = None,
        positive_data_from: Callable[[], Iterable] = None,
        negative_data_from: Callable[[], Iterable] = None,
        allow_none: bool = True,
        required: bool = False,
        default: Any = None,
    ):
        if validate is None:
            self.validators = []
        elif callable(validate) or isinstance(validate, ValidatorABC):
            self.validators = [validate]
        elif is_iterable_but_not_string(validate):
            raise NotImplemented("На данный момент несколько валидаторов не поддерживаются")

        if (positive_data_from or negative_data_from) and default:
            raise ValueError("Параметры data_from и default не могут быть переданы одновременно")
        if required and default:
            raise ValueError("Параметры data_from и default не могут быть переданы одновременно")

        self.positive_data_from = positive_data_from
        self.negative_data_from = negative_data_from
        self.default = default
        self.allow_none = allow_none
        self.required = required
        self.values = ValuesStorage()

    def positive(self):
        self.values = ValuesStorage()
        if self.positive_data_from is not None:
            self._register(list(self.positive_data_from()))
            return

        for validator in self.validators:
            if not isinstance(self, Collection):
                self._register(validator.positive(self))

        if self.allow_none:
            self._register(None)

        if self.default is not None:
            self._register(self.default)

        if not self.required:
            self._register(Missing())

    def negative(self):
        self.values = ValuesStorage()
        if self.negative_data_from is not None:
            self._register(list(self.negative_data_from()))
            return

        for validator in self.validators:
            if not isinstance(self, Collection):
                self._register(validator.negative(self))

        if not self.allow_none:
            self._register(None)

        if self.required:
            self._register(Missing())

    def generate(self, length):
        raise NotImplemented(
            "Для возможности работы валидатора Length с итерируемыми типами данных"
            "необходимо реализовать метод generate, который вернет коллекцию длинны length"
        )

    def get_precision(self):
        raise NotImplemented(
            "Для возможности работы валидатора Range с числовыми типами данных"
            "необходимо реализовать метод get_precision, который вернет минимальный шаг для числового типа"
        )

    def _register(self, for_register: Union[Any, List[Any]]):
        """Добавляет новое значение/значения в список значений поля если оно еще не представлено"""

        if isinstance(for_register, list):
            for value in for_register:
                if value not in self.values:
                    self.values.append(value)
        else:
            if for_register not in self.values:
                self.values.append(for_register)


class String(Field):
    """Представление строк"""

    def positive(self) -> List[Union[str, None]]:
        super().positive()

        if self.positive_data_from is not None:
            return self.values

        if not self.validators:
            self._register(self.generate(length=randint(1, 10)))

        return self.values

    def negative(self) -> List[Union[str, None, Missing]]:
        super().negative()

        if self.negative_data_from is not None:
            return self.values

        self._register(randint(-100, 100))

        return self.values

    def generate(self, length: int):
        """
        Генерирует строку указанной длинны.

        :param length: Длинна строки.
        :return: Строка.
        """

        return ''.join(choice(ascii_letters) for _ in range(length))


class Integer(Field):
    """Представление целых чисел"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.precision = 1

    def positive(self):
        super().positive()

        if self.positive_data_from is not None:
            return self.values

        if not self.validators:
            self._register(randint(-100, 100))

        return self.values

    def negative(self):
        super().negative()

        if self.negative_data_from is not None:
            return self.values

        self._register(
            ''.join(choice(ascii_letters) for _ in range(randint(5, 10)))
        )

        return self.values

    def get_precision(self):
        return self.precision


class Float(Field):
    """Представление чисел с плавающей точкой"""

    def __init__(self, precision: float = 0.01, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.precision = precision

    def positive(self):
        super().positive()

        if self.positive_data_from is not None:
            return self.values

        if not self.validators:
            self._register(randint(-10000, 10000) / 100)

        return self.values

    def negative(self):
        super().negative()

        if self.negative_data_from is not None:
            return self.values

        self._register(
            ''.join(choice(ascii_letters) for _ in range(randint(5, 10)))
        )

        return self.values

    def get_precision(self):
        return self.precision


class Boolean(Field):
    """Представление логического типа"""

    def positive(self):
        super().positive()

        if self.positive_data_from is not None:
            return self.values

        if not self.validators:
            self._register([True, False])

        return self.values

    def negative(self):
        super().negative()

        if self.negative_data_from is not None:
            return self.values

        self._register(
            ''.join(choice(ascii_letters) for _ in range(randint(5, 10)))
        )

        return self.values


class Collection(Field):
    """Представление списков"""

    def __init__(self, data_type: FieldABC, *args, **kwargs):
        """
        Инициализирует коллекцию, добавляя в нее новый параметр data_type

        :param data_type: Тип данных для коллекции
        """

        super().__init__(*args, **kwargs)
        self.data_type = data_type
        self.inner_values = []

    def _register(self, for_register: Union[Any, List[Any]]):
        """
        Добавляет новое значение/значения в список значений поля если оно еще не представлено
        Дополнительно очищает списки от значения Missing, так как делать это на уровне класса SGen запарно

        :param for_register: Регистрируемое значение или список регистрируемых значений
        """

        if isinstance(for_register, list):
            self.values.extend([
                list(filter(lambda item: not isinstance(item, Missing), value))  # Фильтруем Missing внутри списков
                for value in for_register
                if list(filter(lambda item: not isinstance(item, Missing), value)) or not self.validators
            ])
        else:
            if for_register not in self.values:
                self.values.append(for_register)

    def positive(self):
        super().positive()

        if self.positive_data_from is not None:
            return self.values

        self.inner_values = self.data_type.positive()

        for validator in self.validators:
            values = validator.positive(self)
            for value in values:
                self._register(value)

        if not self.validators:
            for value in self.inner_values:
                self._register([[value for _ in range(randint(1, 5))]])
        return self.values

    def negative(self):
        super().negative()

        if self.negative_data_from is not None:
            return self.values

        self.inner_values = self.data_type.positive()
        for validator in self.validators:
            values = validator.negative(self)
            for value in values:
                self._register(value)

        self.inner_values = self.data_type.negative()
        for validator in self.validators:
            values = validator.positive(self)
            for value in values:
                self._register(value)

        if not self.validators:
            for value in self.inner_values:
                self._register([[value for _ in range(randint(1, 5))]])

        return self.values

    def generate(self, length):
        return [
            [allowed_value for _ in range(length)]
            for allowed_value in self.inner_values
        ]


class Nested(Field):
    """Представление сущностей"""

    def __init__(self, data_type: 'SGen', *args, **kwargs):
        """
        Инициализирует вложенную схему, добавляя в нее новый параметр data_type

        :param data_type: Тип данных для схемы
        """

        super().__init__(*args, **kwargs)
        self.data_type = data_type

    def positive(self):
        super().positive()

        if self.positive_data_from is not None:
            return self.values

        for structure in self.data_type.positive():
            yield structure

    def negative(self):
        super().negative()

        if self.negative_data_from is not None:
            return self.values

        for structure in self.data_type.negative():
            yield structure