
from app.models import User, Organization
from app.http_errors import forbidden, unauthorized, not_found

class LoginFlow:
    """all things for the control flow of logging in a user"""

    # get user from email
    def get_user(self, email: str) -> User:
        try:
            sanitized = email.strip().lower()
            return User.get(email_address=sanitized)
        except User.DoesNotExist as e:
            not_found(e=e, message=f"User {email} not found")

    # password flow only: verify password

    # generate "dumb" refresh jwt token (user)

    # assemble auth token data from user, selected org

    # generate auth jwt token (assembled data)
    
    # lazy org selection/creation (selected/createable org)
    def lazy_select_or_create_org(self,
                                  user: User, 
                                  candidate_org: dict) -> Organization:
        """select or create an organization based on the candidate org data"""
        if id_ := candidate_org.get('id'):
            try:
                org = Organization.get(id_)
                assert org in user.organizations, "Organization not in user's organizations"
                return org
            except (AssertionError, Organization.DoesNotExist) as e:
                not_found(e=e, message=f"Organization {id_} not found") 
        org = Organization.create(**candidate_org)
        user.organizations.add(org)
        return org