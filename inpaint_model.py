import os
import sys
import subprocess
import shlex
import pexpect

import cv2
import numpy as np

from pathlib import Path
from shutil import copyfile

def invoke_process(command):
    thread = pexpect.spawn(command, encoding='utf-8')
    thread.logfile = sys.stdout
    print("started %s" % command)
    cpl = thread.compile_pattern_list([pexpect.EOF])
    while True:
        i = thread.expect_list(cpl, timeout=None)
        if i == 0: # EOF
            print("the sub process exited")
            break
    thread.close()

def invoke_process2(command, shellType=False, stdoutType=subprocess.PIPE):
    """runs subprocess with Popen/poll so that live stdout is shown"""
    try:
        process = subprocess.Popen(
            shlex.split(command), shell=shellType, stdout=stdoutType,
            universal_newlines=True)
    except:
        print("ERROR {} while running {}".format(sys.exc_info()[1], command))
        return None
    while True:
        output = process.stdout.readline()
        # used to check for empty output in Python2, but seems
        # to work with just poll in 2.7.12 and 3.5.2
        # if output == '' and process.poll() is not None:
        if process.poll() is not None:
            break
        if output:
            print(output.strip().decode())
    rc = process.poll()
    return rc

class PhotoInpaintModel():
    def __init__(self):
        pass

    def resize_crop(self, image, resize=1):
        if resize == 0 or resize == 1:
            return image

        h, w, c = np.shape(image)
        max_size = min(h, w) * resize // 1
        if min(h, w) > max_size:
            if h > w:
                h, w = int(max_size*h/w), max_size
            else:
                h, w = max_size, int(max_size*w/h)
        h, w = int((h//8)*8), int((w//8)*8)
        image = cv2.resize(image, (w, h),
                           interpolation=cv2.INTER_AREA)
        image = image[:h, :w, :]
        return image

    def paint(self, input_image, opts):
        print('Paint, start.')

        homepath = os.getcwd()
        tmp_path = homepath+'/tmp'
        argfile_path = tmp_path+'/argument.yml'
        imgfile_path = tmp_path+'/images'
        videofile_path = tmp_path+'/videos'
        Path(tmp_path).mkdir(parents=True, exist_ok=True)
        Path(imgfile_path).mkdir(parents=True, exist_ok=True)
        Path(videofile_path).mkdir(parents=True, exist_ok=True)

        copyfile(homepath+'/argument_template.yml', argfile_path)

        # process image
        image = cv2.cvtColor(np.array(input_image), cv2.COLOR_RGB2BGR)
        image = self.resize_crop(image, resize=opts['resize'])
        print('resized')
        # batch_image = image.astype(np.float32)/127.5 - 1
        # batch_image = np.expand_dims(batch_image, axis=0)
        src_path = imgfile_path+'/source.jpg'
        cv2.imwrite(src_path, image)

        # args
        fps = opts['fps']
        num_frames = opts['num_frames']
        x_shift = opts['x_shift']
        y_shift = opts['y_shift']
        z_shift = opts['z_shift']
        traj_type = opts['traj_type']
        effect_type = opts['effect_type']
        img_h, img_w, img_c = np.shape(image)
        longer_side_len = max(img_h, img_w)

        # write argument.yml
        with open(argfile_path, 'a') as myfile:
            myfile.write(f"x_shift_range: [{x_shift}]\n")
            myfile.write(f"y_shift_range: [{y_shift}]\n")
            myfile.write(f"z_shift_range: [{z_shift}]\n")
            myfile.write(f"traj_types: ['{traj_type}']\n")
            myfile.write(f"video_postfix: ['{effect_type}']\n")

            myfile.write(f"fps: {fps}\n")
            myfile.write(f"num_frames: {num_frames}\n")

            myfile.write(f"longer_side_len: {longer_side_len}\n")

            myfile.write(f"src_folder: {imgfile_path}\n")
            myfile.write(f"video_folder: {videofile_path}\n")
            myfile.write(f"depth_folder: {tmp_path}/depth\n")
            myfile.write(f"mesh_folder: {tmp_path}/mesh\n")

            if opts['reuse']:
                myfile.write("depth_format: '.png'\nrequire_midas: False\n")
            else:
                myfile.write("depth_format: '.npy'\nrequire_midas: True\n")


        # output = self.session.run(self.final_out, feed_dict={self.input_photo: batch_image})
        # output = (np.squeeze(output)+1)*127.5
        # output = np.clip(output, 0, 255).astype(np.uint8)

        os.chdir(homepath + '/PhotoInpainting')
        print("Working dir: " + os.getcwd())

        invoke_process('python main.py --config ' + argfile_path)

        os.chdir(homepath)
        return cv2.cvtColor(cv2.imread(src_path), cv2.COLOR_BGR2RGB)
