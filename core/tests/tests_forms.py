import faker
# import hypothesis
# import hypothesis.strategies as st
import pytest

import core.forms


fake = faker.Faker()


@pytest.mark.django_db
def test_new_user_form():
    test_form = core.forms.SignUpForm(data={
        'username': fake.user_name(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'password1': 't3stpassw0rd',
        'password2': 't3stpassw0rd',
        'terms_accepted': True,
    })

    assert test_form.is_valid()
    test_form.save()

def test_quote_urls():
    EXAMPLES = (
        ('http://alabama.gov', '"http://alabama.gov"'),
        ('a b http://alabama.gov c d', 'a b "http://alabama.gov" c d'),
        ('a b "http://alabama.gov" c d', 'a b "http://alabama.gov" c d'),
    )

    for in_query, out_query in EXAMPLES:
        assert core.forms.quote_urls(in_query) == out_query