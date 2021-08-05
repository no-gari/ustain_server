from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PushToken
from .serializers import PushTokenSerializer
from django.shortcuts import get_object_or_404


class PushTokenAPIView(APIView):

    def post(self, request):
        if 'flag' in request.data:
            instance = get_object_or_404(PushToken.objects.all(), token=request.data['push_token'])
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            request.data['token'] = request.data['push_token']
            query = PushToken.objects.filter(token=request.data['token'])
            if query.exists():
                serializer = PushTokenSerializer(query.first(), data=request.data)
            else:
                serializer = PushTokenSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






