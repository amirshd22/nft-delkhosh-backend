from datetime import datetime
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import OrderCourses,OwnedCourse,Course
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
            orderCred = {
                    'pin' : '63A01E4D9C3A023E66A0', #TODO change this 
                    'amount' : int(course.price),
                    'callback' : 'https://cocobeauty.ir/verify/',#TODO change this   
                }
            response = requests.post("https://panel.aqayepardakht.ir/api/create", data=orderCred)
            if response.status_code == 200 and not response.text.replace('-',"").isdigit():
            
                order= OrderCourses.objects.create(
                    user=user,
                    course=course,
                    transId=response.text
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
        order= OrderCourses.objects.get(id=id)

        if user.is_staff or order.user == user:
            serializer = OrderCourseSerializer(order,many=False)
            return Response(serializer.data)

        else:
            return Response({"details": "Not authorize to view this order"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'details': "Order does not exist"}, status= status.HTTP_400_BAD_REQUEST)




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
                return Response({"message": "پرداخت با موفقیت انجام شد"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"details": f"{e}"},status=status.HTTP_400_BAD_REQUEST)
        elif response.status_code == 200 and response.text =='0':
            print(response, "else if error")
            return Response({"details": f"پرداخت با موفقیت انجام نشد {response.text}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(response, "else Error")
            return Response({"details": f"تراکنش با موفقیت انجام نشد {response.text}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"details": f"{e}"})
    