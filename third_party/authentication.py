import firebase_admin.auth as auth
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        id_token = request.META.get("HTTP_AUTHORIZATION")
        if not id_token:
            return None

        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise AuthenticationFailed("Invalid Firebase ID token")

        uid = decoded_token.get("uid")
        if not uid:
            raise AuthenticationFailed("Invalid user")

        return (uid, None)