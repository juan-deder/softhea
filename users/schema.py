from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from graphene import Field, Mutation, String
from graphene_django import DjangoObjectType
from users.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class UserMutation(Mutation):
    class Arguments:
        username = String()
        password = String()

    user = Field(UserType)

    def mutate(self, info, username, password):
        pass


class RegisterMutation(UserMutation):
    def mutate(self, info, username, password):
        user = User.objects.create_user(username, password=password)
        login(info.context, user)
        return RegisterMutation(user=user)


class LoginMutation(UserMutation):
    def mutate(self, info, username, password):
        user = authenticate(info.context, username=username, password=password)
        if user:
            login(info.context, user)
        return LoginMutation(user=user)


class LogoutMutation(Mutation):
    user = Field(UserType)

    def mutate(self, info):
        user = info.context.user if info.context.user.is_authenticated else None
        logout(info.context)
        return LogoutMutation(user=user)


class Query(object):
    user = Field(UserType, username=String(required=True))
    authed = Field(UserType)

    def resolve_user(self, info, username):
        try:
            return User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None

    def resolve_authed(self, info):
        user = info.context.user
        # is_authenticated is False for AnonymousUsers
        return user if user.is_authenticated else None


class Mutation(object):
    register = RegisterMutation.Field()
    login = LoginMutation.Field()
    logout = LogoutMutation.Field()
