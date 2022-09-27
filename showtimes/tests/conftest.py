import os
import sys

from django.utils import timezone
import pytest
from rest_framework.test import APIClient

from movielist.models import Person, Movie
from showtimes.models import Cinema, Screening
from showtimes.tests.utils import faker

sys.path.append(os.path.dirname(__file__))


@pytest.fixture
def client():
    client = APIClient()
    return client


@pytest.fixture
def set_up():
    for _ in range(5):
        director = Person.objects.create(name=faker.name())
        cinema = Cinema.objects.create(name=faker.name())
        movie = Movie.objects.create(title=faker.name(), description='Test no.1', year=1989, director=director)
        Screening.objects.create(date=timezone.now(), cinema=cinema, movie=movie)
