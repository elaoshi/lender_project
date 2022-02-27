import pytest
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APITestCase

from lenders.models import Lender

class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new object.
        """
        url = '/lender'
        data = {
            "name":"33f",
            "code":"Abc",
            "upfront_commistion_rate":0.12,
            "trait_commistion_rate":0.01,
            "active":False
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'],data['name'])
        self.assertEqual(Lender.objects.count(), 1)
        self.assertEqual(Lender.objects.get().name, data['name'])

