from rest_framework.response import Response
from rest_framework.views import APIView
from newbee.newbee_util.crud import find_util, add_util, update_util, delete_util


class NewBeeView(APIView):
    def get(self, request, action):
        return Response(*find_util(request, action))

    def post(self, request, action):
        return Response(*add_util(request, action))

    def put(self, request, action):
        return Response(*update_util(request, action))

    def delete(self, request, action):
        return Response(*delete_util(request, action))
