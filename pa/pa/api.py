from random import choice

from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from tastypie.resources import ModelResource

from news.models import NewsQuote


class UserObjectsOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(added_by=bundle.request.user)

    def read_detail(self, object_list, bundle):
        return bundle.obj.added_by == bundle.request.user

    def create_list(self, object_list, bundle):
        raise Unauthorized("Unauthorized!")

    def create_detail(self, object_list, bundle):
        raise Unauthorized("Unauthorized!")

    def update_list(self, object_list, bundle):
        raise Unauthorized("Unauthorized!")

    def update_detail(self, object_list, bundle):
        raise Unauthorized("Unauthorized!")

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Unauthorized!")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Unauthorized!")


class NewsQuoteResource(ModelResource):
    class Meta:
        queryset = NewsQuote.objects.all()
        resource_name = "news_quote"
        excludes = ["id"]

        authentication = BasicAuthentication()
        authorization = UserObjectsOnlyAuthorization()

    def authorized_read_list(self, object_list, bundle):

        ids = object_list.filter(added_by=bundle.request.user).values_list(
            "id", flat=True
        )

        if ids:
            id = choice(ids)
            return object_list.filter(added_by=bundle.request.user, id=id)
        else:
            return ids
