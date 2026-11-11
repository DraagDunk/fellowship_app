import pytest

from ..models import SeriesCore, SeriesVersion
from ..models.shared import LanguageCodes

@pytest.fixture
def simple_seriescore(simple_author):
    core = SeriesCore.objects.create()
    core.author.add(simple_author)
    return core

@pytest.fixture
def simple_seriesversion(simple_seriescore):
    return SeriesVersion.objects.create(
        name="Simple series",
        description="Very very simple",
        language=LanguageCodes.ENGLISH,
        original_language=True,
        core=simple_seriescore
    )

@pytest.mark.django_db
class TestSeriesCoreModel:

    def test_str_val_no_versions(self, simple_seriescore):
        assert str(simple_seriescore) == f"Unknown series ({simple_seriescore.pk})"

    def test_str_val_with_version(self, simple_seriescore, simple_seriesversion):
        assert str(simple_seriescore) == simple_seriesversion.name


@pytest.mark.django_db
class TestSeriesVersionModel:

    def test_str_val(self, simple_seriesversion):
        assert str(simple_seriesversion) == simple_seriesversion.name