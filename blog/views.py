from django.shortcuts import render, get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post
from .forms import CommentForm, PostForm, LoginForm, RegisterForm
from taggit.models import Tag
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import Group,User
from django.contrib.auth.decorators import login_required,permission_required


def ingreso(request):

    form = LoginForm(request.POST or None)
    mensaje = None
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog:post_list')
        else:
            mensaje = "Login incorrecto"

    context = {'form': form, 'mensaje': mensaje}

    return render(request, 'blog/login.html', context)


def register(request):
    form = RegisterForm(request.POST or None)
    grupos = Group.objects.all()
    mensaje = None
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        grupo = form.cleaned_data['grupo']
        
        user = User.objects.create(username= username)
        user.set_password(password)            
        user.save()
        user.groups.set(grupo)
        return redirect('blog:user_login')
    
    context = {'form':form,'mensaje':mensaje,"grupos":grupos}
    return render(request,'blog/register.html',context)  


def salir(request):
    logout(request)
    return redirect('blog:user_login')


@permission_required('blog.add_post', login_url='blog:user_login')
def post_add(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
       "form":form
    }
    return render(request, 'blog/post/add.html', context)


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    page = request.GET.get('page')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts
    }
    return render(request, 'blog/post/list.html', context)


def post_detail(request, post):
    post = get_object_or_404(Post, slug=post, status='publicado')
    comments = post.comments.filter(active=True)

    new_comment = None
    comment_form = CommentForm(request.POST or None)

    if(request.method == 'POST'):
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'new_comment': new_comment
    }
    return render(request,'blog/post/detail.html', context)



