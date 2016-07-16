from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from animals.models import Animal


class AnimalTests(APITestCase):

    def test_create_animal(self):
        """
        Ensure we can create a new animal object.
        """
        url = reverse('animals:list')
        data = {'name': 'A dog'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Animal.objects.count(), 1)
        self.assertEqual(Animal.objects.get().name, 'A dog')

    def test_update_animal(self):
        """
        Ensure we can update an existing animal object and
        that the response returns the updated object
        representation
        """
        animal = Animal.objects.create(name='A cat')
        url = reverse('animals:detail', kwargs={'pk': animal.pk})
        data = {'name': 'A dog'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Animal.objects.get().name, 'A dog')
        self.assertEqual(response.data, {'id': animal.pk, 'name': 'A dog'})

    def test_delete_animal(self):
        """
        Ensure we can delete an animal object.
        """
        animal = Animal.objects.create(name='A dog')
        url = reverse('animals:detail', kwargs={'pk': animal.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Animal.objects.count(), 0)

    def test_animal_detail(self):
        """
        Ensure we can get the an animal object representation
        """
        animal = Animal.objects.create(name='A dog')
        url = reverse('animals:detail', kwargs={'pk': animal.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': animal.pk, 'name': 'A dog'})

    def test_animal_list(self):
        """
        Ensure we can retrieve the animal list
        """
        a1 = Animal.objects.create(name='A dog')
        a2 = Animal.objects.create(name='A cat')
        url = reverse('animals:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {'id': a1.pk, 'name': 'A dog'},
            {'id': a2.pk, 'name': 'A cat'},
        ])
