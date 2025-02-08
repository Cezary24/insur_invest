import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from polis.polisy_file_serializer import PolicyFileSerializer
from utils.utils_gemini import send_gemini_request
from utils.prompt import PROMPT
from utils.utils_validation import load_json_from_string
import traceback

logger = logging.getLogger(__name__)

@api_view(['POST'])
def create_polisy_file(request):
    serializer = PolicyFileSerializer(data=request.data)
    
    if not serializer.is_valid():
        logger.error(f"Validation errors: {serializer.errors}")
        return Response({
            "status": "error",
            "message": "Invalid input data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Save the initial file
        policy_file = serializer.save()
        
        # Get Gemini response
        gemini_response = send_gemini_request(
            prompt=PROMPT,
            pdf_path=policy_file.file.path
        )
        
        # Log the Gemini response for debugging
        logger.debug(f"Gemini response: {gemini_response}")
        
        # Check for API error response
        if "error" in gemini_response:
            raise ValueError(f"Gemini API error: {gemini_response['error']}")
        
        # Extract the text content from Gemini response
        try:
            llm_text = gemini_response["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as e:
            logger.error(f"Failed to extract text from Gemini response: {gemini_response}")
            raise ValueError(f"Invalid Gemini API response structure: {str(e)}")
        
        # Log the extracted text
        logger.debug(f"Extracted LLM text: {llm_text}")
        
        # Process and validate the JSON
        try:
            processed_json = load_json_from_string(llm_text)
        except ValueError as e:
            logger.error(f"JSON processing error. Input text: {llm_text}")
            raise ValueError(f"JSON processing error: {str(e)}")
        
        # Log the processed JSON
        logger.debug(f"Processed JSON: {processed_json}")
        
        # Update the policy file with processed data
        for key, value in processed_json.items():
            if hasattr(policy_file, key):  # Only set attributes that exist on the model
                setattr(policy_file, key, value)
        
        policy_file.processed_data = processed_json
        policy_file.save()
        
        return Response({
            "status": "success",
            "message": "File processed successfully",
            "data": PolicyFileSerializer(policy_file).data,
            "processed_json": processed_json
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        # Get the full traceback
        tb = traceback.format_exc()
        logger.error(f"Error processing policy file: {str(e)}\nTraceback: {tb}")
        
        error_message = str(e)
        if "Gemini API error" in error_message:
            return Response({
                "status": "error",
                "message": "Failed to process file with AI service",
                "detail": error_message
            }, status=status.HTTP_502_BAD_GATEWAY)
        elif "JSON processing error" in error_message:
            return Response({
                "status": "error",
                "message": "Failed to process extracted data",
                "detail": error_message
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response({
                "status": "error",
                "message": "Internal server error",
                "detail": error_message,
                "traceback": tb if not isinstance(e, ValueError) else None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)