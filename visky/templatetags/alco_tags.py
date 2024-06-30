from django import template

register = template.Library()


@register.filter
def static_path(url: str):
    name = url.split("/")[-1]

    return f"/static/{name}"