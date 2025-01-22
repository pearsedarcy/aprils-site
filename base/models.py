from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PublishingPanel,
)

from wagtail.fields import RichTextField, StreamField
from wagtail.models import (
    DraftStateMixin,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
)

from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

from wagtail.contrib.forms.panels import FormSubmissionsPanel

from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)

from wagtail.snippets.models import register_snippet

from .blocks import FooterContentBlock, FooterLinkBlock

@register_setting
class NavigationSettings(BaseGenericSetting):
    linkedin_url = models.URLField(verbose_name="LinkedIn URL", blank=True)
    github_url = models.URLField(verbose_name="GitHub URL", blank=True)
    mastodon_url = models.URLField(verbose_name="Mastodon URL", blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("linkedin_url"),
                FieldPanel("github_url"),
                FieldPanel("mastodon_url"),
            ],
            "Social settings",
        )
    ]

@register_snippet
class FooterText(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    models.Model,
):

    body = RichTextField()

    panels = [
        FieldPanel("body"),
        PublishingPanel(),
    ]

    def __str__(self):
        return "Footer text"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"footer_text": self.body}

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "Footer Text"

@register_snippet
class HeaderConfiguration(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    models.Model,
):
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Logo"
    )
    cv_button_text = models.CharField(max_length=50, default="CV")
    cv_button_link = models.URLField(blank=True)
    contact_button_text = models.CharField(max_length=50, default="Contact")
    contact_button_link = models.URLField(blank=True)

    panels = [
        FieldPanel("logo"),
        MultiFieldPanel([
            FieldPanel("cv_button_text"),
            FieldPanel("cv_button_link"),
        ], "CV Button"),
        MultiFieldPanel([
            FieldPanel("contact_button_text"),
            FieldPanel("contact_button_link"),
        ], "Contact Button"),
        PublishingPanel(),
    ]

    def __str__(self):
        return "Header Configuration"

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Header Configuration"
        verbose_name_plural = "Header Configurations"

@register_snippet
class FooterConfiguration(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    models.Model,
):
    content = StreamField(
        FooterContentBlock(),
        blank=True,
        use_json_field=True,
        verbose_name="Footer Content"
    )
    privacy_link = models.URLField(blank=True)
    terms_link = models.URLField(blank=True)
    social_links = StreamField(
        [('social_link', FooterLinkBlock())],
        blank=True,
        use_json_field=True,
        verbose_name="Social Links"
    )

    panels = [
        FieldPanel("content"),
        MultiFieldPanel([
            FieldPanel("privacy_link"),
            FieldPanel("terms_link"),
        ], "Legal Links"),
        FieldPanel("social_links"),
        PublishingPanel(),
    ]

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {
            'footer_config': self,
            'request': request
        }

    def __str__(self):
        return "Footer Configuration"

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Footer Configuration"
        verbose_name_plural = "Footer Configurations"

@register_snippet
class SiteLogo(models.Model):
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    alt_text = models.CharField(max_length=100, blank=True)

    panels = [
        FieldPanel('logo'),
        FieldPanel('alt_text'),
    ]

    def __str__(self):
        return "Site Logo"

    class Meta:
        verbose_name = "Site Logo"
        verbose_name_plural = "Site Logo"

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(AbstractEmailForm):
    large_text = RichTextField(blank=True)
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('large_text'),
        FieldPanel('intro'),
        FieldPanel('image'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address'),
                FieldPanel('to_address'),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]