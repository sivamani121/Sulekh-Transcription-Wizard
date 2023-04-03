from django import template
register = template.Library()

@register.filter(name='index_filter')
def index(indexable, i):
    return indexable[i]
@register.filter(name='index_filter2')
def index2(indexable, s):
    a,b = map(int,s.strip().split(':'))
    return indexable[a][b]