from dataclasses import dataclass
from typing import Union

from fields import Field


@dataclass
class SchemaField:
    attr_name: str
    data_generator: Union[Field.positive, Field.negative]
