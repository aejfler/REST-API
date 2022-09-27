import datetime
from faker import Faker
from more_itertools import sample
from random import randrange
from movielist.models import Movie
from showtimes.models import Screening, Cinema
from showtimes.tests.tests import TZ

faker = Faker("pl_PL")


def random_movies():
    movies = list(Movie.objects.all())
    return sample(movies, 3)


def add_screenings(cinema):
    movies = random_movies()
    for movie in movies:
        Screening.objects.create(cinema=cinema, movie=movie, date=faker.date_time(tzinfo=TZ))


def fake_cinema_data():
    cinema_data = {
        "name": faker.name(),
        "city": faker.city(),
    }
    return cinema_data


def create_fake_cinema():
    cinema = Cinema.objects.create(**fake_cinema_data())
    add_screenings(cinema)


def random_date():
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2022, 12, 31)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date


def fake_screening_data():
    screening_data = {
        "date": random_date(),
        "cinema": faker.sentence(nb_words=2),
        "movie": faker.sentence(nb_words=3),
    }
    return screening_data
