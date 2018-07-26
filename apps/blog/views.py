from django.shortcuts import render
from .models import Article, Category, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.conf import settings


tags = Tag.objects.all() 



# Create your views here.
def home(request):  
    posts = Article.objects.filter(status='p', pub_time__isnull=False) 
    paginator = Paginator(posts, settings.PAGE_NUM) 
    page = request.GET.get('page') 
    categories = Category.objects.all()  
    months = Article.objects.datetimes('pub_time', 'month', order='DESC')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'post_list': post_list, 'category_list': categories, 'months': months})


def detail(request, id):
    try:
        categories = Category.objects.all() 
        post = Article.objects.get(id=str(id))
        post.viewed() 
        tags = post.tags.all()
        next_post = post.next_article()  
        prev_post = post.prev_article()  
        months = Article.objects.datetimes('pub_time', 'month', order='DESC')
    except Article.DoesNotExist:
        raise Http404
    return render(
        request, 'post.html',
        {
            'post': post,
            'tags': tags,
            'category_list': categories,
            'next_post': next_post,
            'prev_post': prev_post,
            'months': months
        }
    )


def search_category(request, id):
    categories = Category.objects.all()  
    posts = Article.objects.filter(category_id=str(id))
    category = categories.get(id=str(id))
    paginator = Paginator(posts, settings.PAGE_NUM) 
    months = Article.objects.datetimes('pub_time', 'month', order='DESC')
    try:
        page = request.GET.get('page')  
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'category.html',
                  {'post_list': post_list,
                   'category_list': categories,
                   'category': category,
                   'months': months
                  }
    )


def search_tag(request, tag):
    categories = Category.objects.all() 
    posts = Article.objects.filter(tags__name__contains=tag)
    paginator = Paginator(posts, settings.PAGE_NUM)  
    months = Article.objects.datetimes('pub_time', 'month', order='DESC')
    try:
        page = request.GET.get('page')  
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'tag.html', {
        'post_list': post_list,
        'category_list': categories,
        'tag': tag,
        'months': months
        }
    )


def archives(request, year, month):
    categories = Category.objects.all()  
    posts = Article.objects.filter(pub_time__year=year, pub_time__month=month).order_by('-pub_time')
    paginator = Paginator(posts, settings.PAGE_NUM)  
    months = Article.objects.datetimes('pub_time', 'month', order='DESC')
    try:
        page = request.GET.get('page')  
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'archive.html', {
        'post_list': post_list,
        'category_list': categories,
        'months': months,
        'year_month': year+'年'+month+'月'
        }
    )

