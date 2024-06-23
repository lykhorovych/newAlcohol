from django import template


register = template.Library()


@register.filter
def abs_path(url: str):
    url = url.split("/")[-1]
    return f"../../static/images/{url}"