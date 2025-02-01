from django import template

from wagtail.models import Site

from base.models import FooterText, HeaderConfiguration, FooterConfiguration

register = template.Library()


@register.inclusion_tag("base/includes/footer_text.html", takes_context=True)
def get_footer_text(context):
    footer_text = context.get("footer_text", "")
    header_config = HeaderConfiguration.objects.filter(live=True).first()

    if not footer_text:
        instance = FooterText.objects.filter(live=True).first()
        footer_text = instance.body if instance else ""

    return {
        "footer_text": footer_text,
        "header_config": header_config,
    }

@register.simple_tag(takes_context=True)
def get_site_root(context):
    return Site.find_for_request(context["request"]).root_page

@register.simple_tag
def get_header_config():
    return HeaderConfiguration.objects.filter(live=True).first()

@register.simple_tag
def get_footer_config():
    return FooterConfiguration.objects.first()

@register.simple_tag
def get_site_logo():
    from base.models import SiteLogo  # Updated import path
    return SiteLogo.objects.first()

@register.simple_tag
def get_header_config_footer():
    return HeaderConfiguration.objects.filter(live=True).first()