from sre_parse import State
import requests
from datetime import datetime

from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import OrderConsultingSerializer,ConsultingPlanSerializer
from .models import OrderConsulting,ConsultingPlan


@api_view(["GET"])
def getPlans(request):
    plans = ConsultingPlan.objects.all().order_by("-createdAt")
    serializer = ConsultingPlanSerializer(plans, many=True)
    return Response(serializer.data)     

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createOrder(request):
    user = request.user
    data = request.data

    try:
        plan= ConsultingPlan.objects.get(id=data["planId"])
        
        try:
            tax = plan.price * 0.09
            orderCred = {
                    'pin' : 'aqayepardakht', #TODO change this 
                    'amount' : int(plan.price + tax),
                    'callback' : 'https://localhost/consulting/order/verify/',#TODO change this   
                }
            response = requests.post("https://panel.aqayepardakht.ir/api/create", data=orderCred)
            if response.status_code == 200 and not response.text.replace('-',"").isdigit():
                url ='https://panel.aqayepardakht.ir/startpay/'+response.text
                
                order= OrderConsulting.objects.create(
                    user=user,
                    plan=plan,
                    transId=response.text,
                    url=url
                )
                serializer= OrderConsultingSerializer(order, many=False)
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
    orders = user.orderconsulting_set.all().order_by("-createdAt")
    serializer = OrderConsultingSerializer(orders , many=True)
    return Response(serializer.data)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getOrderById(request,id):
    user= request.user
    try:
        order= OrderConsulting.objects.get(transId=id)

        if user.is_staff or order.user == user:
            serializer = OrderConsultingSerializer(order,many=False)
            return Response(serializer.data)

        else:
            return Response({"details": "Not authorize to view this order"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'details': "Order does not exist"}, status= status.HTTP_400_BAD_REQUEST)



@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, id):
    order = OrderConsulting.objects.get(transId=id)
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
                return Response({"message": "???????????? ???? ???????????? ?????????? ????"}, status=status.HTTP_200_OK)
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
 