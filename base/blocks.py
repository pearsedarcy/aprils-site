from django.core.exceptions import ValidationError
from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    URLBlock,
    PageChooserBlock,
    EmailBlock,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageBlock


# =============================================================================
# Shared Button Blocks - Reusable across all apps
# =============================================================================

class ButtonBlock(StructBlock):
    """A reusable button block that supports both internal pages and external URLs.
    
    Use this block when you need a single button. For dual button patterns
    (primary/secondary), use DualButtonMixin or include two ButtonBlocks.
    """
    text = CharBlock(required=False, help_text="Button text")
    page = PageChooserBlock(required=False, help_text="Internal page link")
    url = URLBlock(required=False, help_text="External URL (used if no page selected)")
    style = ChoiceBlock(
        choices=[
            ('primary', 'Primary'),
            ('secondary', 'Secondary'),
            ('ghost', 'Ghost'),
        ],
        default='primary',
        required=False,
        help_text="Button style"
    )

    def get_url(self, value):
        """Helper method to get the button URL."""
        if value.get('page'):
            return value['page'].url
        return value.get('url', '')

    class Meta:
        icon = "link"
        template = "base/blocks/button_block.html"


class DualButtonMixin:
    """Mixin providing primary and secondary button fields.
    
    Use this in StructBlocks that need the common dual-button pattern.
    Add these fields to your block:
    
        primary_button_text = CharBlock(required=False)
        primary_button_page = PageChooserBlock(required=False)
        primary_button_url = URLBlock(required=False)
        secondary_button_text = CharBlock(required=False)
        secondary_button_page = PageChooserBlock(required=False)
        secondary_button_url = URLBlock(required=False)
    """
    
    @staticmethod
    def get_primary_url(value):
        """Get URL for primary button."""
        if value.get('primary_button_page'):
            return value['primary_button_page'].url
        return value.get('primary_button_url', '')
    
    @staticmethod
    def get_secondary_url(value):
        """Get URL for secondary button."""
        if value.get('secondary_button_page'):
            return value['secondary_button_page'].url
        return value.get('secondary_button_url', '')

class CaptionedImageBlock(StructBlock):
    image = ImageBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "base/blocks/captioned_image_block.html"



class SubHeadingBlock(StructBlock):
    sub_heading_text = CharBlock(classname="sub-title", required=True)
    size = ChoiceBlock(
        choices=[
            ("", "Select a heading size"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        blank=True,
        required=False,
    )

    class Meta:
        icon = "title"
        template = "base/blocks/sub_heading_block.html"

class HeadingBlock(StructBlock):
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(
        choices=[
            ("", "Select a heading size"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        blank=True,
        required=False,
    )

    class Meta:
        icon = "title"
        template = "base/blocks/heading_block.html"


class BaseStreamBlock(StreamBlock):
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(icon="pilcrow")
    image_block = CaptionedImageBlock()

    embed_block = EmbedBlock(
        help_text="Insert a URL to embed. For example, https://www.youtube.com/watch?v=SGJFWirQ3ks",
        icon="media",

    )

class newStreamBlock(StreamBlock):
    heading_block = HeadingBlock()
    sub_heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(icon="pilcrow")
    image_block = CaptionedImageBlock()
    embed_block = EmbedBlock(
        help_text="Insert a URL to embed. For example, https://www.youtube.com/watch?v=SGJFWirQ3ks",
        icon="media",
    )

class FooterLinkBlock(StructBlock):
    title = CharBlock(required=True)
    link_type = ChoiceBlock(
        choices=[
            ('page', 'Internal Page'),
            ('external', 'External URL'),
        ],
        default='page',
        required=True,
    )
    page = PageChooserBlock(required=False)
    external_url = URLBlock(required=False)
    icon = CharBlock(required=False, help_text="Optional: add an SVG icon code")

    def clean(self, value):
        cleaned_data = super().clean(value)
        if cleaned_data['link_type'] == 'page' and not cleaned_data.get('page'):
            raise ValidationError('Please select a page for internal links.')
        if cleaned_data['link_type'] == 'external' and not cleaned_data.get('external_url'):
            raise ValidationError('Please enter a URL for external links.')
        return cleaned_data

    class Meta:
        template = 'base/blocks/footer_link_block.html'
        icon = 'link'

class FooterColumnBlock(StructBlock):
    heading = CharBlock(required=True)
    links = StreamBlock([
        ('link', FooterLinkBlock()),
    ])

    class Meta:
        template = 'base/blocks/footer_column_block.html'
        icon = 'list-ul'

class FooterContentBlock(StreamBlock):
    column = FooterColumnBlock()
    social_links = FooterLinkBlock()

    class Meta:
        template = 'base/blocks/footer_content_block.html'

class ContactInfoBlock(StructBlock):
    icon_svg = CharBlock(required=True, help_text="SVG path data for the icon")
    title = CharBlock(required=True)
    description = CharBlock(required=True)
    contact_type = ChoiceBlock(
        choices=[
            ('social', 'Social Media Link'),
            ('email', 'Email Link'),
        ],
        required=True,
    )
    # Contact-specific fields
    social_link = URLBlock(required=False)
    email = EmailBlock(required=False)

    
    def clean(self, value):
        cleaned_data = super().clean(value)
        contact_type = cleaned_data.get('contact_type')
        
        if contact_type == 'social' and not cleaned_data.get('social_link'):
            raise ValidationError('Please enter a social media URL.')
        elif contact_type == 'email' and not cleaned_data.get('email'):
            raise ValidationError('Please enter an email address.')

            
        return cleaned_data

    class Meta:
        template = 'base/blocks/contact_info_block.html'
        icon = 'info'