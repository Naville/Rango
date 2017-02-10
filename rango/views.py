from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from rango.models import Category,Page
from rango.forms import CategoryForm,PageForm,UserForm,UserProfileForm
from django.contrib.auth import authenticate,login,logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login (request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username,password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request,'rango/login.html',{})
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            #put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                  'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

def add_page(request,category_name_slug):
    try:
        category=Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category=None
    form = PageForm()
    if request.method == 'POST':
        form= PageForm(request.POST)
        if form.is_valid():
            if category:
                page=form.save(commit=False)
                page.category=category
                page.views=0
                page.save()
            return show_category(request,category_name_slug)
        else:
            print form.errors
    context_dict={'form':form,"category":category}
    return render(request,'rango/add_page.html',context_dict)
def add_category(request):
    form=CategoryForm()
    if request.method=="POST":
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request,'rango/add_category.html',{'form':form})
def show_category(request,category_name_slug):
    context_dict={}
    try:
        category=Category.objects.get(slug=category_name_slug)
        pages=Page.objects.filter(category=category)
        context_dict['pages']=pages
        context_dict['category']=category
    except Category.DoesNotExist:
        context_dict['category']=None
        context_dict['pages']=None
    return render(request,'rango/category.html',context_dict)
def index(request):
    request.session.set_test_cookie()
    category_list=Category.objects.order_by('-likes')[:5]
    MostViewed5Pages=Page.objects.order_by('-views')[:5]
    context_dict={"boldmessage":"Crunchy, creamy, cookie, candy, cupcake!",'categories':category_list,'pages':MostViewed5Pages}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response= render(request,'rango/index.html',context=context_dict)
    return response

def about(request):
    visitor_cookie_handler(request)
    return render(request,'rango/about.html',context={"visits":request.session['visits']})
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val
def visitor_cookie_handler(request):
	    visits = int(get_server_side_cookie(request, 'visits', '1'))
	    last_visit_cookie = get_server_side_cookie(request,
	                                               'last_visit',
	                                               str(datetime.now()))
	    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
	                                        '%Y-%m-%d %H:%M:%S')

	    # If it's been more than a day since the last visit...
	    if (datetime.now() - last_visit_time).seconds > 0:
	        visits = visits + 1
	        #update the last visit cookie now that we have updated the count
	        request.session['last_visit'] = str(datetime.now())
	    else:
	        visits = 1
	        # set the last visit cookie
	        request.session['last_visit'] = last_visit_cookie

	    # Update/set the visits cookie
	    request.session['visits'] = visits
