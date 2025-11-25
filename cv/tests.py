"""
Tests for the cv app.

Run with: python manage.py test cv
"""

from django.test import TestCase
from wagtail.test.utils import WagtailPageTestCase
from wagtail.models import Page

from .models import CVPage


class CVPageTest(WagtailPageTestCase):
    """Tests for CVPage model."""

    def setUp(self):
        """Set up test data."""
        self.root_page = Page.objects.get(slug='root')
        try:
            self.home_page = Page.objects.get(slug='home')
        except Page.DoesNotExist:
            from home.models import HomePage
            self.home_page = HomePage(title="Home", slug="home")
            self.root_page.add_child(instance=self.home_page)

    def test_cv_page_can_be_created(self):
        """Test that CVPage can be created."""
        cv_page = CVPage(
            title="My CV",
            slug="cv",
            introduction="<p>Professional software developer</p>",
        )
        self.home_page.add_child(instance=cv_page)
        
        self.assertEqual(cv_page.title, "My CV")
        self.assertIn("Professional software developer", cv_page.introduction)

    def test_cv_page_parent_page_types(self):
        """Test that CVPage can only be created under HomePage."""
        self.assertEqual(
            CVPage.parent_page_types,
            ["home.HomePage"]
        )

    def test_cv_page_with_empty_body(self):
        """Test that CVPage can be created with empty body."""
        cv_page = CVPage(
            title="Empty CV",
            slug="empty-cv",
        )
        self.home_page.add_child(instance=cv_page)
        
        # StreamField body should be empty (no blocks)
        self.assertEqual(len(cv_page.body), 0)

    def test_cv_page_with_empty_introduction(self):
        """Test that CVPage can have blank introduction."""
        cv_page = CVPage(
            title="CV No Intro",
            slug="cv-no-intro",
            introduction="",
        )
        self.home_page.add_child(instance=cv_page)
        
        self.assertEqual(cv_page.introduction, "")
