# <a>SGen</a>

Sgen is a tool for generating test data structures in Python

## <a>Content</a>

- [Description](#about)
- [Get It Now](#download)
- [Documentation](#docs)
- [Requirements](#requirements)
- [Project Links](#links)
- [License](#license)


## <a id="about">Description</a>

- Sgen is a tool for generating test data structures in Python.

```python
from pprint import pprint

from sgen import Sgen, fields


class Pet(SGen):
    name = fields.String()


class User(SGen):
    name = fields.String()
    pet = fields.Nested(Pet(), required=True)


def main():
    datasets = list(User().positive())

    pprint(datasets, indent=2)


if __name__ == '__main__':
    main()

# [ {'name': None, 'pet': {'name': None}},
#   {'name': None, 'pet': {}},
#   {'name': None, 'pet': {'name': 'fszxSnf'}},
#   {'pet': {'name': None}},
#   {'pet': {}},
#   {'pet': {'name': 'RzGTdNzhr'}},
#   {'name': 'ttr', 'pet': {'name': None}},
#   {'name': 'ttr', 'pet': {}},
#   {'name': 'ttr', 'pet': {'name': 'ZpvMOyR'}}]
```

In short, SGen can be used to:

- Generating positive data structures
- Generating negative data structures
- Checking the functionality of data validation at the application input

## <a id="download">Get It Now</a>

```commandline
pip install sgen
```

## <a id="docs">Documentation</a>

- Full documentation is available at [here](https://sgen.readthedocs.io/)

## <a id="requirements">Requirements</a>

- Python >= 3.8

## <a id="links">Project Links</a>

- [Repo](https://github.com/Apels1nA/sgen)
- [Docs](https://sgen.readthedocs.io/)
- [Changelog](https://sgen.readthedocs.io/en/latest/changelog.html)
- [Issues](https://github.com/Apels1nA/sgen/issues)

## <a id="license">License</a>

- MIT licensed. See the bundled [LICENSE](LICENSE) file for more details.
