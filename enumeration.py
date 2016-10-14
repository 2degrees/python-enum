from collections import OrderedDict
from operator import eq, lt, gt, ge, le, ne

from django.db.models import CharField
from django.utils.deconstruct import deconstructible


class EnumField(CharField):

    def __init__(self, enum, *args, **kwargs):
        longest_enum_value = max(len(enum_value) for enum_value in enum)
        self._enum = enum

        if enum.has_ui_labels:
            assert 'choices' not in kwargs, \
                'The enum has UI labels set which precludes specifying choices'
            choices = enum.get_ui_labels()
        else:
            choices = kwargs.pop('choices', [])

        super(EnumField, self).__init__(
            max_length=longest_enum_value, choices=choices, *args, **kwargs
        )

        self.enum_items_by_values = enum.get_items_by_values()

    def deconstruct(self):
        name, path, args, kwargs = super(EnumField, self).deconstruct()
        args.insert(0, self._enum)
        if self._enum.has_ui_labels:
            del kwargs['choices']
        del kwargs['max_length']
        return name, path, args, kwargs

    def to_python(self, value):
        if isinstance(value, EnumItem):
            enum_values = list(self.enum_items_by_values.keys())
            assert list(value.enum_values) == enum_values, \
                'Enum item %r does not belong to this enum' % value

            enum_item = value

        elif value is None:
            enum_item = value

        else:
            assert value in self.enum_items_by_values, \
                '%r must be a value in the enum' % value

            enum_item = self.enum_items_by_values[value]

        return enum_item

    def from_db_value(self, value, expression, connection, context):
        value = self.to_python(value)
        return value

    def get_prep_value(self, value):
        if value is not None:
            value = str(value)
        return value


class NonExistingEnumItemError(Exception):
    pass


@deconstructible
class Enum(object):
    """An enumeration."""

    def __init__(self, *items):
        super(Enum, self).__init__()

        # Ensure that the values and labels are unique:
        values, labels = zip(*items)
        unique_values_count = len(set(values))
        unique_labels_count = len(set(labels))
        assert unique_labels_count == len(items), 'The labels must be unique'
        assert unique_values_count == len(items), 'The values must be unique'

        # Generate EnumItems based the items passed, ensuring that all values
        # and labels are strings.
        self._items = OrderedDict()
        for value, label in items:
            assert isinstance(value, str), \
                'Value %r must be a string' % value
            assert isinstance(label, str), \
                'Label %r must be a string' % label

            self._items[label] = EnumItem(value, values)

        self.has_ui_labels = False

    def __getattr__(self, label):
        """Return the enum item for ``label``."""

        if label not in self._items:
            raise AttributeError('%r is not a valid enum label' % label)

        return self._items[label]

    def __setattr__(self, name, value):
        """
        Set attribute ``name`` to ``value`` providing ``name`` does not
        correspond to an enum label.
        """

        if '_items' in self.__dict__:
            assert name not in self._items, 'Enum items cannot be overridden'

        super(Enum, self).__setattr__(name, value)

    def __iter__(self):
        for enum_item in self._items.values():
            yield enum_item.item_value

    def __len__(self):
        return len(self._items)

    def set_ui_labels(self, ui_labels):
        """
        Set the UI labels for the enum items.
        :param ui_labels: A mapping of enum item values to UI label
        :type ui_labels: :class:`collections.Mapping`
        :raises: :exc:`KeyError` if ``ui_labels`` does not define an entry for
            a given enum item value.
        """

        enum_item_values = self._items.values()
        assert set(enum_item_values) == set(ui_labels.keys()), \
            "All the enum item values must have a UI label."

        for enum_item in enum_item_values:
            ui_label = ui_labels[enum_item]
            enum_item.set_ui_label(ui_label)

        self.has_ui_labels = True

    def get_ui_labels(self):
        """
        :return: A tuple with 2-element tuples (with the enum item and its UI
            label respectively)
        :rtype: :class:`tuple`
        :raises: :exc:`AssertionError` if no UI labels have been set
        """

        enum_items_and_labels = []
        for enum_item in self._items.values():
            enum_items_and_labels.append((enum_item, enum_item.get_ui_label()))

        return tuple(enum_items_and_labels)

    def get_item_by_value(self, item_value):
        if item_value not in self:
            raise NonExistingEnumItemError(item_value)

        items_by_values = self.get_items_by_values()
        item = items_by_values[item_value]
        return item

    def get_items_by_values(self):
        """
        :rtype: :class:`collections.OrderedDict`
        """

        items_by_values = OrderedDict()
        for enum_item in self._items.values():
            items_by_values[enum_item.item_value] = enum_item

        return items_by_values


@deconstructible
class EnumItem(object):
    """An item which exists within an Enum."""

    def __init__(self, item_value, enum_values):
        """
        :param item_value: The value this item represents
        :param item_value: :class:`basestring`
        :param enum_values: All possible values in the parent Enum
        :type enum_values: :class:`collections.Iterable`
        """

        super(EnumItem, self).__init__()

        assert item_value in enum_values, \
            "%r is not contained in the Enum's values" % item_value

        self.enum_values = enum_values
        self.item_value = item_value
        self._item_index = self.enum_values.index(item_value)
        self._item_ui_label = None

    def __repr__(self):
        return '<EnumItem: value=%r, index=%r>' % (self.item_value,
                                                   self._item_index,
                                                   )

    def __str__(self):
        """Return the str representation of the item values."""
        return str(self.item_value)

    def __len__(self):
        """Return the length of the item value."""
        return len(self.item_value)

    def __hash__(self):
        """Return the hash of the item value."""
        return hash(self.item_value)

    def __eq__(self, other):
        return self._compare(other, eq)

    def __ne__(self, other):
        return self._compare(other, ne)

    def __lt__(self, other):
        return self._compare(other, lt)

    def __le__(self, other):
        return self._compare(other, le)

    def __gt__(self, other):
        return self._compare(other, gt)

    def __ge__(self, other):
        return self._compare(other, ge)

    def _compare(self, other_item, operator):
        if not isinstance(other_item, self.__class__):
            comparison = NotImplemented
        elif self.enum_values != other_item.enum_values:
            comparison = NotImplemented
        else:
            comparison = operator(self._item_index, other_item._item_index)

        return comparison

    @property
    def previous_values(self):
        return self.enum_values[:self._item_index]

    @property
    def previous_values_with_self(self):
        return self.enum_values[:(self._item_index + 1)]

    @property
    def subsequent_values(self):
        return self.enum_values[(self._item_index + 1):]

    @property
    def subsequent_values_with_self(self):
        return self.enum_values[self._item_index:]

    def get_ui_label(self):
        """
        Retrieve the label for display to a user.
        :raises: :exc:`AssertionError` if the UI label has not been set
        """

        assert self._item_ui_label is not None, \
            'The UI label must be set before retrieving it'

        return self._item_ui_label

    def set_ui_label(self, label):
        """Set the label for display to a user."""

        self._item_ui_label = label
