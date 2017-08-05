from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


__all__ = (
    'comment_create',
)


# @require_POST
# @login_required
def comment_create(request, post_pk):
    pass