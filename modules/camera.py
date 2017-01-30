import picamera
import threading
import time
import subprocess
from rx import Observer

from modules import logger
from modules import utils

import config
import parameters


class CameraObserver(Observer):
    def __init__(self):
        camera = picamera.PiCamera()
        camera.vflip = True
        camera.hflip = True
        camera.led = False
        camera.rotation = parameters.camera_rotation
        self.camera = camera

    def upload_to_drive(self, picture_path):
        logger.logger.info('UPLOADING TO DRIVE...     ' + picture_path)
        bash_command = 'drive -c ' + config.gdrive_config_path + ' upload -p ' + config.drive_folder_id + ' -f ' + \
                       picture_path + ' 1>/dev/null && rm ' + picture_path
        process = subprocess.Popen(bash_command, shell=True)
        output = process.communicate()[0]
        logger.logger.info('DRIVE UPLOAD!             ' + picture_path)
        pass

    def on_next(self, x):
        logger.logger.info('CAMERA CAPTURE!')
        picture_path = config.tmp_data_path + '/' + utils.get_time() + '_' + str(time.time()) + '.jpg'
        self.camera.capture(picture_path)
        # TODO: is this thread useful. Maybe a simple function call is enough.
        new_upload_thread = threading.Thread(target=self.upload_to_drive, args=[picture_path])
        new_upload_thread.start()

    def on_error(self, error):
        pass

    def on_completed(self):
        pass
