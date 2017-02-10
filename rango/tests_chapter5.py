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

# ===== CHAPTER 5
class Chapter5ModelTests(TestCase):

    def test_create_a_new_category(self):
        cat = Category(name="Python")
        cat.save()

        # Check category is in database
        categories_in_database = Category.objects.all()
        self.assertEquals(len(categories_in_database), 1)
        only_poll_in_database = categories_in_database[0]
        self.assertEquals(only_poll_in_database, cat)

    def test_create_pages_for_categories(self):
        cat = Category(name="Python")
        cat.save()

        # create 2 pages for category python
        python_page = Page()
        python_page.category = cat
        python_page.title="Official Python Tutorial"
        python_page.url="http://docs.python.org/2/tutorial/"
        python_page.save()

        django_page = Page()
        django_page.category = cat
        django_page.title="Django"
        django_page.url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/"
        django_page.save()

        # Check if they both were saved
        python_pages = cat.page_set.all()
        self.assertEquals(python_pages.count(), 2)

        #Check if they were saved properly
        first_page = python_pages[0]
        self.assertEquals(first_page, python_page)
        self.assertEquals(first_page.title , "Official Python Tutorial")
        self.assertEquals(first_page.url, "http://docs.python.org/2/tutorial/")

    def test_population_script_changes(self):
        #Populate database
        populate_rango.populate()

        # Check if the category has correct number of views and likes
        cat = Category.objects.get(name='Python')
        self.assertEquals(cat.views, 128)
        self.assertEquals(cat.likes, 64)

        # Check if the category has correct number of views and likes
        cat = Category.objects.get(name='Django')
        self.assertEquals(cat.views, 64)
        self.assertEquals(cat.likes, 32)

        # Check if the category has correct number of views and likes
        cat = Category.objects.get(name='Other Frameworks')
        self.assertEquals(cat.views, 32)
        self.assertEquals(cat.likes, 16)
