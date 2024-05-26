from pytest import mark as m, raises
from unittest import mock

from app.settings import settings
from app.models.user import User
from app.controllers.magic_link import MagicLinkFlow


@m.describe("when resetting passwords with a magic link")
class TestMagicLink:

    @m.it("requires smtp creds")
    def test_fails_without_smtp_creds(self, db_session):
        host_orig = settings.smtp_email_host
        try:
            settings.smtp_email_host = None
            with raises(NotImplementedError):
                magic_link = MagicLinkFlow(db_session)
                magic_link.send_magic_link(email_address="some@email.com")
        finally:
            settings.smtp_email_host = host_orig

    @m.it("attempts to send an email")
    def test_sends_email(self, db_session):
        user = User(email_address="some@user.com", first_name="Some", last_name="User").create(db_session)
        old_settings = settings.model_dump(exclude_none=True)
        settings.smtp_email_host = "smtp.gmail.com"
        settings.smtp_email_port = 587
        settings.smtp_email_user = "emailio@test.com"
        settings.smtp_email_password = "password"
        try:
            with mock.patch("app.controllers.magic_link.smtplib.SMTP") as smtp_mock:
                magic_link = MagicLinkFlow(db_session)
                magic_link.send_magic_link(email_address=user.email_address)
                smtp_mock.assert_called_once_with(settings.smtp_email_host, settings.smtp_email_port)
                smtp_mock.return_value.starttls.assert_called_once()
                smtp_mock.return_value.login.assert_called_once_with(settings.smtp_email_user, settings.smtp_email_password)
                smtp_mock.return_value.sendmail.assert_called_once()
        finally:
            for k,v in old_settings.items():
                setattr(settings, k, v)