from pytest import mark as m, raises

from app.settings import settings
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
