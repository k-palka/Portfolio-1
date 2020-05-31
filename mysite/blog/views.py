from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail


# Create your views here.


# widok generyczny ListView analogiczny do def post_list

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# II sposób na widok
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


def test(request):
    return render(request, 'blog/post/share.html')


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = '{} ({}) zachęca do przeczytania "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Przeczytaj post "{}" na stronie {}\n\n{}\' Komentarz dodany przez: {}'.format(post.title,
                                                                                                     post_url,
                                                                                                     cd['name'],
                                                                                                     cd['comments'])
            send_mail(subject, message, 'katarzynapalka928@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
