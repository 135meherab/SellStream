# views.py
import string
import random
import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

class InitiatePaymentView(APIView):

    def post(self, request):
        payment_data = {
            'store_id': settings.SSLCOMMERZ_STORE_ID,
            'store_passwd': settings.SSLCOMMERZ_STORE_PASSWORD,
            'total_amount': request.data.get('amount'),
            'currency': 'BDT',
            'tran_id': '12345678',  # Unique transaction ID
            'success_url': 'https://sell-stream.netlify.app/dashboard/main',
            'fail_url': 'https://sell-stream.netlify.app/dashboard/main',
            'cancel_url': 'https://sell-stream.netlify.app/dashboard/main',
            'cus_name': request.data.get('customer_name'),
            'cus_email': request.data.get('customer_email'),
            'cus_phone': request.data.get('customer_phone'),
            'cus_add1' : request.data.get('address1'),
            'cus_city' : request.data.get('address2'),
            'cus_country' : 'Bangladesh',
            'shipping_method' : 'NO',
            'multi_card_name' : "",
            'num_of_item' : 1,
            'product_name' : "Test",
            'product_category' : "Test Category",
            'product_profile' : "general",
            'value_a' : 'name',
            # Add other required fields
        }

        response = requests.post(
            'https://sandbox.sslcommerz.com/gwprocess/v4/api.php',
            data=payment_data
        )

        return Response(response.json())



# views.py
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

@csrf_exempt
@api_view(['POST'])
def payment_success(request):
    # Handle the successful payment here
    return Response({'message': 'Payment successful', 'data': request.data})

@csrf_exempt
@api_view(['POST'])
def payment_fail(request):
    # Handle the failed payment here
    return Response({'message': 'Payment failed', 'data': request.data})

@csrf_exempt
@api_view(['POST'])
def payment_cancel(request):
    # Handle the cancelled payment here
    return Response({'message': 'Payment cancelled', 'data': request.data})

# views.py
import requests

@csrf_exempt
@api_view(['POST'])
def payment_success(request):
    val_id = request.data.get('val_id')

    verification_url = f"https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php?val_id={val_id}&store_id={settings.SSLCOMMERZ_STORE_ID}&store_passwd={settings.SSLCOMMERZ_STORE_PASSWORD}&v=1&format=json"

    verification_response = requests.get(verification_url)
    verification_data = verification_response.json()

    if verification_data['status'] == 'VALID':
        # Payment is verified
        return Response({'message': 'Payment verified', 'data': verification_data})
    else:
        return Response({'message': 'Payment verification failed', 'data': verification_data})
