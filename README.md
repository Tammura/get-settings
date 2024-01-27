# get-settings

[![PyPI version][pypi_badge]][pypi_link]

get-settings is a python library designed to facilitate the retrieval of configuration variables from a `settings.py` file. It provides a convenient way to load these variables as a Python dictionary. This library is particularly useful in the development of Python libraries, as it can dynamically detect and load configuration file content.

- [Installation](#installation)
- [Usage](#usage)
  * [Automatic configuration](#usage)
  * [Manual configuration](#manual-configuration)
- [File format](#file-format)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)


## Installation

```shell
pip install get-settings
```

## Usage

```python
from get_settings import load_settings()

settings = load_settings()  # settings = {"USER": "foo", "EMAIL": "foo@example.org"}
```

Ensure that `settings.py` file exists in the project root and contains the necessary configuration parameters
```
.
├── settings.py
└── foo.py
```

Don't forget to add `get_settings` to your pyproject.toml:
```toml
dependencies = [
    "get-settings>=0.1.0",
]
```

### Manual configuration

Also, you can manually provide the file path to the library's configuration function:

```python
# Provide the path to the settings.py file
settings_path = "/path/to/settings.py"
settings = load_settings(settings_path)
```

## File format
Varibales accepts from the library
```python
# settings.py

USER = "FOO" # YES
PORT = 8000 # YES
DEBUG = True # YES
ORIGINS = ["http://localhost", ...] # YES
FOO = {"email": "foo@example.com"} # YES

foo = "user" # NO
__FOO__ = "user" # NO
```
the result of `load_settings()` will be the following:
```python
{
    "USER": "FOO",
    "PORT": 8000,
    "DEBUG": True,
    "ORIGINS": ["http://localhost", ...],
    "FOO": {"email": "foo@example.com"},
}
```

## Contributing
We welcome contributions to this project! If you would like to contribute, please fork this repository and submit a pull request with your changes. Before submitting a pull request, please make sure that your changes are fully tested and that they adhere to our code standards.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Credits
Some features in this library are partially inspired by the [python-dotenv]([pyton-dotenv]) library
Copyright (c) 2014, Saurabh Kumar, 2013, Ted Tieken, 2013, Jacob Kaplan-Moss

<br>
Thank you for using get-settings library! 

[pypi_badge]: https://badge.fury.io/py/get-settings.svg
[pypi_link]: https://badge.fury.io/py/get-settings
[pyton-dotenv]: https://github.com/theskumar/python-dotenv