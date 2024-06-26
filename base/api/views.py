from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Space
from .serializers import SpaceSerializer

@api_view(["GET"])
def getroute(request):
    
    routes = [
        "GET/ api/",
        "GET/ api/rooms", #an api for people to see all the rooms in our application
        "GET/ api/rooms:id", 
    ]
    return Response(routes) 


@api_view(["GET"])
def getspaces(request):
    space = Space.objects.all()
    
    serializer = SpaceSerializer(space, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getspace(request, pk):
    space = Space.objects.get(id=pk)
    
    serializer = SpaceSerializer(space, many=False)
    return Response(serializer.data)