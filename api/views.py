from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .bert import Answer, run_model

@api_view(['POST'])
def get_class(request):
    if request.method == 'POST':
        data = run_model(request.data)
        return Response(data, status=status.HTTP_201_CREATED)