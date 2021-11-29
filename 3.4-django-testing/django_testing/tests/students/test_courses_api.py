import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from students.models import Course, Student


@pytest.mark.django_db
def test_get_1_course(api_client, course_factory):
    url = reverse("courses-detail", kwargs={'pk': 1})
    first_course = course_factory(_quantity=5)
    result = api_client.get(url)
    assert result.status_code == HTTP_200_OK
    result_json = result.json()
    assert result_json["id"] == 1


@pytest.mark.django_db
def test_get_list_courses(api_client, course_factory):
    url = reverse("courses-list")
    courses = course_factory(_quantity=5)
    result = api_client.get(url)
    assert result.status_code == HTTP_200_OK
    result_json = result.json()
    assert len(result_json) == 5


@pytest.mark.django_db
def test_create_courses(api_client):
    data = {'name': 'Джанго Разработчик'}
    url = reverse("courses-list")
    result = api_client.post(url, data)
    assert result.status_code == HTTP_201_CREATED


@pytest.mark.django_db
def test_update_courses(api_client, course_factory):
    data = {'name': 'Джанго Разработчик'}
    url = reverse("courses-detail", kwargs={'pk': 14})
    course_factory(_quantity=5)
    result = api_client.patch(url, data=data)
    assert result.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    url = reverse("courses-detail", kwargs={'pk': 19})
    course_factory(_quantity=5)
    result = api_client.delete(url)
    assert result.status_code == HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_get_course_by_id(api_client, course_factory):
    id = 23
    url = f'{reverse("courses-list")}?id={id}'
    course_factory(_quantity=5)
    result = api_client.get(url)
    assert result.status_code == HTTP_200_OK
    obj = result.json()
    assert obj[0]['id'] == id


@pytest.mark.django_db
def test_get_course_by_name(api_client):
    filter_name = 'Couser JavaScript'
    url = f'{reverse("courses-list")}?name={filter_name}'
    courses = Course.objects.bulk_create([
        Course(name="Course Django"),
        Course(name="Course HTML"),
        Course(name="Couser Python"),
        Course(name=f"{filter_name}")
    ])
    result = api_client.get(url)
    assert result.status_code == HTTP_200_OK
    results = result.json()
    for course in results: assert course["name"] == filter_name


@pytest.mark.parametrize(
    ["count", "status"],
    (
        (1, HTTP_201_CREATED),
        (2, HTTP_201_CREATED),
        (3, HTTP_400_BAD_REQUEST),
    )
)
@pytest.mark.django_db
def test_with_max_students_per_course(api_client, settings, student_factory, count, status):
    settings.MAX_STUDENTS_PER_COURSE = 2
    url = reverse("courses-list")
    students = student_factory(_quantity=count)
    data = {
        "name": "Test Course",
        "students": [x.id for x in students]
    }
    resp = api_client.post(url, data)
    assert resp.status_code == status


