from typing import TYPE_CHECKING, Optional, Tuple
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from app.models import User, Organization
from app.http_errors import forbidden, unauthorized, not_found

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

"""OSS auth

- single organization create if not exist on first create
- user create 
- user login 
"""

class AuthBase:
    """common utilites for auth"""
    db_session: "Session"
    
    def __init__(self, db_session:"Session"):
        self.db_session = db_session
    
    @classmethod
    def stanardized_email(cls, email:str) -> str:
        return email.strip().lower()

    def get_user(self, email: str) -> User:
        try:
            return User.find(self.db_session, 
                             email_address=self.stanardized_email(email))
        except (MultipleResultsFound, NoResultFound) as e:
            not_found(e=e, message=f"User {email} not found")


class CreateUserFlow(AuthBase):
    """create a new user"""

    def create_with_email_password(self,
                                   email_address:str,
                                   password:str) -> User:
        """standard old-school u/p"""
    
    def create_with_email_sso(self,
                              email_address:str) -> User:
        """create using 3rd party auth"""
    

class LogInUserFlow(AuthBase):
    """log in an existing user"""

    def _get_via_email_password(self,
                                email_address:str,
                                password:str) -> User:
        """standard old-school u/p"""
    
    def _get_via_email_sso(self,
                           email_address:str) -> User:
        """log in using 3rd party auth"""


class JWTTokenFlow(AuthBase):

    def get_refresh_token(self,
                          user:User) -> "JWTToken":
        """generates a bare refresh token for a given user"""

    def get_auth_token(self,
                       refresh_token:"JWTToken",
                       org:Optional["Organization"]) -> Tuple["JWTToken", "VisibleToken"]:   
        """generate a detailed token and a matching client-readable object"""

    # password flow only: verify password

    # generate "dumb" refresh jwt token (user)

    # assemble auth token data from user, selected org

    # generate auth jwt token (assembled data)
    