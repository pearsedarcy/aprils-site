
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
    heading = CharBlock()
    sub_heading = CharBlock(required=False)
    text = RichTextBlock(features=["bold", "italic", "link"])
    image = ImageBlock(required=False)

    class Meta:
        icon = "form"
        template = "portfolio/blocks/card_block.html"

class CardBlock2(StructBlock):
    card_tag = CharBlock(required=False)
    heading = CharBlock()
    sub_heading = CharBlock(required=False)
    text = RichTextBlock(features=["bold", "italic", "link"])
    image = ImageBlock()

    class Meta:
        icon = "form"
        template = "portfolio/blocks/card_block_2.html"

# add FeaturedPostsBlock:
class FeaturedPostsBlock(StructBlock):
    heading = CharBlock()
    text = RichTextBlock(features=["bold", "italic", "link"], required=False)
    posts = ListBlock(PageChooserBlock(page_type="blog.BlogPage"))

    class Meta:
        icon = "folder-open-inverse"
        template = "portfolio/blocks/featured_posts_block.html"

class PortfolioStreamBlock(BaseStreamBlock):
    # delete the pass statement

    card = CardBlock(group="Sections")
    card2 = CardBlock2(group="Sections")
    featured_posts = FeaturedPostsBlock(group="Sections")