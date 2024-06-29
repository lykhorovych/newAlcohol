from django import template

register = template.Library()


@register.filter
def abs_path(url: str):
    name = url.split("/")[-1]
    
    return  f"/staticfiles/images/economy/{name}"