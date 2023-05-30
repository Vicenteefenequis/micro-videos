# pylint: disable=protected-access
from dataclasses import FrozenInstanceError, is_dataclass, dataclass
import unittest
import uuid
from unittest.mock import patch
from abc import ABC
from __seedwork.domain.value_objects import UniqueEntityId, ValueObject
from __seedwork.domain.exceptions import InvalidUuidException


@dataclass(frozen=True)
class StubOneProp(ValueObject):
    prop: str


@dataclass(frozen=True)
class StubTwoProp(ValueObject):
    prop1: str
    prop2: str


class TestValueObjectUnit(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_if_is_a_abstract_class(self):
        self.assertIsInstance(ValueObject(), ABC)

    def test_init_prop(self):
        vo1 = StubOneProp(prop='value')
        self.assertEqual(vo1.prop, 'value')

        vo2 = StubTwoProp(prop1='value1', prop2='value2')
        self.assertEqual(vo2.prop1, 'value1')
        self.assertEqual(vo2.prop2, 'value2')

    def test_convert_to_string(self):
        vo1 = StubOneProp(prop='value')
        self.assertEqual(str(vo1), 'value')

        vo2 = StubTwoProp(prop1='value1', prop2='value2')
        self.assertEqual(str(vo2), '{"prop1": "value1", "prop2": "value2"}')


class TestUniqueEntityIdUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_throw_exception_when_uuid_is_invalid(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate  # type: ignore
        ) as mock_validate:
            with self.assertRaises(InvalidUuidException) as assert_error:
                UniqueEntityId(id='invalid_uuid')
            mock_validate.assert_called_once()
            self.assertEqual(
                assert_error.exception.args[0], 'ID must be a valid UUID')

    def test_accept_uuid_passed_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate  # type: ignore
        ) as mock_validate:
            value_object = UniqueEntityId(
                id='f7b3a8f5-4d9f-4c1c-8a4f-4a5d9f4d9f4c')
            mock_validate.assert_called_once()
            self.assertEqual(
                value_object.id, 'f7b3a8f5-4d9f-4c1c-8a4f-4a5d9f4d9f4c')

    def test_generate_id_when_no_passed_id_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate  # type: ignore
        ) as mock_validate:
            value_object = UniqueEntityId()
            uuid.UUID(value_object.id)
            mock_validate.assert_called_once()

    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = UniqueEntityId()
            value_object.id = 'f7b3a8f5-4d9f-4c1c-8a4f-4a5d9f4d9f4c'  # type: ignore

    def test_str_representation(self):
        value_object = UniqueEntityId()
        self.assertEqual(value_object.id, str(value_object))
