import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def student_factory():
    def factory(**kwargs):
        return baker.make('Student', **kwargs)
    return factory

@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make('Course', **kwargs, make_m2m=True)
    return factory