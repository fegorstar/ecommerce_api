from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

def success_response(message, data=None, count=None, status_code=status.HTTP_200_OK):
    """
    Generate a standardized success response with optional count.

    Args:
    - message (str): The success message.
    - data (list): Optional data to include in the response (should default to an empty list).
    - count (int): Optional count of items.
    - status_code (int): The HTTP status code for the response.

    Returns:
    - Response: A DRF Response object with the standardized format.
    """
    response_data = {
        "status": status_code,
        "message": message
    }
    if count is not None:
        response_data['count'] = count
    response_data['data'] = data if data is not None else []  # Default to empty list

    return Response(response_data, status=status_code)

def error_response(message, validation_errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Generate a standardized error response with optional validation errors.

    Args:
    - message (str): The error message.
    - validation_errors (dict, list, or str): Optional validation errors or a string.
    - status_code (int): The HTTP status code for the response.

    Returns:
    - Response: A DRF Response object with the standardized format.
    """
    response_data = {
        "status": status_code,
        "message": message,
    }
    
    if validation_errors is not None:
        if isinstance(validation_errors, (dict, list)):
            # If validation_errors is a dictionary or a list, add it directly
            response_data['errors'] = validation_errors
        elif isinstance(validation_errors, str):
            # If it's a string, wrap it in a dictionary with a generic key
            response_data['errors'] = {'error': validation_errors}
        else:
            # Handle unexpected types
            response_data['errors'] = {'error': 'An unknown error occurred.'}

    return Response(response_data, status=status_code)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that formats responses using the error_response function.
    """
    # Call the default exception handler first, to get the standard error response.
    response = exception_handler(exc, context)

    # If a response was generated, customize the format using the error_response function
    if response is not None:
        # Handle permission and authentication errors
        if isinstance(exc, (PermissionDenied, NotAuthenticated)):
            return error_response(
                message=str(exc),  # Use the exception message
                status_code=response.status_code
            )
        # For other types of exceptions, use the error message from the response if available
        message = response.data.get('detail', 'An error occurred.')
        return error_response(
            message=message,
            status_code=response.status_code
        )
    
    # If the exception was not handled by DRF's default exception handler, return None
    return response
