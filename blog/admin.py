from django.contrib import admin
from blog.models import Tag, Blog


class MembershipInline(admin.TabularInline):
    model = Blog.tags.through
    extra = 1


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at')
    inlines = [
        MembershipInline,
    ]
    exclude = ('tags',)


admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag)
