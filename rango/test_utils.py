from rango.models import Category, Page

def create_categories():
    # List of categories
    categories = []

    # Create categories from 1 to 10
    for i in xrange(1, 11):
        cat = Category(name="Category " + str(i), likes=i)
        cat.save()
        categories.append(cat)

    return categories

def create_pages(categories):
    # List of pages
    pages = []

    # For each category create 2 pages
    for i in xrange (0, len(categories)):
        category = categories[i]

        # Name the pages according to the links and create a fake url
        for j in xrange(0, 2):
            page_number = i * 2 + j + 1
            page = Page(category=category, title="Page " + str(page_number),
                        url="http://www.page" + str(page_number) + ".com", views=page_number)
            page.save()
            pages.append(page)

    return pages

def create_user():
    # Create a user
    from rango.models import User, UserProfile
    user = User.objects.get_or_create(username="testuser", password="test1234",
                                      first_name="Test", last_name="User", email="testuser@testuser.com")[0]
    user.set_password(user.password)
    user.save()

    # Create a user profile
    user_profile = UserProfile.objects.get_or_create(user=user,
                                                     website="http://www.testuser.com")[0]
    user_profile.save()

    return user, user_profile
