from tests import has_data_type, Unique
from fields import Integer
from validate import Range, Equal, OneOf
from utils import Missing


def test_int():
    field = Integer()

    negative_values = field.negative()

    assert len(negative_values) == 1
    assert not isinstance(negative_values[0], int)


def test_allow_none():
    field = Integer(allow_none=False)

    assert None in field.negative()


def test_required():
    field = Integer(required=True)

    assert has_data_type(field.negative(), Missing)


def test_negative_data_from():
    def negative_data_from():
        return 'a', 666, None, Missing

    field = Integer(negative_data_from=negative_data_from)

    assert field.negative() == list(negative_data_from())


# ===================================================
# Тесты на взаимодействие типа Integer с валидаторами
# ===================================================


def test_range():
    min_value = -998
    max_value = 649

    field = Integer(
        validate=Range(
            min_value=min_value, max_value=max_value
        )
    )

    negative_data = field.negative()

    assert min_value - 1 in negative_data
    assert max_value + 1 in negative_data


def test_range_inclusive():
    min_value = -998
    max_value = 649

    field = Integer(
        validate=Range(
            min_value=min_value,
            max_value=max_value,
            min_inclusive=False,
            max_inclusive=False,
        ),
        allow_none=False,
        required=True,
    )

    negative_data = field.negative()

    assert min_value in negative_data
    assert max_value in negative_data
    assert None in negative_data
    assert has_data_type(negative_data, Missing)


def test_range_default():
    min_value = -998
    max_value = 649
    default = Unique()

    field = Integer(
        validate=Range(
            min_value=min_value,
            max_value=max_value,
            min_inclusive=False,
            max_inclusive=False,
        ),
        allow_none=False,
        default=default,
    )

    negative_data = field.negative()

    assert min_value in negative_data
    assert max_value in negative_data
    assert None in negative_data
    assert default not in negative_data


def test_equal():
    comparable = [Unique()]

    field = Integer(
        validate=Equal(comparable=comparable)
    )

    field_values = field.negative()

    assert comparable[0] not in field_values
    assert None not in field_values
    assert has_data_type(field_values, str)


def test_equal_allow_none_required():
    comparable = [Unique()]

    field = Integer(
        validate=Equal(comparable=comparable),
        allow_none=False,
        required=True,
    )

    field_values = field.negative()

    assert comparable[0] not in field_values
    assert None in field_values
    assert has_data_type(field_values, str)
    assert has_data_type(field_values, Missing)


def test_equal_default():
    comparable = [Unique()]
    default = Unique()

    field = Integer(
        validate=Equal(comparable=comparable),
        allow_none=False,
        default=default,
    )

    field_values = field.negative()

    assert default not in field_values
    assert None in field_values


def test_one_of():
    choices = [Unique(), Unique(), Unique()]

    field = Integer(
        validate=OneOf(choices=choices),
    )

    field_values = field.negative()

    for value in choices:
        assert value not in field_values

    assert None not in field_values
    assert has_data_type(field_values, str)
    assert not has_data_type(field_values, Missing)


def test_one_of_allow_none_required():
    choices = [Unique(), Unique(), Unique()]

    field = Integer(
        validate=OneOf(choices=choices),
        allow_none=False,
        required=True,
    )

    field_values = field.negative()

    for value in choices:
        assert value not in field_values

    assert None in field_values
    assert has_data_type(field_values, str)
    assert has_data_type(field_values, Missing)


def test_one_of_default():
    choices = [Unique(), Unique(), Unique()]
    default = Unique()

    field = Integer(
        validate=OneOf(choices=choices),
        allow_none=False,
        default=default,
    )

    field_values = field.negative()

    for value in choices:
        assert value not in field_values

    assert None in field_values
    assert has_data_type(field_values, str)
    assert default not in field_values