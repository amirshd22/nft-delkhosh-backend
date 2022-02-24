from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import Userprofile
from .serializers import UserProfileSerializer,UserSerializerWithToken

from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView




class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    # throttle_classes = [RegiserAnonRate]
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        messages = {'errors':[]}
        if username == None:
            messages['errors'].append('username can\'t be empty')
        if password == None:
            messages['errors'].append('Password can\'t be empty')  
        if User.objects.filter(username__iexact=username).exists():
            messages['errors'].append("Account already exists with this username.") 
        if len(messages['errors']) > 0:
            print(messages["errors"])
            return Response({"details":messages['errors']},status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create(
                username=username,
                password=make_password(password)
            )
            serializer = UserSerializerWithToken(user, many=False)
        except Exception as e:
            print(e)
            return Response({'details':f'{e}'},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # throttle_classes =[LoginAnonRate]
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['is_staff'] = user.is_staff
        token['id'] = user.id

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user
    try:
        profile = Userprofile.objects.get(user=user)
        serializer = UserProfileSerializer(profile, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({"details":f"{e}"})


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def editProfile(request):
    user = request.user
    data = request.data
    try:
        profile = Userprofile.objects.get(user=user)
        if profile.user == user:
            profile.first_name = data["first_name"]
            profile.last_name = data["last_name"]
            profile.email = data["email"]
            profile.save()
            return Response("تغییرات با موفقیت انجام شد", status= status.HTTP_202_ACCEPTED)
        else:
            return Response("خطایی رخ داده لطفا بعدا دوباره تلاش کنید", status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
         return Response({"details": f"{e}"},status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteUser(request):
    user = request.user
    try:
        profile = Userprofile.objects.get(user=user)
        if profile.user == user:
            profile.delete()
            return Response(":(با موفقیت انجام شد", status= status.HTTP_202_ACCEPTED)
        else:
            return Response("خطایی رخ داده لطفا بعدا دوباره تلاش کنید", status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
         return Response({"details": f"{e}"},status=status.HTTP_400_BAD_REQUEST)

