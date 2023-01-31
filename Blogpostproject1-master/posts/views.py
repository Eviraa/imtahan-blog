from django.shortcuts import render
from django.db.models import Q 
from .models import Category, Post, Author
from .forms import CommentForm

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def homepage (request):
    categories = Category.objects.all()[0:3]
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    context= {
        'object_list': featured,
        'latest': latest,
        'categories':categories,
    }
    return render(request, 'homepage.html',context)

def post (request,slug):
    post = Post.objects.get(slug = slug)
    latest = Post.objects.order_by('-timestamp')[:3]
    comments = post.comments.filter(active=True)
    new_comment = None
    comment_form = CommentForm()
    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.post = post
        new_comment.save()
        comment_form = CommentForm()

    context = {
        'post': post,
        'latest': latest,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'post.html', context)

def about (request):
    return render(request, 'about_page.html')
def exam (request):
    return render(request, 'exam_page.html')
def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'object_list': queryset
    }
    return render(request, 'search_bar.html', context)


def postlist (request,slug):
    category = Category.objects.get(slug = slug)
    posts = Post.objects.filter(categories__in=[category])

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'post_list.html', context)
    

def allposts(request):
    posts = Post.objects.order_by('-timestamp')

    context = {
        'posts': posts,
    }
    return render(request, 'all_posts.html', context)

def like_post(request):
    data = json.loads(request.body)
    id = data["id"]
    post = Post.objects.get(id=id)
    checker = None
    
    if request.user.is_authenticated:
        
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            checker = 0
            
            
        else:
            post.likes.add(request.user)
            checker = 1
    
    likes = post.likes.count()
    
    info = {
        "check": checker,
        "num_of_likes": likes
    }
    
    return JsonResponse(info, safe=False)
    
