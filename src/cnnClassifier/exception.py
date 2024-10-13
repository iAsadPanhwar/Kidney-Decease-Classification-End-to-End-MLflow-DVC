import sys
from cnnClassifier.logger import logging


def error_message_detail(error):
    
    """
    Extracts detailed information about an error.
    
    Args:
        error (Exception): The exception instance.
        
    Returns:
        str: A formatted string containing the filename, line number, and error message.
    """
    
    _, _, exc_tb = sys.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error))
    
    return error_message
    
class CustomException(Exception):
    """
    Custom Exception class that provides detailed error messages.
    """
    
    def __init__(self, error_message):
        
        """
        Initializes the CustomException.
        
        Args:
            error_message (str): The error message.
        """
        
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message)
    
    def __str__(self):
        """
        Returns the detailed error message.
        
        Returns:
            str: The error message with script and line details.
        """
        
        return self.error_message
    