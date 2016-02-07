
import subprocess
import multiprocessing
import time
import datetime
import os

import photos
import config


def executeCommand( command ):
    print( command )
    subprocess.call( command, shell=True, stderr=subprocess.STDOUT)

def createAndInitVirtualDevices( configs ):
    command = "modprobe v4l2loopback devices=3"
    executeCommand( command )
    
    command = "nohup ffmpeg -f video4linux2 -s {0}x{1} -i {2} -codec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 {3} -codec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 {4} >/dev/null 2>/nohup.err &".format(
            configs['INPUT_WIDTH'],
            configs['INPUT_HEIGHT'],
            configs['ORIGINAL_INPUT_DEVICE'],
            configs['PHOTO_INPUT_DEVICE'],
            configs['VIDEO_INPUT_DEVICE'])
    executeCommand( command )
    
    
def startRecord( configs, videoPath ):
    command = "ffmpeg -y -f v4l2 -framerate 30 -t {0} -video_size {1}x{2} -i {3} -s {4}x{5} -b:v 1000 {6}".format(
            configs['VIDEO_RECORD_TIME'],
            configs['INPUT_WIDTH'],
            configs['INPUT_HEIGHT'],
            configs['VIDEO_INPUT_DEVICE'],
            configs['VIDEO_OUTPUT_WIDTH'],
            configs['VIDEO_OUTPUT_HEIGHT'],
            videoPath)
 #   command = "nohup ffmpeg -y -f v4l2 -framerate 30 -t "+configs['VIDEO_RECORD_TIME']+" -video_size "+configs['INPUT_WIDTH']+"x"+configs['INPUT_HEIGHT']+" -i "+configs['VIDEO_INPUT_DEVICE']+" -s "+configs['VID$

    #print(command)    
    executeCommand( command )

def canRecord( configs, videoFilePath ):

    if(os.path.isfile( videoFilePath )):
        if( time.time() - os.path.getctime( videoFilePath ) > float( configs['VIDEO_RECORD_TIME'] )):
            return True
        else:
            return False;
    else:
        return True

def runVideoLoop( configs ):
    #executeCommand("echo " + configs['VIDEO_RECORD_TIME'])
    if( configs['IS_VIDEO_ENABLED'].lower() == 'true'):
        while True:
            videoFilePath = configs['VIDEO_PATH'] + datetime.datetime.today().strftime('%y-%m-%d_%H') + '.mkv'
            can = canRecord( configs, videoFilePath )

            if can == True:
                startRecord( configs, videoFilePath )
                time.sleep( 1 )
            else:
                time.sleep( float( configs['VIDEO_RECORD_TIME'] ) - (time.time() - os.path.getctime( videoFilePath )) )

###############################################################################
    
    
initFilePath = '/etc/terminal/osago.ini'

configs = config.readConfigFile( initFilePath )

createAndInitVirtualDevices( configs )

#executeCommand("echo "+configs['PHOTO_INPUT_DEVICE'])
#xecuteCommand("echo "+configs['VIDEO_INPUT_DEVICE'])
p1 = multiprocessing.Process(target=photos.runPhotosLoop,kwargs={'configs':configs})
p2 = multiprocessing.Process(target=runVideoLoop,kwargs={'configs':configs})

p1.start()
p2.start()

p1.join()
p2.join()
