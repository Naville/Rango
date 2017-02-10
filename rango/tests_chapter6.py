# Chapter 3
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
import os

#Chapter 4
from django.contrib.staticfiles import finders

#Chapter 5
from rango.models import Page, Category
import populate_rango
import test_utils

#Chapter 6
from rango.decorators import chapter6

# ===== Chapter 6
class Chapter6ModelTests(TestCase):
    def test_category_contains_slug_field(self):
        #Create a new category
        new_category = Category(name="Test Category")
        new_category.save()

        #Check slug was generated
        self.assertEquals(new_category.slug, "test-category")

        #Check there is only one category
        categories = Category.objects.all()
        self.assertEquals(len(categories), 1)

        #Check attributes were saved correctly
        categories[0].slug = new_category.slug


class Chapter6ViewTests(TestCase):
    def test_index_context(self):
        # Access index with empty database
        response = self.client.get(reverse('index'))

        # Context dictionary is then empty
        self.assertItemsEqual(response.context['categories'], [])
        self.assertItemsEqual(response.context['pages'], [])

        categories = test_utils.create_categories()
        test_utils.create_pages(categories)

        #Access index with database filled
        response = self.client.get(reverse('index'))

        #Retrieve categories and pages from database
        categories = Category.objects.order_by('-likes')[:5]
        pages = Page.objects.order_by('-views')[:5]

        # Check context dictionary filled
        self.assertItemsEqual(response.context['categories'], categories)
        self.assertItemsEqual(response.context['pages'], pages)

    def test_index_displays_five_most_liked_categories(self):
        #Create categories
        test_utils.create_categories()

        # Access index
        response = self.client.get(reverse('index'))

        # Check if the 5 pages with most likes are displayed
        for i in xrange(10, 5, -1):
            self.assertIn("Category " + str(i), response.content)

    def test_index_displays_no_categories_message(self):
        # Access index with empty database
        response = self.client.get(reverse('index'))

        # Check if no categories message is displayed
        self.assertIn("There are no categories present.", response.content)

    def test_index_displays_five_most_viewed_pages(self):
        #Create categories
        categories = test_utils.create_categories()

        #Create pages for categories
        test_utils.create_pages(categories)

        # Access index
        response = self.client.get(reverse('index'))

        # Check if the 5 pages with most views are displayed
        for i in xrange(20, 15, -1):
            self.assertIn("Page " + str(i), response.content)

    def test_index_contains_link_to_categories(self):
        #Create categories
        categories = test_utils.create_categories()

        # Access index
        response = self.client.get(reverse('index'))

        # Check if the 5 pages with most likes are displayed
        for i in xrange(10, 5, -1):
            category = categories[i - 1]
            self.assertIn(reverse('show_category', args=[category.slug])[:-1], response.content)

    def test_category_context(self):
        #Create categories and pages for categories
        categories = test_utils.create_categories()
        pages = test_utils.create_pages(categories)

        # For each category check the context dictionary passed via render() function
        for category in categories:
            response = self.client.get(reverse('show_category', args=[category.slug]))
            pages = Page.objects.filter(category=category)
            self.assertItemsEqual(response.context['pages'], pages)
            self.assertEquals(response.context['category'], category)

    def test_category_page_using_template(self):
        #Create categories in database
        test_utils.create_categories()

        # Access category page
        response = self.client.get(reverse('show_category', args=['category-1']))

        # check was used the right template
        self.assertTemplateUsed(response, 'rango/category.html')

    @chapter6
    def test_category_page_displays_pages(self):
        #Create categories in database
        categories = test_utils.create_categories()

        # Create pages for categories
        test_utils.create_pages(categories)

        # For each category, access its page and check for the pages associated with it
        for category in categories:
            # Access category page
            response = self.client.get(reverse('show_category', args=[category.slug]))

            # Retrieve pages for that category
            pages = Page.objects.filter(category=category)

            # Check pages are displayed and they have a link
            for page in pages:
                self.assertIn(page.title, response.content)
                self.assertIn(page.url, response.content)

    def test_category_page_displays_empty_message(self):
        #Create categories in database
        categories = test_utils.create_categories()

        # For each category, access its page and check there are no pages associated with it
        for category in categories:
            # Access category page
            response = self.client.get(reverse('show_category', args=[category.slug]))
            self.assertIn("No pages currently in category.".lower(), response.content.lower())

    def test_category_page_displays_category_does_not_exist_message(self):
        # Try to access categories not saved to database and check the message
        response = self.client.get(reverse('show_category', args=['Python']))
        self.assertIn("does not exist!".lower(), response.content.lower())

        response = self.client.get(reverse('show_category', args=['Django']))
        self.assertIn("does not exist!".lower(), response.content.lower())
