## List of concurrent chats
[
![PyPI](https://img.shields.io/pypi/v/sp_ask_report_chats_per_school.svg)
![PyPI](https://img.shields.io/pypi/pyversions/sp_ask_report_chats_per_school.svg)
![PyPI](https://img.shields.io/github/license/guinslym/sp_ask_report_chats_per_school.svg)
](https://pypi.org/project/sp_ask_report_chats_per_school/)
[![TravisCI](https://travis-ci.org/guinslym/sp_ask_report_chats_per_school.svg?branch=master)](https://travis-ci.org/guinslym/sp_ask_report_chats_per_school)


provide a list of concurrents chats per operators

## Installation

**Ask Schools** can be installed from PyPI using `pip` or your package manager of choice:

```
pip install sp_ask_list_of_concurrent_chats
# or
poetry add sp_ask_list_of_concurrent_chats
```

## Usage

Example:

```python

from sp_ask_list_of_concurrent_chats import find_concurrent_chats
import lh3.api as lh3

if __name__ == '__main__':
    client = lh3.Client()
    chats = client.chats()
    all_chats = chats.list_day(2019,9,9, to="2019-10-09")
    df = find_concurrent_chats(all_chats)
    print(df.tail(10))

```


## Todo

1.  Add tests
2.  ~~Add column for Date~~
3.  Add Makefile
4.  ~~Add pypi~~
5.  ~~Create python package~~
6.  Add screenshot to Readme.md

