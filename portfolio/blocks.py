from wagtail.blocks import (
    CharBlock,
    ListBlock,
    PageChooserBlock,
    RichTextBlock,
    StructBlock,
    URLBlock,
    ChoiceBlock,
)

# import ImageBlock:
from wagtail.images.blocks import ImageBlock

from base.blocks import BaseStreamBlock



# add CardBlock:
class CardBlock(StructBlock):
    card_tag = CharBlock(required=False)
    heading = CharBlock()
    sub_heading = CharBlock(required=False)
    text = RichTextBlock(features=["bold", "italic", "link"])
    image = ImageBlock(required=False)
    image_position = ChoiceBlock(
        choices=[
            ('left', 'Left'),
            ('right', 'Right'),
        ],
        default='right',
        required=True,
    )
    primary_button_text = CharBlock(required=False)
    primary_button_url = URLBlock(required=False)
    secondary_button_text = CharBlock(required=False)
    secondary_button_url = URLBlock(required=False)

    class Meta:
        icon = "form"
        template = "portfolio/blocks/card_block.html"

# add FeaturedPostsBlock:
class FeaturedPostsBlock(StructBlock):
    heading = CharBlock()
    text = RichTextBlock(features=["bold", "italic", "link"], required=False)
    posts = ListBlock(PageChooserBlock(page_type="blog.BlogPage"))

    class Meta:
        icon = "folder-open-inverse"
        template = "portfolio/blocks/featured_posts_block.html"

class PortfolioStreamBlock(BaseStreamBlock):
    card = CardBlock(group="Sections")
    featured_posts = FeaturedPostsBlock(group="Sections")