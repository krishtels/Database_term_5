from django.template.defaulttags import register


@register.filter(name='get_dict_value')
def get_dict_value(dictionary, key):
    return dictionary.get(key)


@register.filter(name='get_list_value')
def get_list_value(list_obj, num):
    return list_obj[num]


# @register.filter(name='is_member')
# def is_member(user, group):
#     return user.groups.filter(name=group).exists()
#
