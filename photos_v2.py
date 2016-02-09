# -*- coding: utf-8 -*-

import os.path
import subprocess
import time
import datetime
import math

from shutil import copyfile

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

def reportNotChanged():
    global GATEWAY_API_URL
    global ID_TERMINAL
    
    command = " /usr/bin/curl -i \
 -F cmd=terminals.photo_not_changed \
 -F id_terminal={0} {1}".format( 
     ID_TERMINAL, 
     GATEWAY_API_URL )
 
    executeCommand( command )
       
def getNewFilePath( newDir ):
    fileSavingDir = newDir  + datetime.datetime.today().strftime('%y-%m-%d_%H') 
    
    if ( os.path.exists( fileSavingDir ) ):
        pass
    else:
        os.mkdir ( fileSavingDir )       
    
    return "%s/%d.jpg"  %( fileSavingDir, math.ceil(time.time() * 1000))

def run():
    global PHOTO_PATH
    global PHOTOS_SAVING_DIR
    global PHOTO_SAVING_TIMEOUT
    global PHOTO_UPLOADING_TIMEOUT
    
    requestAt = 0
    photoCopyPath = "";
    sizeOld = 0
    
    isUploadChanged = False
    
    while True:   
        startAt = time.time()  
    
        if ( os.path.isfile( PHOTO_PATH ) ):
            sizeOld = os.path.getsize( PHOTO_PATH )
            os.remove( PHOTO_PATH )
        
        makePhoto( PHOTO_PATH )        
        
        isChanged = ( sizeOld != os.path.getsize( PHOTO_PATH ) )
        isUploadChanged = isUploadChanged or isChanged
        
        # saving
        if ( isChanged ):
            photoCopyPath = getNewFilePath( PHOTOS_SAVING_DIR )
            copyfile( PHOTO_PATH, photoCopyPath )
            print( "SAVED: " + photoCopyPath )
        else:
            print( "SAVING: pass" )
            pass
            
        # uploading
        if( ( time.time() - requestAt )  >= PHOTO_UPLOADING_TIMEOUT ):
            if ( isUploadChanged ):
                print ( "UPLOADING: " + photoCopyPath )
                uploadPhoto( photoCopyPath )
                isUploadChanged = False
            else:
                print( "UPLOADING: not changed" )
                reportNotChanged()
            requestAt = time.time()
        else:
            pass
            
        remainingTime = PHOTO_SAVING_TIMEOUT - ( time.time() - startAt )
            
        if( remainingTime > 0.01 ):
            time.sleep( remainingTime )
                    
        
                
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
    
    
    
    
    

