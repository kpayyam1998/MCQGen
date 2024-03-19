import logging
import os
from datetime import datetime



LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" # set the file format

log_path=os.path.join(os.getcwd(),"logs")# get the current path directory and save file name will be logs
os.makedirs(log_path,exist_ok=True) # if its exisit also Make true

LOG_FILE_PATH=os.path.join(log_path,LOG_FILE) # first parameter is passing the path and 2nd file name

logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE_PATH,# this is for entire file name
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s" # mention diff 1 . which is current 2.line no 3. label 4 message
)
# we are gng to capture evrything 