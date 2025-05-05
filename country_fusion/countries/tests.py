from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from .models import Country


class CountryModelTestCase(TestCase):
    def setUp(self):
        self.country_data = {
            'name': 'Test Country',
            'common_name': 'Test',
            'cca2': 'TC',
            'cca3': 'TCY',
            'capital': 'Test City',
            'region': 'Test Region',
            'subregion': 'Test Subregion',
            'population': 1000000,
            'flag_url': 'https://example.com/flag.png',
            'flag_emoji': '🏳️',
            'timezones': ['UTC+01:00'],
            'languages': {'eng': 'English', 'fre': 'French'}
        }
        self.country = Country.objects.create(**self.country_data)

    def test_country_creation(self):
        self.assertEqual(self.country.name, 'Test Country')
        self.assertEqual(self.country.cca2, 'TC')
        self.assertEqual(self.country.population, 1000000)

    def test_get_languages(self):
        languages = self.country.get_languages()
        self.assertIn('English', languages)
        self.assertIn('French', languages)

    def test_get_timezone(self):
        timezone = self.country.get_timezone()
        self.assertEqual(timezone, 'UTC+01:00')


class CountryAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)
        
        self.country_data = {
            'name': 'Test Country',
            'common_name': 'Test',
            'cca2': 'TC',
            'cca3': 'TCY',
            'capital': 'Test City',
            'region': 'Test Region',
            'subregion': 'Test Subregion',
            'population': 1000000,
            'flag_url': 'https://example.com/flag.png',
            'flag_emoji': '🏳️',
            'timezones': ['UTC+01:00'],
            'languages': {'eng': 'English', 'fre': 'French'}
        }
        self.country = Country.objects.create(**self.country_data)
        
        # Create another country for testing region and language
        self.country2_data = {
            'name': 'Second Country',
            'common_name': 'Second',
            'cca2': 'SC',
            'cca3': 'SCY',
            'capital': 'Second City',
            'region': 'Test Region',  # Same region
            'subregion': 'Another Subregion',
            'population': 2000000,
            'flag_url': 'https://example.com/flag2.png',
            'flag_emoji': '🏴',
            'timezones': ['UTC+02:00'],
            'languages': {'eng': 'English', 'spa': 'Spanish'}  # Has English like first country
        }
        self.country2 = Country.objects.create(**self.country2_data)

    def test_list_countries(self):
        response = self.client.get(reverse('api_country_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_country(self):
        new_country_data = {
            'name': 'New Country',
            'common_name': 'New',
            'cca2': 'NC',
            'cca3': 'NCY',
            'capital': 'New City',
            'region': 'New Region',
            'subregion': 'New Subregion',
            'population': 3000000,
            'flag_url': 'https://example.com/flag3.png',
            'flag_emoji': '🏁',
            'timezones': ['UTC+03:00'],
            'languages': {'eng': 'English', 'ger': 'German'}
        }
        response = self.client.post(reverse('api_country_list'), new_country_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_country(self):
        response = self.client.get(reverse('api_country_detail', kwargs={'pk': self.country.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.country.name)
        self.assertEqual(response.data['cca2'], self.country.cca2)
        
    def test_update_country(self):
        updated_data = {'name': 'Updated Country Name'}
        response = self.client.patch(
            reverse('api_country_detail', kwargs={'pk': self.country.pk}),
            updated_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Country Name')
        
    def test_delete_country(self):
        response = self.client.delete(
            reverse('api_country_detail', kwargs={'pk': self.country.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Country.objects.count(), 1)  # Only country2 remains
        
    def test_regional_countries(self):
        response = self.client.get(
            reverse('api_country_region', kwargs={'pk': self.country.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should find country2
        self.assertEqual(response.data[0]['name'], 'Second Country')
        
    def test_language_countries(self):
        response = self.client.get(
            reverse('api_country_language', kwargs={'language': 'english'})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both countries have English
        
    def test_search_countries(self):
        response = self.client.get(
            reverse('api_country_search', kwargs={'query': 'Second'})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Second Country')