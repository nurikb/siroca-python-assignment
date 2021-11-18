from django.test import TestCase
from sirocaapp.forms import IndexForm


class TestForms(TestCase):


    def test_form_valid_data(self):
        form = IndexForm(data={
            'url': "https://github.com/nurikb/inventory"
        })

        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form = IndexForm(data={
            'url':"google.com/nurikb/inventory"
        })

        self.assertEquals(len(form.errors), 1)