import csv
import os
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from lenders.models import Lender


class AccountTests(APITestCase):
    def test_create_lender(self):
        """
        Ensure we can create a new object.
        """
        url = '/lender'
        data = {
            "name": "33f",
            "code": "Abc",
            "upfront_commistion_rate": 0.12,
            "trait_commistion_rate": 0.01,
            "active": False
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(Lender.objects.count(), 1)
        self.assertEqual(Lender.objects.get().name, data['name'])

    @patch("pandas.read_csv")
    def test_upload_lender(self, mock_read_csv):
        """
        Ensure we can create a new object.
        """

        file_name = "test.csv"
        # Open file in write mode (Arrange)
        with open(file_name, "w") as file:
            writer = csv.writer(file)
            # Add some rows in csv file
            writer.writerow(["active", "name", "trait_commistion_rate", "upfront_commistion_rate", "code"])
            writer.writerow(
                [True, "test", 0.18, 0.21, 'Tes'],
            )
            writer.writerow(
                [True, "Best", 0.19, 0.22, 'Bes'],
            )
        # open file in read mode
        data = open(file_name, "rb")

        url = '/lender/upload'

        data = SimpleUploadedFile(content=data.read(), name=data.name, content_type='multipart/form-data')

        response = self.client.post(url, {"file": data}, format="multipart")
        mock_read_csv.return_value = True
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data.close()
        os.remove(file_name)

    def test_upload_lender_empty(self):
        """
        Ensure we can create a new object.
        """

        url = '/lender/upload'
        response = self.client.post(url, {"file":"aa"}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)