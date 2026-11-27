from dataclasses import asdict, dataclass, fields
import re

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.crypto import force_bytes
from django.utils.http import urlsafe_base64_encode

from clubs.models import ClubEmailTemplate, ClubMembership
from fellowship_app import settings

EMAIL_REPLACE_TOKEN_REGULAR_EXPRESSION = re.compile(r"\[\[([A-Za-z_]+)\]\]")

@dataclass(frozen=True)
class ClubWelcomeEmailTemplateTokens:
    FULL_NAME: str
    FIRST_NAME: str
    CLUB_NAME: str
    SET_PASSWORD_URL: str

    @classmethod
    def names(cls) -> list[str]:
        return [f.name for f in fields(cls)]

@dataclass(frozen=True)
class ClubWelcomeEmailTemplateContext:
    membership: ClubMembership

    @property
    def tokens(self) -> ClubWelcomeEmailTemplateTokens:
        return ClubWelcomeEmailTemplateTokens(
            FULL_NAME=self.membership.person.get_full_name(),
            FIRST_NAME=self.membership.person.first_name,
            CLUB_NAME=self.membership.club.name,
            SET_PASSWORD_URL=self._build_password_reset_url(self.membership.person)
        )

    def _build_password_reset_url(self, member):
        uid = urlsafe_base64_encode(force_bytes(member.pk))
        token = default_token_generator.make_token(member)
        path = reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
        return f"{settings.APP_BASE_URL.rstrip('/')}{path}"

class UnknownTokenError(Exception):
    def __init__(self, token):
        self.token = token
        super().__init__(f"Unknown token [[{token}]]")

def _render_text(text: str, tokens: ClubWelcomeEmailTemplateTokens):
    values = asdict(tokens)
    def sub(match):
        key = match.group(1)
        if key not in values:
            raise UnknownTokenError(key)
        return str(values[key])

    return EMAIL_REPLACE_TOKEN_REGULAR_EXPRESSION.sub(sub, text)

def send_welcome_email(membership: ClubMembership):
    context = ClubWelcomeEmailTemplateContext(membership)
    tokens = context.tokens

    template = ClubEmailTemplate.objects.filter(
        club=membership.club,
        template_type=ClubEmailTemplate.ClubEmailTemplateType.WELCOME
    ).first()

    subject = _render_text(template.subject, tokens)
    body = _render_text(template.body, tokens)

    send_mail(
        subject=subject,
        message=body,
        from_email=settings.DEFAULT_EMAIL_SENDER,
        recipient_list=[membership.person.email],
        fail_silently=False
    )
