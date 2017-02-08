from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category
from rango.models import Page
# Create your views here.
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
    category_list=Category.objects.order_by('-likes')[:5]
    MostViewed5Pages=Page.objects.order_by('-views')[:5]
    context_dict={"boldmessage":"Crunchy, creamy, cookie, candy, cupcake!",'categories':category_list,'MostViewed5Pages':MostViewed5Pages}
    return render(request,'rango/index.html',context=context_dict)

def about(request):
    return render(request,'rango/about.html')
