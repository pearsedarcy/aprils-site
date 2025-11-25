"""
Tests for the portfolio app.

Run with: python manage.py test portfolio
"""

from django.test import TestCase
from wagtail.test.utils import WagtailPageTestCase
from wagtail.models import Page

from .models import PortfolioPage


class PortfolioPageTest(WagtailPageTestCase):
    """Tests for PortfolioPage model."""

    def setUp(self):
        """Set up test data."""
        self.root_page = Page.objects.get(slug='root')
        try:
            self.home_page = Page.objects.get(slug='home')
        except Page.DoesNotExist:
            from home.models import HomePage
            self.home_page = HomePage(title="Home", slug="home")
            self.root_page.add_child(instance=self.home_page)

    def test_portfolio_page_can_be_created(self):
        """Test that PortfolioPage can be created."""
        portfolio = PortfolioPage(
            title="My Portfolio",
            slug="portfolio",
            sub_title="<p>Check out my work</p>",
        )
        self.home_page.add_child(instance=portfolio)
        
        self.assertEqual(portfolio.title, "My Portfolio")
        self.assertIn("Check out my work", portfolio.sub_title)

    def test_portfolio_page_parent_page_types(self):
        """Test that PortfolioPage can only be created under HomePage."""
        self.assertEqual(
            PortfolioPage.parent_page_types,
            ["home.HomePage"]
        )

    def test_portfolio_page_with_empty_body(self):
        """Test that PortfolioPage can be created with empty body."""
        portfolio = PortfolioPage(
            title="Empty Portfolio",
            slug="empty-portfolio",
        )
        self.home_page.add_child(instance=portfolio)
        
        # StreamField body should be empty (no blocks)
        self.assertEqual(len(portfolio.body), 0)
