from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary by key safely."""
    if dictionary and key in dictionary:
        return dictionary.get(key)
    return None
