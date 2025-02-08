from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from polis.polisy_file_serializer import PolicyFileSerializer

@api_view(['POST'])
def create_polisy_file(request):
    print(request.data)
    serializer = PolicyFileSerializer(data=request.data)
    if serializer.is_valid():
        try:
            policy_file = serializer.save()
            return Response(
                PolicyFileSerializer(policy_file).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print("Exception during save:", e)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        print("Validation errors:", serializer.errors) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)