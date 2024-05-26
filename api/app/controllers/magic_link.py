from typing import TYPE_CHECKING, Tuple
from secrets import token_urlsafe
from base64 import b64encode
from pathlib import Path
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from app.logger import get_logger
from app.settings import settings
from app.models.user import User
from app.models.magic_link import MagicLink
from app.controllers.mixins.auth_mixin import AuthMixin
from app.controllers.mixins.password_mixin import PasswordMixin

if TYPE_CHECKING:
    from uuid import UUID

logger = get_logger(__name__)


class MagicLinkFlow(AuthMixin, PasswordMixin):
    """create, store, and validate magic links"""

    def send_magic_link(self, email_address: str):
        """send a magic link to the user"""
        if not self._validate_email_settings():
            logger.error("cannot send magic link, email settings not configured")
            raise NotImplementedError("email settings are not configured")
        logger.info("requested magic link for email %s", email_address)
        try:
            user = User.read(
                self.db_session, email_address=self.standardized_email(email_address)
            )
        except (NoResultFound, MultipleResultsFound):
            logger.error("user not found for email %s", email_address)
            return
        raw_password = token_urlsafe(16)
        slug = self._make_slug(user.id, raw_password)
        logger.debug("removing all existing magic links for user %s", user.id)
        _ = MagicLink.clear_for_user(self.db_session, user.uid)
        logger.debug("creating magic link for user %s", user.id)
        _ = MagicLink(
            user_uid=user.uid,
            token_hash=self.password_context.hash(raw_password),
        ).create(self.db_session)
        logger.info("new magic link created for user %s", user.id)
        self.send_email(email_address, slug)
        logger.info("magic link sent to %s", email_address)

    def _make_slug(cls, user_uid: "UUID", raw_password: str) -> str:
        """generate a magic link slug"""
        decoded = f"{user_uid}:{raw_password}"
        return b64encode(decoded.encode()).decode()

    def send_email(self, email_address: str, slug: str):
        """send the magic link to the user"""
        logger.info("sending magic link to %s", email_address)
        msg = MIMEMultipart()
        msg["From"] = settings.smtp_email_user
        msg["To"] = email_address
        msg["Subject"] = "Reset your LangStory password"
        text, html = self._get_templates()
        link = f"{settings.canonical_url}/auth/magic-link/{slug}"
        msg.attach(MIMEText(text.format(link=link), "plain"))
        msg.attach(MIMEText(html.format(link=link), "html"))

        mailserver = smtplib.SMTP(settings.smtp_email_host, settings.smtp_email_port)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        try:
            logger.debug("logging into smtp server...")
            mailserver.login(settings.smtp_email_user, settings.smtp_email_password)
            logger.debug("logged in. Sending email to %s...", email_address)
            mailserver.sendmail(
                settings.smtp_email_user, email_address, msg.as_string()
            )
            logger.debug("Sent.")
        finally:
            mailserver.quit()

    def _get_templates(self) -> Tuple[str, str]:
        templates_dir = Path(__file__).parent.parent / "templates"
        text = (templates_dir / "magic_link.txt").read_text()
        html = (templates_dir / "magic_link.html").read_text()
        return text, html

    def _validate_email_settings(cls) -> bool:
        """for email to work settings needs to have email creds"""
        for key in [
            "smtp_email_host",
            "smtp_email_port",
            "smtp_email_user",
            "smtp_email_password",
        ]:
            if not getattr(settings, key):
                logger.error("missing email setting %s, cannot send email", key)
                return False
        return True