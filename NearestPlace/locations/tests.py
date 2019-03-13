from django.test import TestCase
from locations.models import Session
import string, secrets


class SessionModelTestCase(TestCase):
    """Tests 'Session' database model."""
    def setUp(self):
        code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        Session.objects.create(
            name='weird8has%%name',
            city='Cairo, Egypt',
            place_type='Cafe',
            code=code)

    def test_session_model(self):
        self.assertTrue(Session.objects.get(name='weird8has%%name'))


class CreateSessionTestCase(TestCase):
    # TODO: Add session with un-valid city/place type
    # TODO: Ensure meeting name is unique
    """Tests creating a new session through user interface."""
    def test_create_session(self):
        meeting_name, place_type, city = 'weird8has%&name', 'Cafe', 'Cairo, Egypt'
        self.client.post('/locations/create_session/',
                         data={
                             'meeting_name': meeting_name,
                             'place_type': place_type,
                             'city': city
                         })
        self.assertTrue(Session.objects.get(name='weird8has%&name'))
