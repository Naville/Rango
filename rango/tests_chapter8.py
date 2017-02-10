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

#Chapter 7
from rango.decorators import chapter7
from rango.forms import CategoryForm, PageForm

#Chapter 8
from django.template import loader
from django.conf import settings
from rango.decorators import chapter8
import os.path

# ====== Chapter 8
class Chapter8ViewTests(TestCase):

    def test_base_template_exists(self):
        # Check base.html exists inside template folder
        path_to_base = settings.TEMPLATE_DIR + '/rango/base.html'
        print path_to_base
        self.assertTrue(os.path.isfile(path_to_base))

    @chapter8
    def test_titles_displayed(self):
        # Create user and log in
        test_utils.create_user()
        self.client.login(username='testuser', password='test1234')

        # Create categories
        categories = test_utils.create_categories()

        # Access index and check the title displayed
        response = self.client.get(reverse('index'))
        self.assertIn('Rango -'.lower(), response.content.lower())

        # Access category page and check the title displayed
        response = self.client.get(reverse('show_category', args=[categories[0].slug]))
        self.assertIn(categories[0].name.lower(), response.content.lower())

        # Access about page and check the title displayed
        response = self.client.get(reverse('about'))
        self.assertIn('About'.lower(), response.content.lower())

        # Access login page and check the title displayed
        response = self.client.get(reverse('login'))
        self.assertIn('Login'.lower(), response.content.lower())

        # Access register page and check the title displayed
        response = self.client.get(reverse('register'))
        self.assertIn('Register'.lower(), response.content.lower())

        # Access restricted page and check the title displayed
        response = self.client.get(reverse('restricted'))
        self.assertIn("Since you're logged in".lower(), response.content.lower())

        # Access add page and check the title displayed
        response = self.client.get(reverse('add_page', args=[categories[0].slug]))
        self.assertIn('Add Page'.lower(), response.content.lower())

        # Access add new category page and check the title displayed
        response = self.client.get(reverse('add_category'))
        self.assertIn('Add Category'.lower(), response.content.lower())

    @chapter8
    def test_pages_using_templates(self):
        # Create user and log in
        test_utils.create_user()
        self.client.login(username='testuser', password='test1234')

        # Create categories
        categories = test_utils.create_categories()
        # Create a list of pages to access
        pages = [reverse('index'), reverse('about'), reverse('add_category'), reverse('register'), reverse('login'),
                 reverse('show_category', args=[categories[0].slug]), reverse('add_page', args=[categories[0].slug])]#, reverse('restricted')]

        # Create a list of pages to access
        templates = ['rango/index.html', 'rango/about.html', 'rango/add_category.html', 'rango/register.html',
                     'rango/login.html','rango/category.html', 'rango/add_page.html']#, 'rango/restricted.html']

        # For each page in the page list, check if it extends from base template
        for template, page in zip(templates, pages):
            response = self.client.get(page)
            self.assertTemplateUsed(response, template)

    @chapter8
    def test_url_reference_in_index_page_when_logged(self):
        # Create user and log in
        test_utils.create_user()
        self.client.login(username='testuser', password='test1234')

        # Access index page
        response = self.client.get(reverse('index'))

        # Check links that appear for logged person only
        self.assertIn(reverse('add_category'), response.content)
        self.assertIn(reverse('restricted'), response.content)
        self.assertIn(reverse('logout'), response.content)
        self.assertIn(reverse('about'), response.content)

    @chapter8
    def test_url_reference_in_index_page_when_not_logged(self):
        #Access index page with user not logged
        response = self.client.get(reverse('index'))

        # Check links that appear for logged person only
        self.assertIn(reverse('register'), response.content)
        self.assertIn(reverse('login'), response.content)
        self.assertIn(reverse('about'), response.content)

    def test_link_to_index_in_base_template(self):
        # Access index
        response = self.client.get(reverse('index'))

        # Check for url referencing index
        self.assertIn(reverse('index'), response.content)

    @chapter8
    def test_url_reference_in_category_page(self):
        # Create user and log in
        test_utils.create_user()
        self.client.login(username='testuser', password='test1234')

        # Create categories
        test_utils.create_categories()

        # Check for add_page in category page
        response = self.client.get(reverse('show_category', args=['category-1']))
        self.assertIn(reverse('add_page', args=['category-1']), response.content)
