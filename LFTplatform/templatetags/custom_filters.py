from django import template

register = template.Library()


@register.filter(name="get_item")
def get_item(dictionary, key):
    if dictionary.get(str(key)) is not None:
        return dictionary.get(str(key))
    raise ValueError("get_item error")


@register.filter(name="get_specs")
def get_specs(dictionary, key):
    if key.data["value"] is not None:
        return dictionary.get(key.data["value"])
