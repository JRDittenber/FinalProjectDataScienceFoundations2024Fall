import os
import sys

def error_message(error, error_detail: sys):
    """
    Generate a detailed error message.

    Args:
        error: The error that occurred.
        error_detail (sys): System information about the error.

    Returns:
        str: A formatted error message.
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    message = (
        "Error occurred in file [{0}] at line number [{1}] error message [{2}]"
        .format(file_name, exc_tb.tb_lineno, str(error))
    )
    return message

class final_except(Exception):
    def __init__(self, error, error_detail):
        """
        Initialize the final_except class with an error message and details.

        Args:
            error: The error that occurred.
            error_detail (sys): System information about the error.
        """
        super().__init__(error_message(error, error_detail))
        self.error_message = error_message(error, error_detail)
    
    def __str__(self):
        return self.error_message
