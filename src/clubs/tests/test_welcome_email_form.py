from django.forms import ValidationError
import pytest

from clubs.forms.club import ClubWelcomeEmailForm

@pytest.mark.parametrize("field", ["subject", "body"])
@pytest.mark.parametrize("bad", [
    "{{ member.password }}",
    "{% include 'x' %}",
    "{# c #}",
    "[[NOPE]]",
    "[[first_name]]"
])
def test_form_rejects_bad_input(field, bad):
    data = {"subject": "ok", "body": "ok"}
    data[field] = bad
    form = ClubWelcomeEmailForm(data=data)
    assert not form.is_valid()
    assert field in form.errors

def test_invalid_token_in_error():
    data = {"subject": "[[NOPE]]", "body": "OK"}
    form = ClubWelcomeEmailForm(data=data)
    assert not form.is_valid()
    assert "NOPE" in form.errors["subject"][0]

def test_valid_form_is_accepted():
    data = {"subject": "Hej [[FIRST_NAME]]", "body": "Velkommen til [[CLUB_NAME]]"}
    form = ClubWelcomeEmailForm(data=data)
    assert form.is_valid(), form.errors
    assert form.cleaned_data["subject"] == "Hej [[FIRST_NAME]]"

def test_accept_normal_square_bracket():
    data = {"subject": "Penge i [DKK]", "body": "Vores penge er i [DKK]"}
    form = ClubWelcomeEmailForm(data=data)
    assert form.is_valid(), form.errors
