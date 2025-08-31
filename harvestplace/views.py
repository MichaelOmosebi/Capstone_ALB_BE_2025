from rest_framework.response import Response
from rest_framework.views import APIView

class WelcomeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            "message": "Welcome to the HarvestPlace API!",
            "description": "Your gateway to connecting farmers and retailers.",
            "docs": "Visit /api/docs/ for API documentation."
        })