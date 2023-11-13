from django import template

register = template.Library()

@register.filter
def is_not_check_count(array):
    counter = 0
    for i in array:
        if not i.is_check:
            counter += 1
    return counter