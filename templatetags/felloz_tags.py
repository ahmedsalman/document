from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django import template
from django.template import Library, Node
from django.template import Variable
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe


register = template.Library()

@stringfilter
def child_comment( object_pk , object_id ):
    y = object_id
    x = str( object_pk )
    if x == y:
        return True
    return False

register.filter('child_comment', child_comment)




register = template.Library()

@register.filter
@stringfilter
def trim(value):
    return value.strip()
