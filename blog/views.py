from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator
from django.views.generic import ListView, View
from django.core.mail import send_mail
from django.views.decorators.http import require_POST


from .models import Post, Comment
from .forms import EmailPostForm, CommentForm



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
  sent = False
  if request.method == 'POST':
    #form was submitted 
    form = EmailPostForm(request.POST)
    if form.is_valid():
      #form fields passed the validation
      cd = form.cleaned_data
      post_url = request.build_absolute_uri(
                post.get_absolute_url())
      subject = f"{cd['name']} recommends you read " \
                f"{post.title}"
      message = f"Read {post.title} at {post_url}\n\n" \
        f"{cd['name']}\'s comments: {cd['comments']}"
      send_mail(subject, message, 'your_account@gmail.com',[cd['to']])
      sent = True
  else:
    form = EmailPostForm()
  return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})



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


@require_POST
def post_comment(request, post_id):
  post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
  comment = None
  # A comment was posted
  form = CommentForm(data=request.POST)
  if form.is_valid():
    # Create a Comment object without saving it to the database
    comment = form.save(commit=False)
    # Assign the post to the comment
    comment.post = post
    # Save the comment to the database
    comment.save()
  return render(request, 'blog/post/comment.html',
                        {'post': post,
                        'form': form,
                        'comment': comment})
