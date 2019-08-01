from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from itou.prescribers.models import Prescriber
from itou.siae.factories import SiaeFactory
from itou.siae.models import Siae
from itou.utils.mocks.geocoding import BAN_GEOCODING_API_RESULT_MOCK
from itou.utils.mocks.siret import API_INSEE_SIRET_RESULT_MOCK


class SignupTest(TestCase):

    def test_allauth_signup_url_override(self):
        """Ensure that the default allauth signup URL is unreachable."""
        ALLAUTH_SIGNUP_URL = reverse('account_signup')
        self.assertEqual(ALLAUTH_SIGNUP_URL, '/accounts/signup/')
        response = self.client.get(ALLAUTH_SIGNUP_URL)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(ALLAUTH_SIGNUP_URL, data={'foo': 'bar'})
        self.assertEqual(response.status_code, 302)

    @mock.patch('itou.utils.siret.call_insee_api', return_value=API_INSEE_SIRET_RESULT_MOCK)
    @mock.patch('itou.utils.geocoding.call_ban_geocoding_api', return_value=BAN_GEOCODING_API_RESULT_MOCK)
    def test_prescriber_signup(self, mock_call_ban_geocoding_api, mock_call_insee_api):
        """Prescriber signup."""

        url = reverse('accounts:prescriber_signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        post_data = {
            'first_name': "John",
            'last_name': "Doe",
            'email': "john.doe@prescriber.com",
            'siret': "12000015300011",
            'password1': '!*p4ssw0rd123-',
            'password2': '!*p4ssw0rd123-',
        }
        response = self.client.post(url, data=post_data)
        mock_call_insee_api.assert_called_once_with(post_data['siret'])
        mock_call_ban_geocoding_api.assert_called_once()
        self.assertEqual(response.status_code, 302)

        user = get_user_model().objects.get(email=post_data['email'])
        self.assertFalse(user.is_job_seeker)
        self.assertTrue(user.is_prescriber)
        self.assertFalse(user.is_siae_staff)

        prescriber = Prescriber.objects.get(siret=post_data['siret'])
        self.assertIn(user, prescriber.members.all())
        self.assertEqual(1, prescriber.members.count())

        self.assertIn(prescriber, user.prescriber_set.all())
        self.assertEqual(1, user.prescriber_set.count())

        membership = user.prescribermembership_set.get(prescriber=prescriber)
        self.assertTrue(membership.is_prescriber_admin)

    def test_siae_signup(self):
        """SIAE signup."""

        siae = SiaeFactory()

        url = reverse('accounts:siae_signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        post_data = {
            'first_name': "John",
            'last_name': "Doe",
            'email': "john.doe@siae.com",
            'siret': siae.siret,
            'password1': '!*p4ssw0rd123-',
            'password2': '!*p4ssw0rd123-',
        }
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, 302)

        user = get_user_model().objects.get(email=post_data['email'])
        self.assertFalse(user.is_job_seeker)
        self.assertFalse(user.is_prescriber)
        self.assertTrue(user.is_siae_staff)

        siae = Siae.active_objects.get(siret=post_data['siret'])
        self.assertIn(user, siae.members.all())
        self.assertEqual(1, siae.members.count())

        membership = user.siaemembership_set.get(siae=siae)
        self.assertTrue(membership.is_siae_admin)

    def test_job_seeker_signup(self):
        """Job-seeker signup."""

        url = reverse('accounts:job_seeker_signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        post_data = {
            'first_name': "John",
            'last_name': "Doe",
            'email': "john.doe@siae.com",
            'password1': '!*p4ssw0rd123-',
            'password2': '!*p4ssw0rd123-',
        }
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, 302)

        user = get_user_model().objects.get(email=post_data['email'])
        self.assertTrue(user.is_job_seeker)
        self.assertFalse(user.is_prescriber)
        self.assertFalse(user.is_siae_staff)