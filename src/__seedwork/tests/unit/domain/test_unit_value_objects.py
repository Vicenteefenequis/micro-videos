from dataclasses import is_dataclass
import unittest
from unittest.mock import patch
from __seedwork.domain.exceptions import InvalidUuidException
from __seedwork.domain.value_objects import UniqueEntityId
import uuid

class TestUniqueEntityIdUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_throw_exception_when_uuid_is_invalid(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate # type: ignore
        ) as mock_validate:
            with self.assertRaises(InvalidUuidException) as assert_error:
                UniqueEntityId(id='invalid_uuid')
            mock_validate.assert_called_once()
            self.assertEqual(assert_error.exception.args[0],'ID must be a valid UUID')
    
    def test_accept_uuid_passed_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate # type: ignore
        ) as mock_validate:
            value_object = UniqueEntityId(id='f7b3a8f5-4d9f-4c1c-8a4f-4a5d9f4d9f4c')
            mock_validate.assert_called_once()
            self.assertEqual(value_object.id,'f7b3a8f5-4d9f-4c1c-8a4f-4a5d9f4d9f4c')

    def test_generate_id_when_no_passed_id_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate # type: ignore
        ) as mock_validate:
            value_object = UniqueEntityId()
            uuid.UUID(value_object.id)
            mock_validate.assert_called_once()