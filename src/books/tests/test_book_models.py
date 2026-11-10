import pytest

from ..models import BookCore, BookVersion
from ..models.shared import LanguageCodes

@pytest.fixture
def simple_bookcore(simple_author, simple_genre):
    core = BookCore.objects.create(
        series_number=1
    )
    core.author.set([simple_author])
    core.genres.set([simple_genre])
    return core

@pytest.fixture
def simple_bookversion(simple_bookcore):
    return BookVersion.objects.create(
        original_language=True,
        title="Totally title",
        description="Very funnay",
        language=LanguageCodes.ENGLISH,
        core=simple_bookcore
    )

@pytest.mark.django_db
class TestBookCoreModel:

    def test_str_val_no_original(self, simple_bookcore):
        assert str(simple_bookcore) == f"Unknown book ({simple_bookcore.pk})"

    def test_str_val_with_original(self, simple_bookversion, simple_bookcore):
        assert str(simple_bookcore) == simple_bookversion.title