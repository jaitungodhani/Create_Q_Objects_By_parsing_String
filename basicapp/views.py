from django.shortcuts import render
from rest_framework.views import APIView
from .models import SchoolModel
from .serializers import Schoolserializer
from .parse_string import parse_search_phrase
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status

class SchoolApi(APIView):
    def post(self, request, *args, **kwargs):
        try:
            parse_string = request.data.get("parse_string", None)

            if not parse_string:
                raise exceptions.NotFound("plz enter filter_string")

            search_filter = parse_search_phrase(parse_string)
            school_filter_obj = SchoolModel.objects.filter(search_filter)
            serializer = Schoolserializer(school_filter_obj, many = True)
            return Response({"data" : serializer.data})
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

