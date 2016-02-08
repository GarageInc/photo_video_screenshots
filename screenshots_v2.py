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
    
    
def makeScreenshot( screenShotPath ):
    command = 'DISPLAY=:0 /usr/bin/scrot -q 80 '+screenShotPath+' && /usr/bin/convert -crop 1920x1080+0+0 ' + screenShotPath + ' ' + screenShotPath

    executeCommand( command )


def uploadScreenshot( configs, screenshotPath ):
    command = ' /usr/bin/curl -i \
 -F cmd=terminals.upload_screenshot \
 -F id_terminal=' + configs['ID_TERMINAL'] + ' \
 -F name=file \
 -F file=@' + screenshotPath + ' ' + configs['GATEWAY_UPLOAD_URL']
    
    executeCommand( command )

def reportNotChanged( configs ):
    command = ' /usr/bin/curl -i \
 -F cmd=terminals.screenshot_not_changed \
 -F id_terminal=' + configs['ID_TERMINAL'] + ' ' + configs['GATEWAY_API_URL']
 
    executeCommand( command )
       
def getNewFilePath( configs, newDir ):
    fileSavingDir = newDir  + datetime.datetime.today().strftime('%y-%m-%d_%H') 
    
    if ( os.path.exists( fileSavingDir ) ):
        pass
    else:
        os.mkdir ( fileSavingDir )       
    
    newFileName = str( int(math.ceil(time.time() * 1000)) ) + ".jpg"
    newFilePath = fileSavingDir + "/" + newFileName

    return newFilePath

def run( configs ):
    
    screenshotPath = configs['SCREENSHOT_PATH'];
    savingDir = configs['SCREENSHOTS_SAVING_DIR']    
    
    savingTimeout = int( configs['SCREENSHOT_SAVING_TIMEOUT'] )    
    uploadingTimeout = int( configs['SCREENSHOT_UPLOADING_TIMEOUT'] )
    
    requestAt = 0
    screenshotCopyPath = "";
    sizeOld = 0
    
    while True:   
        startAt = time.time()  
    
        if ( os.path.isfile( screenshotPath ) ):
            sizeOld = os.path.getsize( screenshotPath )
            os.remove( screenshotPath )
        
        makeScreenshot( screenshotPath )        
        
        isChanged = ( sizeOld != os.path.getsize( screenshotPath ) )
        
        # saving
        if ( isChanged ):
            screenshotCopyPath = getNewFilePath( configs, savingDir )
            copyfile( screenshotPath, screenshotCopyPath )
            print( "SAVED: " + screenshotCopyPath )
        else:
            print( "SAVING: pass" )
            pass
            
        # uploading
        if( ( time.time() - requestAt )  >= uploadingTimeout ):
            if ( isChanged ):
                print ( "UPLOADING: " + screenshotCopyPath )
                uploadScreenshot( configs, screenshotCopyPath )
            else:
                print( "UPLOADING: not changed" )
                reportNotChanged( configs )
            requestAt = time.time()
        else:
            pass
            
        remainingTime = savingTimeout - ( time.time() - startAt )
            
        if( remainingTime > 0.1 ):
            time.sleep( remainingTime )
                    
        
                
###############################################################################    
         
initFilePath = '/etc/terminal/osago.ini'

configs = config.readConfigFile( initFilePath )

if ( configs['IS_SCREENSHOT_ENABLED'].lower() == 'true' ):
    run( configs )
    
    
    
    
    

