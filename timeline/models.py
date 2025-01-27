from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel

from timeline.blocks import TimelineStreamBlock

class TimelinePage(Page):
    parent_page_types = ["home.HomePage"]
    
    intro = RichTextField(
        blank=True,
        help_text="Introduction text for the timeline"
    )
    
    timeline_entries = StreamField(
        TimelineStreamBlock(),
        blank=True,
        use_json_field=True,
        help_text="Add timeline entries here"
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("timeline_entries"),
    ]

    class Meta:
        verbose_name = "Timeline Page"
        verbose_name_plural = "Timeline Pages"
