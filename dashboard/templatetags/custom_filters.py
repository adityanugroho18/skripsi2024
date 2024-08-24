import locale
from django import template

register = template.Library()

@register.filter()
def currency_format(value):
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # Set to US locale for formatting
        formatted_value = locale.format_string("%0.2f", float(value), grouping=True)
        formatted_value = formatted_value.replace(',', 'temp').replace('.', ',').replace('temp', '.')
        return formatted_value
    except (ValueError, TypeError):
        return value
