from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField

from portfolio.blocks import PortfolioStreamBlock


class PortfolioPage(Page):
    parent_page_types = ["home.HomePage"]

    sub_title = RichTextField( blank=True)

    body = StreamField(
        PortfolioStreamBlock(),
        blank=True,
        use_json_field=True,
        help_text="Use this section to list your projects and skills.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("sub_title"),
        FieldPanel("body"),
    ]