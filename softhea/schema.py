from graphene import ObjectType, String, Schema
import blog.schema
import users.schema


class Query(blog.schema.Query, users.schema.Query):
    pass


class Mutation(object):
    pass


schema = Schema(query=Query)
