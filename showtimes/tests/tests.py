import pytz
from faker import Faker

import pytest
from moviebase.settings import TIME_ZONE
from showtimes.models import Cinema, Screening
from movielist.models import Movie


faker = Faker("pl_PL")
TZ = pytz.timezone(TIME_ZONE)


@pytest.mark.django_db
def test_add_cinema(client):
    cinemas_before = Cinema.objects.count()
    new_cinema = {
        "name": "Abrakadabra",
        "city": "Rzeszow"
    }

    response = client.post('/cinemas/', new_cinema, format='json')

    assert response.status_code == 201
    assert Cinema.objects.count() == cinemas_before + 1
    for key, value in new_cinema.items():
        assert key in response.data
        if isinstance(value, list):
            assert len(response.data[key]) == len(value)
        else:
            assert response.data[key] == value


@pytest.mark.django_db
def test_get_cinema_list(client):
    response = client.get('/cinemas/', format='json')
    assert response.status_code == 200
    assert Cinema.objects.count() == len(response.data)


@pytest.mark.django_db
def test_get_cinema_detail(client, set_up):
    cinema = Cinema.objects.first()
    response = client.get(f"/cinemas/{cinema.pk}/", format='json')
    assert response.status_code == 200
    for field in ("name", "city"):
        assert field in response.data


@pytest.mark.django_db
def test_delete_cinema(client, set_up):
    cinema = Cinema.objects.first()
    response = client.delete(f"/cinemas/{cinema.id}/", format='json')
    assert response.status_code == 204
    cinemas_ids = [cinema.id for cinema in Cinema.objects.all()]
    assert cinema.id not in cinemas_ids


@pytest.mark.django_db
def test_update_cinema(client, set_up):
    cinema = Cinema.objects.first()
    response = client.get(f"/cinemas/{cinema.pk}/", format='json')
    cinema_data = response.data
    new_name = "Anonymous"
    cinema_data["name"] = new_name
    new_city = "Test_city"
    cinema_data["city"] = new_city
    response = client.patch(f"/cinemas/{cinema.pk}/", cinema_data, format='json')
    assert response.status_code == 200
    cinema_updated = Cinema.objects.get(pk=cinema.pk)
    assert cinema_updated.name == "Anonymous"


@pytest.mark.django_db
def test_add_screening(client):
    screenings_count = Screening.objects.count()
    new_screening_data = {
        "cinema": Cinema.objects.first().name,
        "movie": Movie.objects.first().title,
        "date": faker.date_time(tzinfo=TZ).isoformat()
    }

    response = client.post(f"/screenings/", new_screening_data, format='json')
    assert response.status_code == 201
    assert Screening.objects.count() == screenings_count + 1

    new_screening_data["date"] = new_screening_data["date"].replace('+00:00', 'Z')
    for key, value in new_screening_data.items():
        assert key in response.data
        assert response.data[key] == value


@pytest.mark.django_db
def test_get_screening_list(client):
    response = client.get('/screenings/', format='json')
    assert response.status_code == 200
    assert Screening.objects.count() == len(response.data)


@pytest.mark.django_db
def test_get_screening_detail(client, set_up):
    screening = Screening.objects.first()
    response = client.get(f"/screenings/{screening.pk}/", format='json')
    assert response.status_code == 200
    for field in ("movie", "cinema", "date"):
        assert field in response.data


@pytest.mark.django_db
def test_delete_screening(client, set_up):
    screening = Screening.objects.first()
    response = client.delete(f"/screenings/{screening.pk}/", format='json')
    assert response.status_code == 204
    screening_ids = [screening.pk for screening in Screening.objects.all()]
    assert screening.pk not in screening_ids


@pytest.mark.django_db
def test_update_screening(client, set_up):
    screening = Screening.objects.first()
    response = client.get(f"/screenings/{screening.pk}/", format='json')
    screening_data = response.data
    new_cinema = Cinema.objects.last()
    screening_data["cinema"] = new_cinema.name
    response = client.patch(f"/screenings/{screening.pk}/", screening_data, format='json')
    assert response.status_code == 200
    screening_updated = Screening.objects.get(pk=screening.pk)
    assert screening_updated.cinema == new_cinema
