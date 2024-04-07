from rest_framework.permissions import BasePermission 

class CustomPermission(BasePermission):
    # Implement custom permission logic here
    def has_permission(self, request, view):
        if request.user.is_superuser:
            # Allow superusers to perform any action
            return True
                                     # 👇 this is your Group Name            
        if request.user.groups.filter(name='Group_User').exists():
            # Allow users in the specific group to view data
            if view.action in ['retrieve', 'list']:
                return True

        return False