from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .authentication import FirebaseAuthentication

class UserProfileView(APIView):
    authentication_classes = [FirebaseAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Authenticated user", "user": request.user})