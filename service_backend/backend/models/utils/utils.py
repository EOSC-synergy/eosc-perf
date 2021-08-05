"""Utils subpackage with mixins and tools to extend models.
"""
from . import HasCreationDate, users


class HasCreationDetails(
    HasCreationDate, users.HasCreationUser
):
    """Mixin that adds creation details utils."""
    pass
