import random, string
import secrets

from .serializers import ProfileSerializer

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,        
        'userEmail': user.email,
        'userId': user.id,          
        'user': ProfileSerializer(user, context={'request': request}).data
    }

def generate_password():
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for i in range(16))