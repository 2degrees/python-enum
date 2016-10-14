# -*- coding: utf-8 -*-
from collections import OrderedDict

from nose.tools import assert_false
from nose.tools import assert_raises
from nose.tools import assert_raises_regexp
from nose.tools import eq_
from nose.tools import ok_
from nose.tools import raises

from enumeration import Enum, EnumItem, NonExistingEnumItemError, EnumField

AGES_OF_MAN = (
    'baby',
    'toddler',
    'child',
    'teenager',
    'adult',
    'elderly',
    )


class TestEnum(object):
    """Tests for :class:`Enum`."""

    def setup(self):
        self.ages_of_man_enum = Enum(
            *zip(
                AGES_OF_MAN,
                ('BABY', 'TODDLER', 'CHILD', 'TEENAGER', 'ADULT', 'ELDERLY')
                )
            )

    #{ Constructor tests

    def test_constructor_with_non_string_values(self):
        """Values must be strings."""
        assert_raises(AssertionError, Enum, (3.14, 'Pi'))

    def test_constructor_with_non_string_labels(self):
        """Labels must be strings."""
        assert_raises(AssertionError, Enum, ('Pi', 3.14))

    def test_constructor_with_duplicated_values(self):
        """Values must be unique."""
        assert_raises(AssertionError, Enum, ('1', 'One'), ('1', 'Uno'))

    def test_constructor_with_duplicated_labels(self):
        """Labels must be unique."""
        assert_raises(AssertionError, Enum, ('1', 'One'), ('1.0', 'One'))

    #{ Enum item retrieval tests

    def test_getattr_for_known_label(self):
        """Enum labels map to their respective EnumItem instances."""

        retrieved_enum_item = self.ages_of_man_enum.ADULT
        expected_enum_item = EnumItem('adult', AGES_OF_MAN)
        eq_(retrieved_enum_item, expected_enum_item)

    @raises(AttributeError)
    def test_getattr_for_unknown_label(self):
        """Trying to access an non-existent label raises an AttributeError."""

        self.ages_of_man_enum.COW

    #{ Attribute setting tests

    @raises(AssertionError)
    def test_enum_item_overriding(self):
        """Enum items cannot be overridden."""

        self.ages_of_man_enum.ADULT = None

    def test_setting_non_enum_item(self):
        """Attributes other than enum items can be set."""

        self.ages_of_man_enum.other = 'Something'

        eq_(self.ages_of_man_enum.other, 'Something')

    #{ Contains test

    def test_contains_with_known_value(self):
        ok_('baby' in self.ages_of_man_enum)

    def test_contains_with_unknown_value(self):
        assert_false('sheep' in self.ages_of_man_enum)

    #}

    def test_iter(self):
        """Iteration happens over the enum values."""

        eq_(tuple(self.ages_of_man_enum), AGES_OF_MAN)

    def test_length(self):
        eq_(len(AGES_OF_MAN), len(self.ages_of_man_enum))

    def test_getting_items_by_values(self):
        expected_items_by_values = OrderedDict((
            ('baby', self.ages_of_man_enum.BABY),
            ('toddler', self.ages_of_man_enum.TODDLER),
            ('child', self.ages_of_man_enum.CHILD),
            ('teenager', self.ages_of_man_enum.TEENAGER),
            ('adult', self.ages_of_man_enum.ADULT),
            ('elderly', self.ages_of_man_enum.ELDERLY),
            ))

        eq_(self.ages_of_man_enum.get_items_by_values(),
            expected_items_by_values)

    def test_getting_existing_item_by_value(self):
        eq_(
            self.ages_of_man_enum.ADULT,
            self.ages_of_man_enum.get_item_by_value('adult'),
            )

    def test_getting_non_existing_item_by_value(self):
        non_existing_item_value = 'sheep'
        assert_raises_regexp(
            NonExistingEnumItemError,
            non_existing_item_value,
            self.ages_of_man_enum.get_item_by_value,
            non_existing_item_value,
            )

    def test_setting_ui_labels(self):
        assert_false(self.ages_of_man_enum.has_ui_labels)

        items_ui_labels = {
            self.ages_of_man_enum.BABY: "Baby",
            self.ages_of_man_enum.TODDLER: "Toddler",
            self.ages_of_man_enum.CHILD: "Child",
            self.ages_of_man_enum.TEENAGER: "Teenager",
            self.ages_of_man_enum.ADULT: "Adult",
            self.ages_of_man_enum.ELDERLY: "Elderly",
            }
        self.ages_of_man_enum.set_ui_labels(items_ui_labels)
        for enum_item, item_label in items_ui_labels.items():
            eq_(enum_item._item_ui_label, item_label)

        ok_(self.ages_of_man_enum.has_ui_labels)

    def test_setting_missing_key(self):
        """Every enum item has to receive a label"""
        items_ui_labels = {
            self.ages_of_man_enum.BABY: "Baby",
            }

        assert_raises(AssertionError,
                      self.ages_of_man_enum.set_ui_labels,
                      items_ui_labels)

        assert_false(self.ages_of_man_enum.has_ui_labels)

    def test_getting_ui_labels(self):
        items_ui_labels = OrderedDict((
            (self.ages_of_man_enum.BABY, 'Baby'),
            (self.ages_of_man_enum.TODDLER, 'Toddler'),
            (self.ages_of_man_enum.CHILD, 'Child'),
            (self.ages_of_man_enum.TEENAGER, 'Teenager'),
            (self.ages_of_man_enum.ADULT, 'Adult'),
            (self.ages_of_man_enum.ELDERLY, 'Elderly'),
            ))
        self.ages_of_man_enum.set_ui_labels(items_ui_labels)
        eq_(self.ages_of_man_enum.get_ui_labels(),
            tuple(items_ui_labels.items()))


class TestEnumItem(object):
    """Tests for :class:`EnumItem`."""

    def setup(self):
        self.enum1_item1 = EnumItem('baby', AGES_OF_MAN)
        self.enum1_item1_copy = EnumItem('baby', AGES_OF_MAN)
        self.enum1_item2 = EnumItem('toddler', AGES_OF_MAN)
        self.enum2_item1 = EnumItem('Cow', ('Sheep', 'Cow'))

    def test_item_value_not_in_enum_values(self):
        """
        The constructor checks that the item's value is one of the values enum.

        """

        assert_raises(AssertionError, EnumItem, 'Dead', AGES_OF_MAN)

    def test_repr(self):
        enum_item = EnumItem('baby', AGES_OF_MAN)

        eq_(repr(enum_item), "<EnumItem: value='baby', index=0>")

    def test_str(self):
        """The str representation is that of the item value."""
        item_value = 'baby'
        enum_item = EnumItem(item_value, AGES_OF_MAN)

        eq_(str(enum_item), str(item_value))

    def test_length(self):
        """The length is that of the item value."""
        item_value = 'baby'
        enum_item = EnumItem(item_value, AGES_OF_MAN)

        eq_(len(enum_item), len(item_value))

    def test_hash(self):
        """The hash is the same as the hash of the item value."""
        item_value = 'baby'
        enum_item = EnumItem(item_value, AGES_OF_MAN)

        eq_(hash(enum_item), hash(item_value))

    #{ Equality tests

    def test_comparison_with_heterogenous_objects(self):
        """Rich comparison is only supported with items of the same enum."""
        eq_(self.enum1_item1.__eq__('baby'), NotImplemented)
        eq_(self.enum1_item1.__eq__(self.enum2_item1), NotImplemented)

    def test_equals(self):
        """The item_value is considered as the basis of the equality check."""
        eq_(self.enum1_item1, self.enum1_item1)
        eq_(self.enum1_item1, self.enum1_item1_copy)
        assert_false(self.enum1_item1 == self.enum1_item2)

    def test_not_equals(self):
        ok_(self.enum1_item1 != self.enum1_item2)
        assert_false(self.enum1_item1 != self.enum1_item1)
        assert_false(self.enum1_item1 != self.enum1_item1_copy)

    #{ Inequality tests

    def test_less_than(self):
        """The index is used when determining less than comparisons."""
        ok_(self.enum1_item1 < self.enum1_item2)
        assert_false(self.enum1_item1 < self.enum1_item1)
        assert_false(self.enum1_item2 < self.enum1_item1)

    def test_less_than_or_equal_to(self):
        """
        The index is used when determining less than or equal to comparisons.

        """
        ok_(self.enum1_item1 <= self.enum1_item2)
        ok_(self.enum1_item1 <= self.enum1_item1)
        assert_false(self.enum1_item2 <= self.enum1_item1)

    def test_greater_than(self):
        """The index is used when determining greater than comparisons."""
        ok_(self.enum1_item2 > self.enum1_item1)
        assert_false(self.enum1_item1 > self.enum1_item1_copy)
        assert_false(self.enum1_item1 > self.enum1_item2)

    def test_greater_than_or_equal_to(self):
        """
        The index is used when determining greater than or equal to comparisons.

        """
        ok_(self.enum1_item2 >= self.enum1_item1)
        ok_(self.enum1_item1 >= self.enum1_item1_copy)
        assert_false(self.enum1_item1 >= self.enum1_item2)

    #{ Tests for retrieving previous and subsequent values

    def test_previous_values(self):
        eq_(self.enum1_item1.previous_values, tuple())
        eq_(self.enum1_item2.previous_values, ('baby',))

    def test_previous_values_with_self(self):
        eq_(self.enum1_item1.previous_values_with_self, ('baby',))
        eq_(self.enum1_item2.previous_values_with_self, ('baby', 'toddler'))

    def test_subsequent_values(self):
        enum1_penultimate_item = EnumItem('adult', AGES_OF_MAN)
        enum1_last_item = EnumItem('elderly', AGES_OF_MAN)

        eq_(enum1_penultimate_item.subsequent_values, ('elderly',))
        eq_(enum1_last_item.subsequent_values, tuple())

    def test_subsequent_values_with_self(self):
        enum1_penultimate_item = EnumItem('adult', AGES_OF_MAN)
        enum1_last_item = EnumItem('elderly', AGES_OF_MAN)

        eq_(enum1_penultimate_item.subsequent_values_with_self,
            ('adult', 'elderly'))
        eq_(enum1_last_item.subsequent_values_with_self, ('elderly',))

    #{ Tests for setting and getting UI labels

    def test_setting_ui_label(self):
        item_ui_label = "Enum item 1 UI label"
        self.enum1_item1.set_ui_label(item_ui_label)
        eq_(self.enum1_item1._item_ui_label, item_ui_label)

    def test_getting_ui_label(self):
        item_ui_label = "Enum item 1 UI label"
        self.enum1_item1._item_ui_label = item_ui_label
        eq_(self.enum1_item1.get_ui_label(), item_ui_label)

    @raises(AssertionError)
    def test_getting_unset_ui_label(self):
        """Getting the UI label when it is unset raises an AssertionError"""
        self.enum1_item1.get_ui_label()

    #}


class TestEnumField(object):
    """Tests for :class:`EnumField`."""

    def setup(self):
        self.CLOTHES_SIZE_ENUM = Enum(
            ('xs', 'EXTRA_SMALL'),
            ('s', 'SMALL'),
            ('m', 'MEDIUM'),
            ('l', 'LARGE'),
            ('xl', 'EXTRA_LARGE'),
            ('xxl', 'EXTRA_EXTRA_LARGE'),
            )

        self.enum_field = EnumField(self.CLOTHES_SIZE_ENUM)

    def test_max_length(self):
        """The field takes its maximum length from the longest enum value."""
        enum_field = EnumField(self.CLOTHES_SIZE_ENUM)

        eq_(enum_field.max_length, 3)

    def test_conversion_from_string_to_python(self):
        """The field is converted to an Enum item if it's set as a string."""

        eq_(self.CLOTHES_SIZE_ENUM.EXTRA_SMALL, self.enum_field.to_python('xs'))

        assert_raises(AssertionError, self.enum_field.to_python, 'ultra_large')

    def test_conversion_from_enum_item_to_python(self):
        """The field is left as is if it's set as an enum item."""

        eq_(
            self.CLOTHES_SIZE_ENUM.EXTRA_SMALL,
            self.enum_field.to_python(self.CLOTHES_SIZE_ENUM.EXTRA_SMALL),
            )

        assert_raises(
            AssertionError,
            self.enum_field.to_python,
            EnumItem('baby', ('baby', 'adult')),
            )

    def test_conversion_from_none_to_python(self):
        eq_(None, self.enum_field.to_python(None))

    def test_get_prep_value(self):
        eq_('s', self.enum_field.get_prep_value(self.CLOTHES_SIZE_ENUM.SMALL))

    def test_get_prep_value_with_none(self):
        eq_(None, self.enum_field.get_prep_value(None))

    def test_from_db_value(self):
        enum_value = self.enum_field.from_db_value('s', None, None, None)
        eq_(self.CLOTHES_SIZE_ENUM.SMALL, enum_value)

    def test_from_db_value_with_none(self):
        enum_value = self.enum_field.from_db_value(None, None, None, None)
        eq_(None, enum_value)

    def test_choices_for_ui_labels(self):
        """
        When the UI labels are set for the Enum, the "choices" attribute is
        automatically set from the Enum.
        """

        items_ui_labels = {
            self.CLOTHES_SIZE_ENUM.EXTRA_SMALL: 'Extra small',
            self.CLOTHES_SIZE_ENUM.SMALL: 'Small',
            self.CLOTHES_SIZE_ENUM.MEDIUM: 'Medium',
            self.CLOTHES_SIZE_ENUM.LARGE: 'Large',
            self.CLOTHES_SIZE_ENUM.EXTRA_LARGE: 'Extra large',
            self.CLOTHES_SIZE_ENUM.EXTRA_EXTRA_LARGE: 'Extra extra large',
            }

        self.CLOTHES_SIZE_ENUM.set_ui_labels(items_ui_labels)

        enum_field = EnumField(self.CLOTHES_SIZE_ENUM)

        eq_(enum_field.choices, self.CLOTHES_SIZE_ENUM.get_ui_labels())

    def test_choices_for_ui_labels_with_choices(self):
        """
        If choices is specified when UI labels have already been set an
        AssertionError is raised.
        """

        items_ui_labels = {
            self.CLOTHES_SIZE_ENUM.EXTRA_SMALL: 'Extra small',
            self.CLOTHES_SIZE_ENUM.SMALL: 'Small',
            self.CLOTHES_SIZE_ENUM.MEDIUM: 'Medium',
            self.CLOTHES_SIZE_ENUM.LARGE: 'Large',
            self.CLOTHES_SIZE_ENUM.EXTRA_LARGE: 'Extra large',
            self.CLOTHES_SIZE_ENUM.EXTRA_EXTRA_LARGE: 'Extra extra large',
            }

        self.CLOTHES_SIZE_ENUM.set_ui_labels(items_ui_labels)

        assert_raises(AssertionError, EnumField, self.CLOTHES_SIZE_ENUM,
            choices=(('a', 'Apple'), ('b', 'Ball'))
            )

    def test_choices_for_unset_ui_labels_no_choices(self):
        """
        When no UI labels have been set and no "choices" argument is passed,
        the "choices" attribute is not set.
        """

        eq_(self.enum_field.choices, [])

    def test_choices_for_unset_ui_labels_with_choices(self):
        """
        When no UI labels have been set but a "choices" argument is passed,
        the "choices" attribute is set to the choices passed in.
        """

        choices = (('a', 'Apple'), ('b', 'Ball'))
        enum_field = EnumField(self.CLOTHES_SIZE_ENUM, choices=choices)

        eq_(enum_field.choices, choices)
