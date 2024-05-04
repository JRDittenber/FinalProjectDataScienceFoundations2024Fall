from Primary_Folder.logger import logging
from Primary_Folder.exceptions import final_except
import sys 

try:
    a = 1/0

except Exception as e:
    logging.info(e)
    raise final_except(e,sys) from e 



    


