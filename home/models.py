from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from home.blocks import HeroBlock, FeaturesGridBlock, CTABlock

class HomePage(Page):
    content = StreamField([
        ('hero', HeroBlock()),
        ('features_grid', FeaturesGridBlock()),
        ('cta', CTABlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("content"),
    ]