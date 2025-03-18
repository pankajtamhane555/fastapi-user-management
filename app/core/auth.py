from oso import Oso
from fastapi import Depends, HTTPException, status
from app.api.v1.dependencies import get_current_user
from app.models.user import User

oso = Oso()

# Define the authorization rules in Polar
POLAR_RULES = """
# Allow admins to do anything
allow(user: User, _action, _resource) if user.role = "admin";

# Users can view and edit their own profile
allow(user: User, "read", target: User) if user.id = target.id;
allow(user: User, "update", target: User) if user.id = target.id;
allow(user: User, "delete", target: User) if user.id = target.id;

# Users can view basic information about other users
allow(user: User, "list", "users") if user.role = "admin";
"""

def init_oso():
    oso.load_str(POLAR_RULES)
    oso.register_class(User)

init_oso()

def authorize(action: str, resource: any = None):
    async def authorization_dependency(current_user: User = Depends(get_current_user)):
        if not oso.is_allowed(current_user, action, resource):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return authorization_dependency
