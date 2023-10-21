from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post
from django.core.paginator import Paginator
from django.views.generic import ListView, View
from .forms import EmailPostForm



def post_list(request):
  post_list = Post.published.all()
  paginator = Paginator(post_list, 3)
  page_number = request.GET.get('page',1)
  posts = paginator.get_page(page_number)
  return render(request,'blog/post/list.html',{'posts': posts}) 

class Custom404View(View):
    def get(self, request, *args, **kwargs):
        # You can customize the response as needed, such as rendering a template.
        return render(request, 'custom_404.html', status=404)

class PostListView(ListView):
  queryset = Post.published.all()
  context_object_name = 'posts'
  paginate_by = 3
  template_name = 'blog/post/list.html'


def post_share(request, post_id):
  #retreive published post by id
  post = get_object_or_404(Post, id = post_id, status = Post.Status.PUBLISHED)
  if request.method == 'POST':
    #form was submitted 
    form = EmailPostForm(request.POST)
    if form.is_valid():
      #form fields passed the validation
      cd = form.cleaned_data
  else:
    form = EmailPostForm()
  return render(request, 'blog/post/share.html', {'post': post, 'form': form})



def post_detail(request,year, month, day, post):
  post = get_object_or_404(Post,
                status=Post.Status.PUBLISHED,
                slug=post,
                publish__year=year,
                publish__month = month,
                publish__day = day
                )
  return render(request, 
  'blog/post/detail.html', {'post': post})