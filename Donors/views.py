from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

# Create your views here.

# Disable CSRF protection for the GraphQL view
@csrf_exempt
class MyGraphQLView(GraphQLView):
    pass