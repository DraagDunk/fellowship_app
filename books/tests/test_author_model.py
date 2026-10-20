import pytest

@pytest.mark.django_db
class TestAuthorModel:

    def test_str_val(self, simple_author):
        assert str(simple_author) == simple_author.name