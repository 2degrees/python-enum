# python-enumeration

[![Build Status](https://travis-ci.org/2degrees/python-enumeration.svg?branch=master)](https://travis-ci.org/2degrees/python-enumeration) 
[![Coverage Status](https://coveralls.io/repos/github/2degrees/python-enumeration/badge.svg?branch=master)](https://coveralls.io/github/2degrees/python-enumeration?branch=master)

An enumeration data type for Python.

## Getting started

python-enumeration can be installed from PyPi via:

```bash
pip install python-enumeration

```

You can then import the library and define an enumeration:

```python
from enumeration import Enum

MY_ENUM = Enum(
    ('value', 'IDENTIFIER'),
    ...
)
```


## Usage

python-enumeration allows you to define enumerated data so that you have
a consistent interface to the underlying data, e.g.

```python
>>> from enumeration import Enum
>>> AGES_OF_MAN = Enum(
...     ('baby', 'BABY'),
...     ('toddler', 'TODDLER'),
...     ('child', 'CHILD'),
...     ('teenager', 'TEENAGER'),
...     ('adult', 'ADULT'),
...     ('elderly', 'ELDERLY'),
... )
>>> AGES_OF_MAN.BABY
<EnumItem: value='baby', index=0>
>>> str(AGES_OF_MAN.BABY)
'baby'
>>> AGES_OF_MAN.BABY.item_value
'baby'
```

### Comparison

python-enumeration supports comparison operations on its items so the
order in which the enum defines its items is importation:

```python
>>> AGES_OF_MAN.BABY < AGES_OF_MAN.TODDLER
True
>>> AGES_OF_MAN.TODDLER > AGES_OF_MAN.CHILD
False
>>> AGES_OF_MAN.ADULT <= AGES_OF_MAN.ADULT
True
```

It's also possible to list all the values which are less than or
greater than an item:

```python
>>> AGES_OF_MAN.CHILD.previous_values
('baby', 'toddler')
>>> AGES_OF_MAN.CHILD.previous_values_with_self
('baby', 'toddler', 'child')
>>> AGES_OF_MAN.CHILD.subsequent_values
('teenager', 'adult', 'elderly')
>>> AGES_OF_MAN.CHILD.subsequent_values_with_self
('child', 'teenager', 'adult', 'elderly')
```

### Setting human-readable labels

If you want to display a label for your enumeration in some UI, you can
define a set of UI labels for the enumeration:

```python
>>> AGES_OF_MAN.set_ui_labels({
...     AGES_OF_MAN.BABY: "Baby",
...     AGES_OF_MAN.TODDLER: "Toddler",
...     AGES_OF_MAN.CHILD: "Child",
...     AGES_OF_MAN.TEENAGER: "Teenager",
...     AGES_OF_MAN.ADULT: "Adult",
...     AGES_OF_MAN.ELDERLY: "Elderly",
... })
>>> AGES_OF_MAN.BABY.get_ui_label()
'Baby'
>>> AGES_OF_MAN.get_ui_labels()
((<EnumItem: value='baby', index=0>, 'Baby'), (<EnumItem: value='toddler', index=1>, 'Toddler'), (<EnumItem: value='child', index=2>, 'Child'), (<EnumItem: value='teenager', index=3>, 'Teenager'), (<EnumItem: value='adult', index=4>, 'Adult'), (<EnumItem: value='elderly', index=5>, 'Elderly'))
```

For further examples of how you can use the enumeration, see the test
suite.
