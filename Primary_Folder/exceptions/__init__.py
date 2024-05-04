import os 
import sys 

def error_message(error, error_detail:sys):
    _,_,exc_tb =error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred name [{0}] line number [{1}] error meesage [{2}]".format(file_name, exc_tb.tb_lineno, error_detail, str(error))
    return error_message 

class final_except(Exception):
    def __init__(self, error_message, error_detail):
        
        super.__init__(error_message)
        self.error_message = error_message(
            error_message, error_detail=error_detail
        )
        
def __str__(self):
    return self.error_message
