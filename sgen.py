from inspect import getmembers
from typing import List

from fields import Field
from dto import SchemaField
from utils import Missing


class SGen:
    """
    Класс для генерации тестовых структур данных.
    """

    def fields(self, is_positive: bool) -> List[SchemaField]:
        """
        Возвращает список полей схемы и генераторы данных для них.

        :param is_positive: True если надо вернуть позитивные генераторы.
        :return: Список SchemaField.
        """

        method = 'positive' if is_positive else 'negative'

        schema_fields = getmembers(
            self,
            lambda field: isinstance(field, Field)
        )

        return [
            SchemaField(attr_name=field[0], data_generator=getattr(field[1], method))
            for field in schema_fields
        ]

    def _generate(self, fields: List[SchemaField]):
        """
        Генерирует декартово произведение значений полей.

        :param fields: Список полей.
        :return: Генератор.
        """

        if len(fields) == 1:
            for value in fields[0].data_generator():
                yield [(fields[0].attr_name, value)]
        else:
            for value in fields[0].data_generator():
                for rest in self._generate(fields=fields[1:]):
                    yield [(fields[0].attr_name, value)] + rest

    def positive(self):
        """
        Генерирует набор позитивных тестовых данных.

        :return: Генератор словарей.
        """

        for dataset in self._generate(fields=self.fields(is_positive=True)):
            yield dict(filter(
                lambda field_value: not isinstance(field_value[1], Missing),
                dataset
            ))

    def negative(self):
        """
        Генерирует набор негативных тестовых данных.

        :return: Список словарей.
        """

        positive_generators = self.fields(is_positive=True)
        negative_generators = self.fields(is_positive=False)

        for n_gen in negative_generators:
            fields = [n_gen]
            for p_gen in positive_generators:
                if p_gen.attr_name == n_gen.attr_name:
                    continue
                fields.append(p_gen)

            for dataset in self._generate(fields=fields):
                yield dict(filter(
                    lambda field_value: not isinstance(field_value[1], Missing),
                    dataset
                ))

        for dataset in self._generate(fields=self.fields(is_positive=False)):
            yield dict(filter(
                lambda field_value: not isinstance(field_value[1], Missing),
                dataset
            ))
