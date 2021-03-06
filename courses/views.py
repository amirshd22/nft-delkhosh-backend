from datetime import datetime
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import CourseReview, OrderCourses,OwnedCourse,Course
from .serializers import OrderCourseSerializer,OwnedCourseWithFileSerializer,OwnedCourseWithoutFileSerializer,CourseSerializerWithFile,CourseSerializerWithoutFile



@api_view(["GET"])
def getCourses(request):
    courses = Course.objects.all().order_by("-createdAt")
    serializer = CourseSerializerWithoutFile(courses,many=True)
    return Response(serializer.data)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createOrder(request):
    user= request.user
    data= request.data
    
    try:
        course= Course.objects.get(id=data["courseId"])
        
        try:
            tax = course.price * 0.09
            orderCred = {
                    'pin' : 'aqayepardakht', #TODO change this 
                    'amount' : int(course.price + tax),
                    'callback' : 'https://cocobeauty.ir/verify/',#TODO change this   
                }
            response = requests.post("https://panel.aqayepardakht.ir/api/create", data=orderCred)
            if response.status_code == 200 and not response.text.replace('-',"").isdigit():
                url ='https://panel.aqayepardakht.ir/startpay/'+response.text
                
                order= OrderCourses.objects.create(
                    user=user,
                    course=course,
                    transId=response.text,
                    url=url
                )
                serializer= OrderCourseSerializer(order, many=False)
                return Response(serializer.data)
            else:
                return Response("Error")
        
        except Exception as e:
            return Response({"details":f"{e}"})
    except Exception as e:
        return Response({"details":f"{e}"})




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.ordercourse_set.all().order_by("-createdAt")
    serializer = OrderCourseSerializer(orders , many=True)
    return Response(serializer.data)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getOrderById(request,id):
    user= request.user
    try:
        order= OrderCourses.objects.get(transId=id)

        if user.is_staff or order.user == user:
            serializer = OrderCourseSerializer(order,many=False)
            return Response(serializer.data)

        else:
            return Response({"details": "Not authorize to view this order"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'details': "Order does not exist"}, status= status.HTTP_400_BAD_REQUEST)





@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getMyCourses(request): 
    user = request.user
    try:
        courses= OwnedCourse.objects.filter(user=user).order_by("-createdAt")
        serializer = OwnedCourseWithoutFileSerializer(courses, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"details":f"{e}"}, status= status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def getCourseDetails(request,id):
    user = request.user
    try:
        course = Course.objects.get(id=id)
        if user.is_authenticated:
            
            try:
                ownedCourse = OwnedCourse.objects.get(course=course,user=user)
                serializer = OwnedCourseWithFileSerializer(ownedCourse, many=False)    
            except:
                serializer = CourseSerializerWithoutFile(course, many=False)   
        else:
            serializer = CourseSerializerWithoutFile(course, many=False)    
        return Response(serializer.data)
    except Exception as e:
        return Response({"details": f"{e}"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, id):
    user = request.user
    order = OrderCourses.objects.get(transId=id)
    data = {
    'pin' : '63A01E4D9C3A023E66A0',
    'amount' : int(order.plan.price),
    'transid' : order.transId
    }
    try:
        if order.user == user :
                
            # response = requests.post('https://panel.aqayepardakht.ir/api/verify', data = data)
            response= 1
            if response == 1:
                print(response, "success")
                order.isPaid = True
                order.paidAt = datetime.now() #TODO update the amount of the people_used
                order.save()
                try:
                    userCourse = OwnedCourse.objects.create(
                        user=user,
                        course= order.course,
                    )
                    return Response({"message": "???????????? ???? ???????????? ?????????? ????"}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"details": f"{e}"},status=status.HTTP_400_BAD_REQUEST)
            elif response.status_code == 200 and response.text =='0':
                print(response, "else if error")
                return Response({"details": f"???????????? ???? ???????????? ?????????? ?????? {response.text}"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print(response, "else Error")
                return Response({"details": f"???????????? ???? ???????????? ?????????? ?????? {response.text}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"details":"?????????? ???? ???????? ???????? ???????? ???????????? ???????? ????????"}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return Response({"details": f"{e}"})




# Course Review

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createCourseReview(request,id):
    course = Course.objects.get(id=id)
    user = request.user
    data = request.data

    alreadyExists = course.courseReview_set.filter(user=user).exists()
    if alreadyExists:
        content = {
            "details": "?????? ?????????? ?????? ???????? ??????"
        }
        return Response(content , status=status.HTTP_400_BAD_REQUEST)
    
    # elif data["rate"] == 0:
    #     content = {
    #         "details": "???????? ?????????????? ???? ???????????? ????????"
    #     }
    #     return Response(content , status=status.HTTP_400_BAD_REQUEST)
    else:
        review= CourseReview.objects.create(
            user=user,
            course=course,
            content = data['content']
        )
        return Response({"details": "?????? ?????? ???? ???????????? ?????????? ????"})