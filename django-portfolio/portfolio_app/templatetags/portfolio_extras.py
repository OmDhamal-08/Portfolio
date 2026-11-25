from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary by key safely."""
    if dictionary and key in dictionary:
        return dictionary.get(key)
    return None


@register.filter
def rich_text(value):
    """Turn plain content text into safe HTML.

    - Blank lines separate paragraphs.
    - Lines starting with "- " become list items.
    - A short line ending with ":" becomes a small heading.
    Everything is HTML-escaped first, so content files cannot inject markup.
    """
    if not value:
        return ''
    html = []
    in_list = False
    for raw_line in str(value).splitlines():
        line = raw_line.strip()
        if line.startswith('- '):
            if not in_list:
                html.append('<ul>')
                in_list = True
            html.append(f'<li>{escape(line[2:])}</li>')
            continue
        if in_list:
            html.append('</ul>')
            in_list = False
        if not line:
            continue
        if line.endswith(':') and len(line) < 60:
            html.append(f'<h4>{escape(line[:-1])}</h4>')
        else:
            html.append(f'<p>{escape(line)}</p>')
    if in_list:
        html.append('</ul>')
    return mark_safe(''.join(html))
