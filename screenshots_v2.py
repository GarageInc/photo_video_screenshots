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
    
    
def makeScreenShot( screenShotPath ):
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
   

def move( configs, screenshotPath, savingDir ):
    fileSavingDir = savingDir  + datetime.datetime.today().strftime('%y-%m-%d_%H') 
    
    if ( os.path.exists( fileSavingDir ) ):
        pass
    else:
        os.mkdir ( fileSavingDir )       
    
    fileExtension = os.path.splitext( os.path.basename( screenshotPath ) )[1];

    newFileName = str( int(math.ceil(time.time() * 1000)) ) + fileExtension
    copyfile( screenshotPath, fileSavingDir + "/" + newFileName)

def saving( configs, screenshotPath, savingDir ):

    sizeOld = 0
    
    if ( os.path.isfile( screenshotPath ) ):
        sizeOld = os.path.getsize( screenshotPath )
        os.remove( screenshotPath )
    
    makeScreenShot( screenshotPath )
    
    sizeNew = os.path.getsize( screenshotPath )     
            
    if ( sizeNew != sizeOld ):
        print( "SAVING: success" )
        move( configs, screenshotPath, savingDir )
    else:
        print( "SAVING: pass" )
        pass
    
def uploading( configs, screenshotPath ):
    
    sizeOld = 0
    
    if ( os.path.isfile( screenshotPath ) ):
        sizeOld = os.path.getsize( screenshotPath )
        os.remove( screenshotPath )
    
    makeScreenShot( screenshotPath )
    
    sizeNew = os.path.getsize( screenshotPath )     
            
    if ( sizeNew != sizeOld ):
        print ( "UPLOADING: success" )
        uploadScreenshot( configs, screenshotPath )
    else:
        print( "UPLOADING: not changed" )
        reportNotChanged( configs )

def run( configs ):
    
    screenshotPath = configs['SCREENSHOT_PATH'];
    savingDir = configs['SCREENSHOTS_SAVING_DIR']    
    
    savingTimeout = int( configs['SCREENSHOT_SAVING_TIMEOUT'] )    
    uploadingTimeout = int( configs['SCREENSHOT_UPLOADING_TIMEOUT'] )
    
    lastUploading = 0
    
    while True:   
        # uploading            
        currentTime = time.time();
                
        timeRemaining = uploadingTimeout - (currentTime - lastUploading)
            
        if( timeRemaining < 0 ):
            uploading( configs, screenshotPath )
            lastUploading = time.time()
            
        # saving 
        startSaving = time.time()  
        
        saving( configs, screenshotPath, savingDir )

        finishSaving = time.time()
                
        timeRemaining = savingTimeout - (finishSaving - startSaving)
            
        if( timeRemaining > 0.1 ):
            time.sleep( timeRemaining )
                    
        
                
###############################################################################    
         
initFilePath = '/etc/terminal/osago.ini'

configs = config.readConfigFile( initFilePath )

if ( configs['IS_SCREENSHOT_ENABLED'].lower() == 'true' ):
    run( configs )
    
    
    
    
    

