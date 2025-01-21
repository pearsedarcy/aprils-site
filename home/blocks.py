from wagtail.blocks import (
    CharBlock,
    ListBlock,
    RichTextBlock,
    StructBlock,
    URLBlock,
    ChoiceBlock,
)
from wagtail.images.blocks import ImageBlock


class HeroBlock(StructBlock):
    style = ChoiceBlock(
        choices=[
            ('split', 'Split Content'),
            ('background', 'Background Image'),
        ],
        default='split',
        help_text="Choose the hero section style"
    )
    heading = CharBlock(help_text="Main hero heading")
    text = RichTextBlock(features=["bold", "italic", "link"], help_text="Hero description")
    primary_button_text = CharBlock(required=False)
    primary_button_url = URLBlock(required=False)
    secondary_button_text = CharBlock(required=False)
    secondary_button_url = URLBlock(required=False)
    image = ImageBlock(required=False)

    class Meta:
        template = "home/blocks/hero_block.html"
        icon = "placeholder"


class FeatureBlock(StructBlock):
    icon = ImageBlock(required=False)
    title = CharBlock()
    text = RichTextBlock(features=["bold", "italic", "link"])
    button_text = CharBlock(required=False)
    button_url = URLBlock(required=False)

    class Meta:
        template = "home/blocks/feature_block.html"
        icon = "plus"


class FeaturesGridBlock(StructBlock):
    title = CharBlock(required=False)
    intro_text = RichTextBlock(required=False)
    features = ListBlock(FeatureBlock())

    class Meta:
        template = "home/blocks/features_grid_block.html"
        icon = "grip"


class CTABlock(StructBlock):
    heading = CharBlock()
    text = RichTextBlock(features=["bold", "italic", "link"])
    primary_button_text = CharBlock(required=False)
    primary_button_url = URLBlock(required=False)
    secondary_button_text = CharBlock(required=False)
    secondary_button_url = URLBlock(required=False)
    image = ImageBlock(required=False)

    class Meta:
        template = "home/blocks/cta_block.html"
        icon = "plus"
