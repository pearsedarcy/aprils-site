"""
Block definitions for the portfolio app.
This module contains all the block types used to build portfolio pages.
"""

from wagtail.blocks import (
    CharBlock,
    ListBlock,
    PageChooserBlock,
    RichTextBlock,
    StructBlock,
    URLBlock,
    ChoiceBlock,
)
from wagtail.images.blocks import ImageBlock
from base.blocks import BaseStreamBlock


class CardBlock(StructBlock):
    """A block for creating card-style content with image and text.
    
    Supports:
    - Optional card tag/label
    - Heading and optional sub-heading
    - Rich text content
    - Optional image with position choice
    - Two optional buttons (primary and secondary)
    """
    
    # Card content fields
    card_tag = CharBlock(required=False, help_text="Optional tag displayed at the top of the card")
    heading = CharBlock(help_text="Main heading of the card")
    sub_heading = CharBlock(required=False, help_text="Optional secondary heading")
    text = RichTextBlock(features=["bold", "italic", "link"], help_text="Main content text")
    
    # Image configuration
    image = ImageBlock(required=False, help_text="Optional image to display alongside content")
    image_position = ChoiceBlock(
        choices=[
            ('left', 'Left'),
            ('right', 'Right'),
        ],
        default='right',
        required=True,
        help_text="Choose which side the image appears on"
    )
    
    # Updated button fields
    primary_button_text = CharBlock(required=False, help_text="Text for the primary green button")
    primary_button_page = PageChooserBlock(required=False, help_text="Internal page link for the primary button")
    primary_button_url = URLBlock(required=False, help_text="External URL for the primary button")

    secondary_button_text = CharBlock(required=False, help_text="Text for the secondary pink button")
    secondary_button_page = PageChooserBlock(required=False, help_text="Internal page link for the secondary button")
    secondary_button_url = URLBlock(required=False, help_text="External URL for the secondary button")

    class Meta:
        icon = "form"
        template = "portfolio/blocks/card_block.html"
        help_text = "Add a card with image and text content, with optional buttons"


class FeaturedPostsBlock(StructBlock):
    """A block for displaying a curated list of blog posts.
    
    Allows editors to select specific blog posts to feature on the portfolio page.
    """
    
    heading = CharBlock(help_text="Section heading")
    text = RichTextBlock(
        features=["bold", "italic", "link"], 
        required=False, 
        help_text="Optional introduction text"
    )
    posts = ListBlock(
        PageChooserBlock(page_type="blog.BlogPage"),
        help_text="Select blog posts to feature"
    )

    class Meta:
        icon = "folder-open-inverse"
        template = "portfolio/blocks/featured_posts_block.html"


class PortfolioStreamBlock(BaseStreamBlock):
    """StreamBlock for building portfolio pages.
    
    Extends the BaseStreamBlock with portfolio-specific blocks.
    """
    
    card = CardBlock(group="Sections")
    featured_posts = FeaturedPostsBlock(group="Sections")