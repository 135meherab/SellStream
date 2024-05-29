from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .authentication import FirebaseAuthentication
from django.contrib.auth.models import AnonymousUser
from rest_framework import status

class UserProfileView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": "Authenticated user", "user": user})
    


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# import firebase_admin.auth as auth

# class GoogleLoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         id_token = request.data.get("idToken")
#         if not id_token:
#             return Response({"error": "ID token required"}, status=400)

#         try:
#             decoded_token = auth.verify_id_token(id_token)
#         except Exception as e:
#             return Response({"error": str(e)}, status=400)

#         uid = decoded_token.get("uid")
#         email = decoded_token.get("email")

#         # Here you can create the user in your Django app if not exists
#         # For example:
#         # user, created = User.objects.get_or_create(uid=uid, defaults={'email': email})

#         return Response({"uid": uid, "email": email})