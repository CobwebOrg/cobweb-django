import faker
import hypothesis
import hypothesis.strategies as st
import pytest
from django.urls import reverse

from core.forms import SignUpForm


fake = faker.Faker()


@pytest.mark.django_db
def test_new_user_form():
    test_form = SignUpForm(data={
        'username': fake.user_name(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'password1': 't3stpassw0rd',
        'password2': 't3stpassw0rd',
    })

    assert test_form.is_valid()
    test_form.save()
