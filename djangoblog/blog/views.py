from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, User
from .forms import AddBlog, EditBlog
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
import copy

def home(request):
    context = {'posts': Post.objects.all().order_by('-date_posted')}
    return render(request, 'genericBlog/home.html', context)


def about(request):
    return render(request, 'genericBlog/about.html', {'title': 'About'})


# normal query run in this functions
# @login_required()
# def add_blog(request):
#     if request.method == "POST":
#         form = AddBlog(request.POST)
#         if form.is_valid():
#             form.save()
#             title = form.cleaned_data.get('title')
#             messages.success(request, f"'{title}' Blog added successfully")
#             return redirect('blog-home')
#     else:
#         form = AddBlog()
#         return render(request, 'blog/add_blog.html', {'form': form})
#
#
# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     login_user = request.user
#     edit_form = True if login_user == post.author else False
#     return render(request, 'blog/detail.html', {'post': post, 'edit': edit_form})
#
#
# @login_required()
# def edit_blog(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         edit_form = EditBlog(request.POST, instance=post)
#         if edit_form.is_valid():
#             post = edit_form.save(commit=False)
#             post.author = request.user
#             # post.date_posted = timezone.now()
#             post.save()
#             title = edit_form.cleaned_data.get('title')
#             messages.success(request, f"{ title } Blog has been updated")
#             return redirect('blog-home')
#     else:
#         edit_form = EditBlog(instance=post)
#         return render(request, 'blog/edit.html', {'edit': edit_form})
#
#
# def delete_post(request, pk):
#     post = Post.objects.get(pk=pk).delete()
#     messages.success(request, f"Post has been deleted")
#     return redirect('blog-home')
#
#
# def search_post(request):
#     search_name = request.POST['search']
#     post = Post.objects.filter(
#             Q(title__contains=search_name) |
#             Q(content__contains=search_name)
#             Q(author__startswith=search_name)
#         )
#     context = {
#         'posts': post
#     }
#     return render(request, 'blog/home.html', context)

# use generic method ORM query
class PostListView(ListView):
    model = Post
    template_name = 'genericBlog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'genericBlog/userPost.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'genericBlog/detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'genericBlog/add_blog.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'genericBlog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    fields = ['title', 'content']
    template_name = 'genericBlog/post_confirm_delete.html'
    success_url = '/blog'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class SearchPost(ListView):
    model = Post
    template_name = 'genericBlog/home.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_name'] = self.request.GET.get('search')
        return context

    def get_queryset(self):
        search_name = self.request.GET.get('search')
        search_result = Post.objects.filter(
            Q(title__contains=search_name) |
            Q(content__contains=search_name) |
            Q(author__username=search_name)
        )
        return search_result