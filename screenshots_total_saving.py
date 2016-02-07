# -*- coding: utf-8 -*-

import os.path
import subprocess
import time
import datetime

from shutil import move

import config


def executeCommand( command ):
    #print( command )
    subprocess.call( command, shell=True, stderr=subprocess.STDOUT)
    
    
def makeScreenShot( screenShotPath ):
    command = 'DISPLAY=:0 /usr/bin/scrot -q 80 '+screenShotPath+' && /usr/bin/convert -crop 1920x1080+0+0 ' + screenShotPath + ' ' + screenShotPath

    executeCommand( command )


def uploadScreenshot( screenShotPath, configs ):
    command = ' /usr/bin/curl -i \
 -F cmd=terminals.upload_screenshot \
 -F id_terminal=' + configs['ID_TERMINAL'] + ' \
 -F name=file \
 -F file=@' + screenShotPath + ' ' + configs['GATEWAY_UPLOAD_URL']
    
    executeCommand( command )

def reportScreenshotNotChanged( configs ):
    command = ' /usr/bin/curl -i \
 -F cmd=terminals.screenshot_not_changed \
 -F id_terminal=' + configs['ID_TERMINAL'] + ' ' + configs['GATEWAY_API_URL']
 
    executeCommand( command )
   
   
sizeOld = 0  
fileForUploading = "";

def moveToSave( configs, screenShotPath ):
    fileSavingDir = configs['SCREENSHOTS_SAVING_DIR'] + datetime.datetime.today().strftime('%y-%m-%d_%H') 
    print ( fileSavingDir )
    
    if ( os.path.exists( fileSavingDir ) ):
        pass
    else:
        os.mkdir ( fileSavingDir )       
    
    fileName = os.path.basename( screenShotPath )
    fileExtension = os.path.splitext(fileName)[1];

    newFileName = str( int(round(time.time() * 1000)) ) + fileExtension
    move( screenShotPath, fileSavingDir + "/" + newFileName)
    
    global fileForUploading
    fileForUploading =  fileSavingDir + "/" + newFileName
  

def runSaving( configs, screenShotPath ):

    global sizeOld;    
    
    makeScreenShot( screenShotPath )
    
    sizeNew = os.path.getsize( screenShotPath ) 
        
    if ( sizeNew != sizeOld ):        
        sizeOld = sizeNew
        moveToSave( configs, screenShotPath )
    else:
        os.remove( screenShotPath )
                 

def runUploadingAndSaving( configs ):
    screenShotPath = configs['SCREENSHOT_PATH'];
        
    stop = False
    start_uploading = time.time()
    
    while ( stop == False ):
        start_saving = time.time()  
        runSaving( configs, screenShotPath )
        finish_saving = time.time()
            
        timeOut =  int( configs['SCREENSHOT_SAVING_TIMEOUT'] ) - (finish_saving - start_saving)
        
        if( timeOut > 0.1 ):
            time.sleep( timeOut )
                
        finish_uploading = time.time();
            
        timeOut =  int( configs['SCREENSHOT_UPLOADING_TIMEOUT'] ) - (finish_uploading - start_uploading)
        
        if( timeOut < 0.1 ):
            stop = True
        
    global fileForUploading
    uploadScreenshot( fileForUploading, configs ) 
                
                
###############################################################################    
         
initFilePath = '/etc/terminal/osago.ini'

configs = config.readConfigFile( initFilePath )

if ( configs['IS_SCREENSHOT_ENABLED'].lower() == 'true' ):
    while True:
        runUploadingAndSaving( configs )
    
    
    
    
    

