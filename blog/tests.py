"""
Tests for the blog app.

Run with: python manage.py test blog
"""

from datetime import date
from django.test import TestCase
from wagtail.test.utils import WagtailPageTestCase
from wagtail.models import Page

from .models import BlogIndexPage, BlogPage, BlogTagIndexPage, Author


class AuthorTest(TestCase):
    """Tests for Author snippet."""

    def test_author_creation(self):
        """Test that Author can be created."""
        author = Author.objects.create(name="Jane Doe")
        self.assertEqual(str(author), "Jane Doe")
        self.assertEqual(author.name, "Jane Doe")

    def test_author_without_image(self):
        """Test that Author can be created without an image."""
        author = Author.objects.create(name="John Smith")
        self.assertIsNone(author.author_image)


class BlogIndexPageTest(WagtailPageTestCase):
    """Tests for BlogIndexPage model."""

    def setUp(self):
        """Set up test data."""
        self.root_page = Page.objects.get(slug='root')
        try:
            self.home_page = Page.objects.get(slug='home')
        except Page.DoesNotExist:
            from home.models import HomePage
            self.home_page = HomePage(title="Home", slug="home")
            self.root_page.add_child(instance=self.home_page)

    def test_blog_index_page_can_be_created(self):
        """Test that BlogIndexPage can be created."""
        blog_index = BlogIndexPage(
            title="Blog",
            slug="blog",
            intro="<p>Welcome to my blog</p>",
            header="<h1>My Blog</h1>",
        )
        self.home_page.add_child(instance=blog_index)
        
        self.assertEqual(blog_index.title, "Blog")
        self.assertIn("Welcome to my blog", blog_index.intro)


class BlogPageTest(WagtailPageTestCase):
    """Tests for BlogPage model."""

    def setUp(self):
        """Set up test data."""
        self.root_page = Page.objects.get(slug='root')
        try:
            self.home_page = Page.objects.get(slug='home')
        except Page.DoesNotExist:
            from home.models import HomePage
            self.home_page = HomePage(title="Home", slug="home")
            self.root_page.add_child(instance=self.home_page)
        
        # Create blog index
        self.blog_index = BlogIndexPage(
            title="Blog",
            slug="blog",
        )
        self.home_page.add_child(instance=self.blog_index)

    def test_blog_page_can_be_created(self):
        """Test that BlogPage can be created."""
        blog_page = BlogPage(
            title="My First Post",
            slug="my-first-post",
            date=date.today(),
            intro="This is my first blog post",
            body="<p>Content of the blog post</p>",
        )
        self.blog_index.add_child(instance=blog_page)
        
        self.assertEqual(blog_page.title, "My First Post")
        self.assertEqual(blog_page.intro, "This is my first blog post")

    def test_blog_page_main_image_without_gallery(self):
        """Test that main_image returns None when no gallery images."""
        blog_page = BlogPage(
            title="Test Post",
            slug="test-post",
            date=date.today(),
            intro="Test intro",
        )
        self.blog_index.add_child(instance=blog_page)
        
        self.assertIsNone(blog_page.main_image())

    def test_blog_page_with_author(self):
        """Test that BlogPage can have authors."""
        author = Author.objects.create(name="Test Author")
        
        blog_page = BlogPage(
            title="Authored Post",
            slug="authored-post",
            date=date.today(),
            intro="Post with author",
        )
        self.blog_index.add_child(instance=blog_page)
        blog_page.authors.add(author)
        
        self.assertIn(author, blog_page.authors.all())


class BlogTagIndexPageTest(WagtailPageTestCase):
    """Tests for BlogTagIndexPage model."""

    def setUp(self):
        """Set up test data."""
        self.root_page = Page.objects.get(slug='root')
        try:
            self.home_page = Page.objects.get(slug='home')
        except Page.DoesNotExist:
            from home.models import HomePage
            self.home_page = HomePage(title="Home", slug="home")
            self.root_page.add_child(instance=self.home_page)

    def test_blog_tag_index_page_can_be_created(self):
        """Test that BlogTagIndexPage can be created."""
        tag_index = BlogTagIndexPage(
            title="Blog Tags",
            slug="tags",
        )
        self.home_page.add_child(instance=tag_index)
        
        self.assertEqual(tag_index.title, "Blog Tags")
