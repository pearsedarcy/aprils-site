from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

class TimelineCardBlock(blocks.StructBlock):
    date = blocks.CharBlock(
        required=True,
        help_text="Enter the date or time period"
    )
    title = blocks.CharBlock(
        required=True,
        help_text="Enter the title of this timeline entry"
    )
    description = blocks.RichTextBlock(
        required=True,
        features=['bold', 'italic', 'link'],
        help_text="Enter the description of this timeline entry"
    )
    image = ImageChooserBlock(
        required=False,
        help_text="Optional: Choose an image to accompany this entry"
    )
    
    class Meta:
        template = 'timeline/blocks/timeline_card.html'
        icon = 'date'
        label = 'Timeline Entry'

class TimelineStreamBlock(blocks.StreamBlock):
    timeline_entry = TimelineCardBlock()

    class Meta:
        min_num = 1
        max_num = 50
