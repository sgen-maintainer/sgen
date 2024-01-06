from fields import (
    Collection,
    String,
    Float,
    Boolean,
    Integer,
)
from validate import Length
from tests import Unique, has_data_type
from utils import Missing

DATA_TYPES = [
    # [Тип поля, представляемый им тип, противоположный тип]
    [String, str, int],
    [Integer, int, str],
    [Float, float, str],
    [Boolean, bool, str],
]


def test_simple():
    for type_ in DATA_TYPES:
        field = Collection(data_type=type_[0]())

        field_values = field.negative()

        assert None not in field_values
        assert not has_data_type(field_values, Missing)
        assert has_data_type(field_values, list)

        for value in field_values:
            if isinstance(value, list):
                assert (
                    has_data_type(value, type_[1]) or
                    has_data_type(value, type_[2]) or
                    has_data_type(value, Missing) or
                    None not in value
                )

        default = Unique()
        field = Collection(data_type=type_[0](), default=default)
        assert default not in field.negative()


def test_length_validator():
    min_length = 100
    max_length = 200

    for type_ in DATA_TYPES:
        field = Collection(
            data_type=type_[0](allow_none=False, required=True),
            validate=Length(
                min_length=min_length,
                max_length=max_length,
            ),
            allow_none=False,
            required=True,
        )

        field_values = field.negative()

        assert None in field_values
        assert has_data_type(field_values, Missing)
        assert has_data_type(field_values, list)

        has_lower = False
        has_min = False
        has_max = False
        has_biggest = False
        has_positive_len_but_wrong_type_min = False
        has_positive_len_but_wrong_type_max = False

        for value in field_values:
            if not isinstance(value, list):
                continue

            if len(value) == min_length - 1:
                has_lower = True
            elif len(value) == min_length:
                has_min = True
                if isinstance(value[0], type_[2]):
                    has_positive_len_but_wrong_type_min = True
            elif len(value) == max_length:
                has_max = True
                if isinstance(value[0], type_[2]):
                    has_positive_len_but_wrong_type_max = True
            elif len(value) == max_length + 1:
                has_biggest = True

        assert has_lower and has_min and has_max and has_biggest
        assert has_positive_len_but_wrong_type_min
        assert has_positive_len_but_wrong_type_max


def test_length_validator_with_inclusive():
    min_length = 100
    max_length = 200

    for type_ in DATA_TYPES:
        field = Collection(
            data_type=type_[0](allow_none=False, required=True),
            validate=Length(
                min_length=min_length,
                max_length=max_length,
                min_inclusive=False,
                max_inclusive=False,
            ),
            allow_none=False,
            required=True,
        )

        field_values = field.negative()

        has_lower = False
        has_min = False
        has_max = False
        has_biggest = False
        has_positive_len_but_wrong_type_min = False
        has_positive_len_but_wrong_type_max = False

        for value in field_values:
            if not isinstance(value, list):
                continue

            if len(value) == min_length:
                has_lower = True
            elif len(value) == min_length + 1:
                has_min = True
                if isinstance(value[0], type_[2]):
                    has_positive_len_but_wrong_type_min = True
            elif len(value) == max_length - 1:
                has_max = True
                if isinstance(value[0], type_[2]):
                    has_positive_len_but_wrong_type_max = True
            elif len(value) == max_length:
                has_biggest = True

        assert has_lower and has_min and has_max and has_biggest
        assert has_positive_len_but_wrong_type_min
        assert has_positive_len_but_wrong_type_max
