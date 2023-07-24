from django.db import models
from django.core.validators import MinLengthValidator
from django.urls import reverse


class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class PostCategory(models.Model):
    category = models.CharField(max_length=30)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Post(models.Model):
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=100)
    image = models.ImageField(upload_to="posts", null=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='posts')
    post_category = models.ForeignKey(PostCategory, on_delete=models.DO_NOTHING, related_name="post_category", null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    created = models.DateField(verbose_name="Date Created", auto_now=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    #
    # def get_title(self):
    #     return self.post.title
    #
    # def __str__(self):
    #     return f"{self.created}|{self.user_name} ({self.post.title})"
