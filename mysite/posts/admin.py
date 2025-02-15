from django.contrib import admin
from .models import Post
from comments.models import Comment

# 게시글을 조회할 때 댓글도 함께 조회되도록 처리
class CommentsInline(admin.TabularInline):
    model = Comment
    extra = 1

class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'updated_by', 'updated_at')
    search_fields = ('title', 'created_by__username')
    list_filter = ('created_at',)
    inlines = [CommentsInline]

admin.site.register(Post, PostsAdmin)