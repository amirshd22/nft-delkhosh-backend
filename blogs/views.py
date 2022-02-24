from re import L
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from rest_framework.pagination import PageNumberPagination

from .models import Blog,Like
from .serializers import BlogSerializer

@api_view(["GET"])
def getBlogs(request):
    blogs= Blog.objects.all().order_by("-createdAt")
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(blogs, request)
    serializer = BlogSerializer(result_page,many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_like(request):
    user= request.user
    data= request.data
    try:
        blog= Blog.objects.get(id=data["id"])
        like,created= Like.objects.get_or_create(
            user=user,
            blog=blog
        )
        if created:
            like.delete()
        return Response({"details":"لایک با موفقیت انجام شد"},status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"details":f"{e}"},status=status.HTTP_400_BAD_REQUEST)
