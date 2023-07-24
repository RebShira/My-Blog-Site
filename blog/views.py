from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.views import View

from .models import Post
from .forms import CommentForm
import mimetypes


def about_me(request):
    return render(request, 'blog/about_me.html')


class StartingPageView(ListView):
    template_name = "blog/starting_page.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


# def starting_page(request):
#     start_posts = Post.objects.all().order_by('-date')[:3]
#     return render(request, 'blog/starting_page.html', {'posts': start_posts})


class AllPostsView(ListView):
    template_name = "blog/posts_page.html"
    model = Post
    ordering = ["post_category", "-date"]
    context_object_name = "posts"
    # post_categories = []
    # for record in model.objects.all():
    #     curr_category = record.post_category.category
    #     if curr_category not in post_categories:
    #         post_categories.append(curr_category)

    def get_context_data(self, *, object_list=None, **kwargs):
        post_categories = []
        for record in self.model.objects.all():
            curr_category = record.post_category.category
            if curr_category not in post_categories:
                post_categories.append(curr_category)
        data = super().get_context_data(**kwargs)
        data["categories"] = post_categories
        return data


# def posts(request):
#     all_posts = Post.objects.all()
#     return render(request, 'blog/posts_page.html', {'posts': all_posts})


class SinglePostView(View):
    # template_name = "blog/post_detail.html"
    # model = Post

    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post_id=post.id)
        }
        return render(request, "blog/post_detail.html", context)

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post_detail", args=[slug]))

        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post_id=post.id)
        }
        return render(request, "blog/post_detail.html")


class ReadLaterView(View):

    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored_posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
            request.session["stored_posts"] = stored_posts
        else:
            stored_posts.remove(post_id)
            request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["tags"] = self.object.tags.all()
    #     context["comment_form"] = CommentForm()
    #     return context


# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(request, 'blog/post_detail.html', {
#         'post': identified_post,
#         'tags': identified_post.tags.all()})
