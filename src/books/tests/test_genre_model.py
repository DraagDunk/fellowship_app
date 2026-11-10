import pytest

@pytest.mark.django_db
class TestGenreModel:

    def test_str_val(self, simple_genre):
        assert str(simple_genre) == simple_genre.name
