from django.urls import path, reverse, include, resolve
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class ManagingExpectationViewTests(APITestCase):
    login_url = reverse('expectations:user-login')
    expectation_url = reverse('expectations:get-expectations_list')
    post_expectation_url = reverse('expectations:create_managing_expectations')
    update_and_delete_expectation_url = reverse('expectations:update_or_delete_managing_expectations', args=[1])

    def setUp(self):
        self.client = APIClient()
        url = reverse('expectations:user_registration')
        data = {"email": "admin1@gmail.com", "password": "admin1234"}
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        resp = self.client.post(self.login_url,  {"email": "admin1@gmail.com", "password": "admin1234"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        self.jwt_token = resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt_token)

    def test_get_user_authenticated(self):
        response = self.client.get(self.expectation_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.expectation_url)
        self.assertEquals(response.status_code, 401)

    def test_post_update_and_delete_expectation_user_authenticated(self):
        post_data = {"expected_role": "backend developement", "expected_finished_time": "2022-02-01T00:00:00+00:00"}
        post_response = self.client.post(self.post_expectation_url, post_data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        updated_date = {"expected_role": "frontend developement", "expected_finished_time": "2022-02-01T00:00:00+00:00"}
        updated_response = self.client.patch(self.update_and_delete_expectation_url, updated_date, format='json')
        self.assertEqual(updated_response.status_code, status.HTTP_201_CREATED)

        deleted_response = self.client.delete(self.update_and_delete_expectation_url)
        self.assertEqual(deleted_response.status_code, status.HTTP_200_OK)

    def test_post_update_and_delete_expectation_user_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        post_data = {"expected_role": "backend developement", "expected_finished_time": "2022-02-01T00:00:00+00:00"}
        post_response = self.client.post(self.post_expectation_url, post_data, format='json')
        self.assertEqual(post_response.status_code, 401)

        updated_date = {"expected_role": "frontend developement", "expected_finished_time": "2022-02-01T00:00:00+00:00"}
        updated_response = self.client.patch(self.update_and_delete_expectation_url, updated_date, format='json')
        self.assertEqual(updated_response.status_code, 401)

        deleted_response = self.client.delete(self.update_and_delete_expectation_url)
        self.assertEqual(deleted_response.status_code, 401)

