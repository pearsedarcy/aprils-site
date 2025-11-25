"""
Tests for the base app.

Run with: python manage.py test base
"""

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from wagtail.test.utils import WagtailPageTestCase
from wagtail.models import Page, Site

from .models import (
    NavigationSettings,
    FooterText,
    HeaderConfiguration,
    FooterConfiguration,
    SiteLogo,
    SiteFavicon,
    FormPage,
    FormField,
)


class NavigationSettingsTest(TestCase):
    """Tests for NavigationSettings model."""

    def test_navigation_settings_creation(self):
        """Test that NavigationSettings can be created."""
        settings = NavigationSettings.objects.create(
            linkedin_url="https://linkedin.com/in/test",
            github_url="https://github.com/test",
            mastodon_url="https://mastodon.social/@test",
        )
        self.assertEqual(settings.linkedin_url, "https://linkedin.com/in/test")
        self.assertEqual(settings.github_url, "https://github.com/test")
        self.assertEqual(settings.mastodon_url, "https://mastodon.social/@test")

    def test_navigation_settings_blank_urls(self):
        """Test that social URLs can be blank."""
        settings = NavigationSettings.objects.create()
        self.assertEqual(settings.linkedin_url, "")
        self.assertEqual(settings.github_url, "")
        self.assertEqual(settings.mastodon_url, "")


class FooterTextTest(TestCase):
    """Tests for FooterText snippet."""

    def test_footer_text_creation(self):
        """Test that FooterText can be created."""
        footer = FooterText.objects.create(body="<p>Test footer content</p>")
        self.assertEqual(str(footer), "Footer text")
        self.assertIn("Test footer content", footer.body)

    def test_footer_text_preview_template(self):
        """Test that FooterText has correct preview template."""
        footer = FooterText.objects.create(body="<p>Test</p>")
        self.assertEqual(footer.get_preview_template(None, None), "base.html")


class HeaderConfigurationTest(TestCase):
    """Tests for HeaderConfiguration snippet."""

    def test_header_configuration_creation(self):
        """Test that HeaderConfiguration can be created."""
        header = HeaderConfiguration.objects.create(
            cv_button_text="My CV",
            contact_button_text="Get in Touch",
        )
        self.assertEqual(str(header), "Header Configuration")
        self.assertEqual(header.cv_button_text, "My CV")
        self.assertEqual(header.contact_button_text, "Get in Touch")

    def test_header_configuration_defaults(self):
        """Test HeaderConfiguration default values."""
        header = HeaderConfiguration.objects.create()
        self.assertEqual(header.cv_button_text, "CV")
        self.assertEqual(header.contact_button_text, "Contact")


class FooterConfigurationTest(TestCase):
    """Tests for FooterConfiguration snippet."""

    def test_footer_configuration_creation(self):
        """Test that FooterConfiguration can be created."""
        footer = FooterConfiguration.objects.create(
            privacy_link="https://example.com/privacy",
            terms_link="https://example.com/terms",
        )
        self.assertEqual(str(footer), "Footer Configuration")
        self.assertEqual(footer.privacy_link, "https://example.com/privacy")

    def test_footer_configuration_preview_template(self):
        """Test that FooterConfiguration has correct preview template."""
        footer = FooterConfiguration.objects.create()
        self.assertEqual(footer.get_preview_template(None, None), "base.html")


class SiteLogoTest(TestCase):
    """Tests for SiteLogo snippet."""

    def test_site_logo_creation(self):
        """Test that SiteLogo can be created."""
        logo = SiteLogo.objects.create(alt_text="Company Logo")
        self.assertEqual(str(logo), "Site Logo")
        self.assertEqual(logo.alt_text, "Company Logo")


class SiteFaviconTest(TestCase):
    """Tests for SiteFavicon snippet."""

    def test_site_favicon_creation(self):
        """Test that SiteFavicon can be created."""
        favicon = SiteFavicon.objects.create(alt_text="Site Favicon")
        self.assertEqual(str(favicon), "Site Favicon")
        self.assertEqual(favicon.alt_text, "Site Favicon")


class FormPageTest(WagtailPageTestCase):
    """Tests for FormPage model."""

    def setUp(self):
        """Set up test data."""
        self.root_page = Page.objects.get(slug='root')
        # Get or create home page
        try:
            self.home_page = Page.objects.get(slug='home')
        except Page.DoesNotExist:
            from home.models import HomePage
            self.home_page = HomePage(title="Home", slug="home")
            self.root_page.add_child(instance=self.home_page)

    def test_form_page_can_be_created(self):
        """Test that FormPage can be created under home page."""
        form_page = FormPage(
            title="Contact Us",
            slug="contact",
            intro="<p>Get in touch with us</p>",
            thank_you_text="<p>Thanks for your message!</p>",
            from_address="noreply@example.com",
            to_address="admin@example.com",
            subject="New Contact Form Submission",
        )
        self.home_page.add_child(instance=form_page)
        
        self.assertEqual(form_page.title, "Contact Us")
        self.assertIn("Get in touch", form_page.intro)

    def test_form_page_with_fields(self):
        """Test that FormPage can have form fields."""
        form_page = FormPage(
            title="Contact",
            slug="contact-form",
            from_address="test@example.com",
            to_address="admin@example.com",
            subject="Test",
        )
        self.home_page.add_child(instance=form_page)
        
        # Add form fields
        FormField.objects.create(
            page=form_page,
            label="Name",
            field_type="singleline",
            required=True,
        )
        FormField.objects.create(
            page=form_page,
            label="Email",
            field_type="email",
            required=True,
        )
        FormField.objects.create(
            page=form_page,
            label="Message",
            field_type="multiline",
            required=True,
        )
        
        self.assertEqual(form_page.form_fields.count(), 3)


class TemplateTagsTest(TestCase):
    """Tests for custom template tags."""

    def test_navigation_tags_load(self):
        """Test that navigation template tags can be loaded."""
        from django.template import Template, Context
        template = Template('{% load navigation_tags %}')
        # Should not raise an exception
        template.render(Context({}))


class ContextProcessorsTest(TestCase):
    """Tests for context processors."""

    def test_daisyui_themes_context(self):
        """Test that daisyui themes context processor returns themes."""
        from poxed.context_processors import daisyui_themes_context
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get('/')
        
        context = daisyui_themes_context(request)
        
        self.assertIn('daisyui_themes', context)
        self.assertIsInstance(context['daisyui_themes'], list)
        self.assertIn('light', context['daisyui_themes'])
        self.assertIn('dark', context['daisyui_themes'])


class BaseTemplateTest(TestCase):
    """Tests for base templates."""

    def setUp(self):
        self.client = Client()

    @override_settings(DEBUG=True)
    def test_base_template_renders(self):
        """Test that the base template renders without errors."""
        # This will test template loading
        from django.template.loader import get_template
        template = get_template('base.html')
        self.assertIsNotNone(template)
