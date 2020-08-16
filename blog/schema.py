from graphene import String, ObjectType, List
from graphene_django import DjangoObjectType
from blog.models import Blog, Tag


class BlogType(DjangoObjectType):
    class Meta:
        model = Blog


class TagType(DjangoObjectType):
    class Meta:
        model = Tag


class Query(ObjectType):
    blogs = List(BlogType, tags=List(String, required=False))
    tags = List(TagType)

    def resolve_blogs(self, info, tags=[]):
        queryset = Blog.objects.all()
        for tag in tags:
            queryset = queryset.filter(tags__name__exact=tag)
        return queryset

    def resolve_tags(self, info):
        return Tag.objects.all()
