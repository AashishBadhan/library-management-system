from django import template

register = template.Library()

@register.filter(name="abs")
def absolute_value(value):
    """Return absolute value for numbers; if non-numeric, return unchanged."""
    try:
        return abs(int(value)) if isinstance(value, bool) is False else abs(int(value))
    except (ValueError, TypeError):
        try:
            return abs(float(value))
        except (ValueError, TypeError):
            return value
