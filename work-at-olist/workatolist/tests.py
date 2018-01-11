from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from workatolist.models import Channel

class ApiChannelEmptyTests(TestCase):

    def test_listing_channels(self):
        """
        Test the return of the channels empty
        """
        client = APIClient()
        response = client.get('/channels/')
        assert response.status_code == 200
        self.assertEqual(response.json(), [])

    def test_add_channel(self):
        """
        Insert a new channel
        """
        client = APIClient()
        data = {
            'name': 'walmart',
            'slug': 'walmart'
        }
        response = client.post('/channels/', data)
        assert response.status_code == 201

        response = client.get('/channels/')
        assert response.status_code == 200
        ret_data = response.json()[0]
        self.assertEqual(ret_data['name'], 'walmart')
        self.assertEqual(ret_data['slug'], 'walmart')


class ApiCategoryEmptyTests(TestCase):

    fixtures = ["workatolist/fixtures/channel_walmart.json"]

    def test_list_categories(self):
        """
        Test list of categories empty
        """
        client = APIClient()
        response = client.get('/categories/')
        assert response.status_code == 200
        self.assertEqual(response.json(), [])

    def test_add_category_without_channel(self):
        """
        Insert a new cattegory without channel
        """
        client = APIClient()
        category_data = {
            'name': 'Computers',
            'slug': 'computers',
            'parent': None,
        }
        response = client.post('/categories/', category_data)
        assert response.json()['channel'][0] == 'This field is required.'
        assert response.status_code == 400


class ApiCategoryTests(TestCase):

    fixtures = ["workatolist/fixtures/channel_walmart_and_categories.json"]

    def test_add_category_with_channel(self):
        """
        Insert a new cattegory with channel
        """
        channel = Channel.objects.get(slug='walmart')

        client = APIClient()
        category_data = {
            'name': 'Computers',
            'slug': 'computers',
            'channel': channel.slug,
            'parent': None
        }
        response = client.post('/categories/', category_data)
        assert response.json()['parent'] is None
        assert response.json()['channel'].endswith("/channels/walmart/")
        assert response.status_code == 201

    def test_add_category_with_channel(self):
        """
        Insert a new cattegory with channel and parent
        """
        channel = Channel.objects.get(slug='walmart')

        client = APIClient()
        category_data = {
            'name': 'Computers',
            'slug': 'computers',
            'channel': channel.slug,
            'parent': "accessories",
        }
        response = client.post('/categories/', category_data)
        assert response.json()['parent'] is not None
        assert response.json()['channel'].endswith("/channels/walmart/")
        assert response.json()['parent'].endswith("/categories/accessories/")
        assert response.status_code == 201

