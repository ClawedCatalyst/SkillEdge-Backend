from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def getDetails(request):
    routes = ['Suhail', 'Shreyansh']
    
    return Response(routes)