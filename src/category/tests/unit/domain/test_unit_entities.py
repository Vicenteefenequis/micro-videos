import unittest
from datetime import datetime
from dataclasses import FrozenInstanceError, is_dataclass
from category.domain.entities import Category


class TestCategory(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_constructor(self):
        category = Category(name='Movie')

        self.assertEqual(category.name, 'Movie')
        self.assertEqual(category.description, None)
        self.assertEqual(category.is_active, True)
        self.assertIsInstance(category.created_at, datetime)

        created_at = datetime.now()
        category = Category(
            name='Movie',
            description='some description',
            is_active=False,
            created_at=created_at
        )

        self.assertEqual(category.name, 'Movie')
        self.assertEqual(category.description, 'some description')
        self.assertEqual(category.is_active, False)
        self.assertEqual(category.created_at, created_at)

    def test_if_created_at_is_generated_in_constructor(self):
        category1 = Category(name='Movie 1')
        category2 = Category(name='Movie 2')
        self.assertNotEqual(
            category1.created_at,
            category2.created_at
        )

    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = Category(name='Test')
            value_object.name = 'Test 2'  # type: ignore

    def test_update(self):
        category = Category(name='Movie')
        category.update(name='Movie 2', description='some description')

        self.assertEqual(category.name, 'Movie 2')
        self.assertEqual(category.description, 'some description')

    def test_activate(self):
        category = Category(name='Movie', is_active=False)
        category.activate()

        self.assertEqual(category.is_active, True)

    def test_deactivate(self):
        category = Category(name='Movie', is_active=True)
        category.deactivate()

        self.assertEqual(category.is_active, False)
