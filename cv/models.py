from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel

from .blocks import CVStreamBlock

class CVPage(Page):
    """Page model for CV/Resume pages."""
    
    parent_page_types = ["home.HomePage"]
    
    introduction = RichTextField(
        features=["bold", "italic", "link"],
        help_text="Brief introduction or professional summary",
        blank=True
    )

    body = StreamField(
        CVStreamBlock(),
        use_json_field=True,
        blank=True,
        help_text="Build your CV content here"
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
    ]
