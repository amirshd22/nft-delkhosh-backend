import requests

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from datetime import datetime

from .models import AdvertisingPlan,OrderAdvertising
from .serializers import OrderAdvertisingSerializer,AdvertisingPlanSerializer


@api_view(["GET"])
def getAdvertisingPlans(request):
    plans= AdvertisingPlan.objects.all().order_by("-createdAt")
    serializer = AdvertisingPlanSerializer(plans, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createOrder(request):
    user= request.user
    data= request.data
    try:
        plan= AdvertisingPlan.objects.get(id=data["planId"])
        try:
            orderCred = {
                    'pin' : '63A01E4D9C3A023E66A0', #TODO change this 
                    'amount' : int(plan.price),
                    'callback' : 'https://cocobeauty.ir/verify/',#TODO change this   
                }
            response = requests.post("https://panel.aqayepardakht.ir/api/create", data=orderCred)
            if response.status_code == 200 and not response.text.replace('-',"").isdigit():
                url ='https://panel.aqayepardakht.ir/startpay/'+response.text
            
                order= OrderAdvertising.objects.create(
                    user=user,
                    plan=plan,
                    description=data["description"],
                    link=data["link"],
                    image=request.FILES["image"],
                    transId=response.text,
                    url=url
                )
                serializer= OrderAdvertisingSerializer(order, many=False)
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
    orders = user.orderadvertising_set.all().order_by("-createdAt")
    serializer = OrderAdvertisingSerializer(orders , many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def getAllOrders(request):
    orders= OrderAdvertising.objects.all().order_by("-createdAt")
    serializer= OrderAdvertisingSerializer(orders,many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getOrderById(request,id):
    user= request.user
    try:
        order= OrderAdvertising.objects.get(id=id)

        if user.is_staff or order.user == user:
            serializer = OrderAdvertisingSerializer(order,many=False)
            return Response(serializer.data)

        else:
            return Response({"details": "Not authorize to view this order"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'details': "Order does not exist"}, status= status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, id):
    order = OrderAdvertising.objects.get(transId=id)
    data = {
    'pin' : '63A01E4D9C3A023E66A0',
    'amount' : int(order.plan.price),
    'transid' : order.transId
    }
    try:
        if order.user == request.user:

            # response = requests.post('https://panel.aqayepardakht.ir/api/verify', data = data)
            response= 1
            if response == 1:
                print(response, "success")
                order.isPaid = True
                order.paidAt = datetime.now() #TODO update the amount of the people_used
                order.save()
                return Response({"message": "پرداخت با موفقیت انجام شد"}, status=status.HTTP_200_OK)
            elif response.status_code == 200 and response.text =='0':
                print(response, "else if error")
                return Response({"details": f"پرداخت با موفقیت انجام نشد {response.text}"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print(response, "else Error")
                return Response({"details": f"تراکنش با موفقیت انجام نشد {response.text}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"details":"مشکلی رخ داده لطفا بعدا دوباره تلاش کنید"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({"details": f"{e}"})
    