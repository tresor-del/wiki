from django import template

register = template.Library()

@register.filter(name='strip_lines')
def strip_lines(value):
    """Applique .strip() sur chaque ligne d'un texte"""
    if isinstance(value, str):
        return "\n".join(line.strip() for line in value.splitlines())
    return value
