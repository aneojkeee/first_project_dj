import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from students.models import Course

# URL_LIST = reverse('courses-list')
# URL_DETAIL = reverse('courses-detail', args=[1])

@pytest.mark.django_db
def test_get_one_course(api_client, course_factory):
    url = reverse("courses-list")
    courses = course_factory(_quantity=10)
    resp = api_client.get(url)
    id = resp.data[0]['id']
    name = resp.data[0]['name']
    url2 =url + f'{id}/'
    response = api_client.get(url2)
    assert response.data['name'] == name

@pytest.mark.django_db
def test_get_all_courses(api_client, course_factory):
    url = reverse("courses-list")
    courses = course_factory(_quantity=10)
    resp = api_client.get(url)
    assert len(resp.data) == 10

@pytest.mark.django_db
def test_filter_by_id(api_client, course_factory):
    url = reverse("courses-list")
    courses = course_factory(_quantity=10)
    response = api_client.get(url)
    all_courses = response.data
    test_course_id = all_courses[1]['id']
    filter_id = api_client.get(url, {'id': test_course_id})
    assert filter_id.status_code == 200
    assert filter_id.data[0]['id'] == test_course_id
#
@pytest.mark.django_db
def test_filter_by_name(api_client, course_factory):
    url = reverse("courses-list")
    courses = course_factory(_quantity=10)
    response = api_client.get(url)
    all_courses = response.data
    test_course_name = all_courses[1]['name']
    filter_name = api_client.get(url, {'name': test_course_name})
    assert filter_name.data[0]['name'] == test_course_name
    assert filter_name.status_code == 200


@pytest.mark.django_db
def test_create_course(api_client):
    payload = {
        'name': 'Test_course2'
    }
    url = reverse("courses-list")
    resp = api_client.post(url, data=payload, format='json')
    assert resp.status_code == 201

@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    url = reverse("courses-list")
    course_factory(_quantity=2, name='test_name')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data[0]['name'] == 'test_name'
    id = response.data[0]['id']
    url_detail = reverse("courses-detail", args=[id])
    update_data = {'name': 'new_test_name', }
    resp = api_client.patch(url_detail, data=update_data, format='json')
    assert resp.status_code == 200
    assert resp.data['name'] == 'new_test_name'

@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    url = reverse("courses-list")
    course_factory(_quantity=10)
    resp = api_client.get(url)
    id = resp.data[0]['id']
    url_detail = reverse("courses-detail", args=[id])
    resp_json = resp.json()
    assert len(resp_json) == 10
    api_client.delete(url_detail)
    response = api_client.get(url)
    response_json = response.json()
    assert len(response_json) == 9