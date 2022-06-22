from textwrap import wrap

import textile
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def multiply(value, arg):
    """will multiple value and arg and return the product"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        # if an error is encountered, just return 'value'
        return value


@register.filter
def nz(value, arg="---"):
    """if a value is equal to None, this function will return arg instead"""
    if value is None or value == "":
        return arg
    else:
        return value


@register.filter
def nmissing(value):
    """if a value is equal to None, this function will return arg instead"""
    if value is None or value == "":
        return '<span class="red-font" style="font-size: large">MISSING</span>'
    else:
        return value


@register.filter
def zero2val(value, arg):
    """if a value is equal to zero, this function will return arg instead"""
    # weed out any possibility of errors
    try:
        float(value) == 0
    # if not able to cast, then just return 'value'
    except (ValueError, TypeError):
        # print("val={},arg={}".format(value, arg))
        return value
    else:
        #
        if float(value) == 0:
            return arg
        else:
            return value


@register.filter
def divide(value, arg):
    try:
        float(value)
    except (TypeError, ValueError):
        return 0
    else:
        try:
            return float(nz(value, 0)) / float(arg)
        except (ZeroDivisionError):
            return 0


@register.filter
def percentage(value, arg=2):
    try:
        float(value)
    except (TypeError, ValueError):
        return "0%"
    else:
        return format(value, ".{}%".format(arg))


@register.filter
def subtract(value, arg):
    try:
        float(value)
        float(arg)
    except (TypeError, ValueError):
        return "n/a"
    else:
        return float(value) - float(arg)


@register.filter
def timedelta(value, arg):
    """the difference of two datetime objects in days"""
    return (value - arg).days


@register.filter
def tostring(value):
    """casts 'value' into a str """
    return str(value)


@register.filter
def tohtml(value):
    '''converts basic text to html '''
    try:
        value = str(value)
        # if not able to cast, then just return 'value'
    except (ValueError, TypeError):
        return value
    else:
        return mark_safe(textile.textile(value))


@register.filter
def html_to_text(value):
    val = value.replace("</p>", "\n").replace("<p>", "").replace("<p.*\">", "")
    return val


@register.filter
def currency(value, with_sign=False):
    """returns 'value' into a currency format """
    try:
        value = float(value)
        # if not able to cast, then just return 'value'
    except (ValueError, TypeError):
        return value
    else:
        if with_sign:
            return "$ {0:,.2f}".format(value)
        else:
            return "{0:,.2f}".format(value)


@register.filter(name='lookup')
def lookup(my_dict, key):
    """lookup the value of a dictionary. value is a dictionary object and arg is the key"""
    try:
        return my_dict[key]
    except (KeyError, TypeError, IndexError):
        return ""


@register.filter(name='dict_2_list')
def dict_2_list(my_dict):
    """turn a dictionary into a list of key"""
    print(my_dict)
    try:
        return [key for key in my_dict]
    except (KeyError, TypeError):
        return ""


@register.filter
def kmark(value, args):
    '''
    :param value: any float
    :param args:  should be two parts: first = precision (int); second  = with_sign (True/False)
    :return: value / 1000 with [precision] decimal places and formated with a "K" if with_sign
    '''
    # both args must be present, if not then leave
    if args is None or len(args) < 2:
        return value

    arg_list = [arg.strip() for arg in args.split(',')]
    precision = int(arg_list[0])
    with_sign = bool(arg_list[1])

    try:
        float(value)
        # if not able to cast, then just return 'value'
    except (ValueError, TypeError):
        return value
    else:
        return "{1:,.{0}f} K".format(precision, float(value) / 1000) if with_sign else "{1:,.{0}f}".format(precision, float(value) / 1000)


@register.filter
def repeat(value, arg):
    repeat_string = ""
    for i in range(0, arg):
        repeat_string = repeat_string + str(value)
    return repeat_string


@register.filter
def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""

    if hasattr(value, str(arg)):
        return getattr(value, arg)
    # elif hasattr(value, 'has_key') and value.has_key(arg):
    #     return value[arg]
    # elif numeric_test.match(str(arg)) and len(value) > int(arg):
    #     return value[int(arg)]
    else:
        return value


@register.filter
def get_model_name(obj):
    try:
        return obj._meta.model_name
    except (TypeError, ValueError):
        return None


@register.filter
def get_model_verbose_name(obj, plural=False):
    try:
        if plural:
            return obj._meta.model._meta.verbose_name_plural
        else:
            return obj._meta.model._meta.verbose_name
    except (AttributeError, TypeError, ValueError):
        return None


@register.filter
def timedelta_duration_days(td):
    total_seconds = int(td.total_seconds())
    days = total_seconds // 86400
    remaining_hours = total_seconds % 86400
    remaining_minutes = remaining_hours % 3600
    hours = remaining_hours // 3600
    minutes = remaining_minutes // 60
    seconds = remaining_minutes % 60

    days_str = f'{days} days ' if days else ''
    hours_str = f'{hours}h ' if hours else ''
    minutes_str = f'{minutes}m ' if minutes else ''
    seconds_str = f'{seconds}s' if seconds and not hours_str else ''

    return f'{days_str}'


@register.filter
def text_wrap(text, width=70):
    """
    The used PDF libs don't allow CSS word-wrap, so to split long words (e.g. urls)
    we wrap the text by lines and join them with spaces to have multiple lines. See:
    https://github.com/nigma/django-easy-pdf/issues/65
    https://github.com/xhtml2pdf/xhtml2pdf/issues/379
    """
    return ' '.join(wrap(text, width))


@register.filter
def get_timezone_time(dt):
    try:
        from dm_apps.utils import get_timezone_time
        return get_timezone_time(dt)
    except:
        return dt
