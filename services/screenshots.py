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
    fileSavingDir = newDir  + datetime.datetime.today().strftime('%y-%m-%d_%H') 
    
    if ( os.path.exists( fileSavingDir ) ):
        pass
    else:
        os.mkdir ( fileSavingDir )       
    
    return "%s/%d.jpg"  %( fileSavingDir, math.ceil(time.time() * 1000))

def run():
    global SCREENSHOT_PATH
    global SCREENSHOTS_DATA_DIR
    global SCREENSHOT_INTERVAL
    global SCREENSHOT_UPLOAD_INTERVAL
    
    requestAt = 0
    screenshotCopyPath = "";
    sizeOld = 0
    
    isUploadChanged = False
    
    while True:   
        startAt = time.time()  
    
        if ( os.path.isfile( SCREENSHOT_PATH ) ):
            sizeOld = os.path.getsize( SCREENSHOT_PATH )
            os.remove( SCREENSHOT_PATH )
        
        makeScreenshot( SCREENSHOT_PATH )        
        
        isChanged = ( sizeOld != os.path.getsize( SCREENSHOT_PATH ) )
        isUploadChanged = isUploadChanged or isChanged
        
        # saving
        if ( isChanged ):
            screenshotCopyPath = getNewFilePath( SCREENSHOTS_DATA_DIR )
            copyfile( SCREENSHOT_PATH, screenshotCopyPath )
            print( "SAVED: " + screenshotCopyPath )
        else:
            print( "SAVING: pass" )
            pass
            
        # uploading
        if( ( time.time() - requestAt )  >= SCREENSHOT_UPLOAD_INTERVAL ):
            if ( isUploadChanged ):
                print ( "UPLOADING: " + screenshotCopyPath )
                uploadScreenshot( screenshotCopyPath )
                isUploadChanged = False
            else:
                print( "UPLOADING: not changed" )
                reportNotChanged()
            requestAt = time.time()
        else:
            pass
            
        remainingTime = SCREENSHOT_INTERVAL - ( time.time() - startAt )
            
        if( remainingTime > 0.01 ):
            time.sleep( remainingTime )
                    
        
                
###############################################################################    
         
initFilePath = '/etc/osago/terminal'

configs = config.readConfigFile( initFilePath )

ID_TERMINAL = configs['ID_TERMINAL'] 
GATEWAY_UPLOAD_URL = configs['GATEWAY_UPLOAD_URL']
GATEWAY_API_URL = configs['GATEWAY_API_URL']
    
SCREENSHOT_PATH = configs['SCREENSHOT_PATH'];
SCREENSHOTS_DATA_DIR = configs['SCREENSHOTS_DATA_DIR']    
        
SCREENSHOT_INTERVAL = int( configs['SCREENSHOT_INTERVAL'] )    
SCREENSHOT_UPLOAD_INTERVAL = int( configs['SCREENSHOT_UPLOAD_INTERVAL'] )

IS_SCREENSHOTS_ENABLED = configs['IS_SCREENSHOTS_ENABLED'].lower() == 'true'

if( SCREENSHOTS_DATA_DIR[-1] != '/' ):
	SCREENSHOTS_DATA_DIR+='/'

if ( IS_SCREENSHOTS_ENABLED ):
    run()
    
    
    
    
    

