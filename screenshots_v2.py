# -*- coding: utf-8 -*-

import math
import subprocess

from shutil import copyfile
from datetime import datetime
from time import time, sleep
from os import path, mkdir, remove

import config

def executeCommand( command ):
    #print( command )
    subprocess.call( command, shell=True, stderr=subprocess.STDOUT)
    
def makeScreenshot( screenshotPath ):
    command = "DISPLAY=:0 /usr/bin/scrot -q 80 {0} && /usr/bin/convert -crop 1920x1080+0+0 {1} {2}".format(
        screenshotPath, 
        screenshotPath, 
        screenshotPath )
    executeCommand( command )

def uploadScreenshot( screenshotPath ):
    global GATEWAY_UPLOAD_URL
    global ID_TERMINAL
    
    command = " /usr/bin/curl -i \
 -F cmd=terminals.upload_screenshot \
 -F id_terminal={0} \
 -F name=file \
 -F file=@{1} {2}".format( 
     ID_TERMINAL, 
     screenshotPath, 
     GATEWAY_UPLOAD_URL )
    
    executeCommand( command )

def reportNotChanged():
    global GATEWAY_API_URL
    global ID_TERMINAL
    
    command = " /usr/bin/curl -i \
 -F cmd=terminals.screenshot_not_changed \
 -F id_terminal={0} {1}".format( 
     ID_TERMINAL, 
     GATEWAY_API_URL )
 
    executeCommand( command )
       
def getNewFilePath( newDir ):
    fileSavingDir = newDir  + datetime.today().strftime('%y-%m-%d_%H') 
    
    if ( path.exists( fileSavingDir ) ):
        pass
    else:
        mkdir ( fileSavingDir )       
    
    return "%s/%d.jpg"  %( fileSavingDir, math.ceil(time() * 1000))

def run():
    global SCREENSHOT_PATH
    global SCREENSHOTS_SAVING_DIR
    global SCREENSHOT_SAVING_TIMEOUT
    global SCREENSHOT_UPLOADING_TIMEOUT
    
    requestAt = 0
    screenshotCopyPath = "";
    sizeOld = 0
    
    isUploadChanged = False
    
    while True:   
        startAt = time()  
    
        if ( path.isfile( SCREENSHOT_PATH ) ):
            sizeOld = path.getsize( SCREENSHOT_PATH )
            remove( SCREENSHOT_PATH )
        
        makeScreenshot( SCREENSHOT_PATH )        
        
        isChanged = ( sizeOld != path.getsize( SCREENSHOT_PATH ) )
        isUploadChanged = isUploadChanged or isChanged
        
        # saving
        if ( isChanged ):
            screenshotCopyPath = getNewFilePath( SCREENSHOTS_SAVING_DIR )
            copyfile( SCREENSHOT_PATH, screenshotCopyPath )
            print( "SAVED: " + screenshotCopyPath )
        else:
            print( "SAVING: pass" )
            pass
            
        # uploading
        if( ( time() - requestAt )  >= SCREENSHOT_UPLOADING_TIMEOUT ):
            if ( isUploadChanged ):
                print ( "UPLOADING: " + screenshotCopyPath )
                uploadScreenshot( screenshotCopyPath )
                isUploadChanged = False
            else:
                print( "UPLOADING: not changed" )
                reportNotChanged()
            requestAt = time()
        else:
            pass
            
        remainingTime = SCREENSHOT_SAVING_TIMEOUT - ( time() - startAt )
            
        if( remainingTime > 0.01 ):
            sleep( remainingTime )
                    
        
                
###############################################################################    
         
initFilePath = '/etc/terminal/osago.ini'

configs = config.readConfigFile( initFilePath )

GATEWAY_UPLOAD_URL = configs['GATEWAY_UPLOAD_URL']
ID_TERMINAL = configs['ID_TERMINAL'] 
GATEWAY_API_URL = configs['GATEWAY_API_URL']
    
SCREENSHOT_PATH = configs['SCREENSHOT_PATH'];
SCREENSHOTS_SAVING_DIR = configs['SCREENSHOTS_SAVING_DIR']    
        
SCREENSHOT_SAVING_TIMEOUT = int( configs['SCREENSHOT_SAVING_TIMEOUT'] )    
SCREENSHOT_UPLOADING_TIMEOUT = int( configs['SCREENSHOT_UPLOADING_TIMEOUT'] )
IS_SCREENSHOT_ENABLED = configs['IS_SCREENSHOT_ENABLED'].lower() == 'true'

if ( IS_SCREENSHOT_ENABLED ):
    run()
    
    
    
    
    

