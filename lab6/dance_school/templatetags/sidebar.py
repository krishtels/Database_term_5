from django import template


register = template.Library()


@register.inclusion_tag('dance_school/dancer_sidebar.html', name='dancer_sidebar')
def dancer_sidebar(user):
    return {'user': user}



