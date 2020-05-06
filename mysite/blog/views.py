from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


# Create your views here.


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # po 3 posty na każdej stronie
    page = request.GET.get('page')  # parametr GET.page wskazującego na numer bieżącej strony
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # jeżeli zmienna page nie jest liczbą całkowitą to pobierana jest pierwsza strona wyników
        posts = paginator.page(1)
    except EmptyPage:
        # jeżeli zmienna page ma wartość większą niż numer ostatniej strony wyników
        # to pobierana jest ostatnia strona wyników
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})
