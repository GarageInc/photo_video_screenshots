# -*- coding: utf-8 -*-

import math

from shutil import move
from datetime import datetime
from time import time, sleep
from os import path, mkdir

import config

def executeCommand( command ):
    #print( command )
    subprocess.call( command, shell=True, stderr=subprocess.STDOUT)
    
def makePhoto( photoPath ):    
    global PHOTO_INPUT_DEVICE
    
    command = "/usr/bin/streamer -c {0} -s 1920x1080 -f jpeg -o {1}".format(
        PHOTO_INPUT_DEVICE,
        photoPath);
    
    executeCommand( command )

def uploadPhoto( photoPath ):
    global GATEWAY_UPLOAD_URL
    global ID_TERMINAL
    
    command = " /usr/bin/curl -i \
 -F cmd=terminals.upload_photo \
 -F id_terminal={0} \
 -F name=file \
 -F file=@{1} {2}".format( 
     ID_TERMINAL, 
     photoPath, 
     GATEWAY_UPLOAD_URL )
    
    executeCommand( command )
       
def getNewFilePath( newDir ):
    fileSavingDir = newDir  + datetime.today().strftime('%y-%m-%d_%H') 
    
    if ( path.exists( fileSavingDir ) ):
        pass
    else:
        mkdir ( fileSavingDir )       
    
    return "%s/%d.jpeg"  %( fileSavingDir, math.ceil(time() * 1000))

def run():
    global PHOTO_PATH
    global PHOTOS_SAVING_DIR
    global PHOTO_SAVING_TIMEOUT
    global PHOTO_UPLOADING_TIMEOUT
    
    requestAt = 0
    photoCopyPath = "";
        
    while True:   
        startAt = time.time()  
            
        makePhoto( PHOTO_PATH )   
        
        # saving
        photoCopyPath = getNewFilePath( PHOTOS_SAVING_DIR )
        move( PHOTO_PATH, photoCopyPath )
        print ( "SAVED: " + photoCopyPath )
            
        # uploading
        if ( ( time() - requestAt )  >= PHOTO_UPLOADING_TIMEOUT ):
            print ( "UPLOADING: " + photoCopyPath )
            uploadPhoto( photoCopyPath )
            requestAt = time()
        else:
            pass
            
        remainingTime = PHOTO_SAVING_TIMEOUT - ( time() - startAt )
            
        if( remainingTime > 0.01 ):
            sleep( remainingTime )
                    
        
                
###############################################################################    
         
initFilePath = '/etc/terminal/osago.ini'

configs = config.readConfigFile( initFilePath )

GATEWAY_UPLOAD_URL = configs['GATEWAY_UPLOAD_URL']
GATEWAY_API_URL = configs['GATEWAY_API_URL']
ID_TERMINAL = configs['ID_TERMINAL'] 
    
PHOTO_PATH = configs['PHOTO_PATH'];
PHOTOS_SAVING_DIR = configs['PHOTOS_SAVING_DIR']    
        
PHOTO_SAVING_TIMEOUT = int( configs['PHOTO_SAVING_TIMEOUT'] )    
PHOTO_UPLOADING_TIMEOUT = int( configs['PHOTO_UPLOADING_TIMEOUT'] )
IS_PHOTO_ENABLED = configs['IS_PHOTO_ENABLED'].lower() == 'true'

PHOTO_INPUT_DEVICE = configs['PHOTO_INPUT_DEVICE']

if ( IS_PHOTO_ENABLED ):
    run()
    
    
    
    
    

