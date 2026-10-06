from django.db import models
from django.utils.translation import gettext_lazy as _

class LanguageCodes(models.TextChoices):
        DANISH = "da", _("Danish")
        ENGLISH = "en", _("English")