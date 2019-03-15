from django.test import TestCase
from locations.models import Session, Location
from django.db.utils import IntegrityError
import string
import secrets

# TODO: Test get_location


class SessionModelTestCase(TestCase):
    """Tests 'Session' database model."""
    def setUp(self):
        self.code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        Session.objects.create(
            name='Test Name',
            city='Cairo, Egypt',
            place_type='Cafe',
            code=self.code)

    def test_session_model(self):
        self.assertTrue(Session.objects.get(name='Test Name'))
        # Assert meetings codes are unique
        self.assertRaises(
            IntegrityError,
            lambda: Session.objects.create(name='any', city='any',
                                           place_type='Cafe', code=self.code)
        )


class CreateSessionTestCase(TestCase):
    """Tests creating a new session through user interface."""
    def test_create_session(self):
        meeting_name, place_type, city = 'Test Name', 'Cafe', 'Cairo, Egypt'
        self.client.post('/locations/create_session/',
                         data={
                             'meeting_name': meeting_name,
                             'place_type': place_type,
                             'city': city
                         })
        self.assertTrue(Session.objects.get(name='Test Name'))


class LocationModelTestCase(TestCase):
    """
    Assert model can accept different locations and associate them
    with a session.
    """
    def setUp(self):
        code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        self.test_session = Session.objects.create(
            name='Test Name',
            city='Cairo, Egypt',
            place_type='Cafe',
            code=code)

    def test_location_model(self):
        self.assertTrue(Location.objects.create(longitude='31.300546',
                                                latitude='30.011927',
                                                session=self.test_session))
        self.assertTrue(Location.objects.create(longitude='-79.396813',
                                                latitude='43.653946',
                                                session=self.test_session))


class AddLocationTestCase(TestCase):
    """
    Assert accepting different locations and associating them
    with a session through views method.
    Assumption: the location passed by client (if exists) is always
    an object in the shape {lat:'', lng:'', code:''}.
    """
    def setUp(self):
        self.code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        Session.objects.create(
            name='Test Name',
            city='Cairo, Egypt',
            place_type='Cafe',
            code=self.code)

    def test_add_location(self):
        self.client.post('/locations/add_location',
                         data={
                             'lat': '30.011927',
                             'lng': '31.300546',
                             'code': self.code
                         })
        self.assertTrue(Location.objects.get(latitude='30.011927'))
