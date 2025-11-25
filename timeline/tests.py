"""
Tests for the timeline app.

Run with: python manage.py test timeline
"""

from django.test import TestCase
from wagtail.test.utils import WagtailPageTestCase
from wagtail.models import Page

from .models import TimelinePage


class TimelinePageTest(WagtailPageTestCase):
    """Tests for TimelinePage model."""

    def setUp(self):
        """Set up test data."""
        self.root_page = Page.objects.get(slug='root')
        try:
            self.home_page = Page.objects.get(slug='home')
        except Page.DoesNotExist:
            from home.models import HomePage
            self.home_page = HomePage(title="Home", slug="home")
            self.root_page.add_child(instance=self.home_page)

    def test_timeline_page_can_be_created(self):
        """Test that TimelinePage can be created."""
        timeline = TimelinePage(
            title="My Timeline",
            slug="timeline",
            intro="<p>My career journey</p>",
        )
        self.home_page.add_child(instance=timeline)
        
        self.assertEqual(timeline.title, "My Timeline")
        self.assertIn("My career journey", timeline.intro)

    def test_timeline_page_parent_page_types(self):
        """Test that TimelinePage can only be created under HomePage."""
        self.assertEqual(
            TimelinePage.parent_page_types,
            ["home.HomePage"]
        )

    def test_timeline_page_with_empty_entries(self):
        """Test that TimelinePage can be created with empty timeline entries."""
        timeline = TimelinePage(
            title="Empty Timeline",
            slug="empty-timeline",
        )
        self.home_page.add_child(instance=timeline)
        
        # StreamField should be empty (no entries)
        self.assertEqual(len(timeline.timeline_entries), 0)

    def test_timeline_page_verbose_name(self):
        """Test TimelinePage verbose names."""
        self.assertEqual(TimelinePage._meta.verbose_name, "Timeline Page")
        self.assertEqual(TimelinePage._meta.verbose_name_plural, "Timeline Pages")
