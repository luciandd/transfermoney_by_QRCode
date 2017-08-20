from authentications.utils import check_permissions_by_user
from django import template

register = template.Library()


@register.filter(name='has_permission_name')
def has_permission_name(user, group_name):
    """
    Verify User have permission to see menu
    """
    return check_permissions_by_user(user, group_name)