from django import template
register = template.Library()

@register.filter(name='index_filter')
def index(indexable, i):
    return indexable[i]