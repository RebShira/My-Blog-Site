from django.contrib import admin
from .models import Author, Post, Tag, PostCategory, Comment


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('author', 'date', 'tags',)
    list_display = ('title', 'author', 'date',)
    ordering = ('title', 'date',)


class AuthorAdmin(admin.ModelAdmin):
    ordering = ('last_name', 'first_name')


class CommentAdmin(admin.ModelAdmin):
    list_filter = ('post', 'user_name', 'created',)
    list_display = ('created', 'user_name', 'post')
    ordering = ('post', '-id',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)
