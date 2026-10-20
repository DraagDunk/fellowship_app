import pytest

from ..models import Author, Genre

@pytest.fixture
def simple_author():
    return Author.objects.create(name="Author McAuthorface")

@pytest.fixture
def simple_genre():
    return Genre.objects.create(name="Simple")