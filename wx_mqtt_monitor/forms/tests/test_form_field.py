import unittest

from mqtt_monitor.forms.form_field import FormField

class TestFormField(unittest.TestCase):
    def setUp(self):
        self.form_field = FormField("TestField", "TestValue")

    def test_getFieldValue(self):
        self.assertEqual(self.form_field.getFieldValue(), "TestValue")

    def test_setFieldValue(self):
        self.form_field.setFieldValue("NewTestValue")
        self.assertEqual(self.form_field.getFieldValue(), "NewTestValue")

    def test_renderField_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.form_field.renderField()

if __name__ == '__main__':
    unittest.main()
