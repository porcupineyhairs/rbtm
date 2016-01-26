import os
from threading import Thread

import h5py

import numpy as np
import scipy.ndimage
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from storage import app

logger = app.logger


def extract_frame(frame_id, experiment_id):
    frames_file_path = os.path.join('data', 'experiments', str(experiment_id), 'before_processing', 'frames.h5')
    with h5py.File(frames_file_path, 'r') as frames_file:
        frame = frames_file[str(frame_id)]
    logger.info('hdf5 file: extract frame {} of experiment {} successfully'.format(frame_id, experiment_id))
    return frame


def add_frame(frame, frame_id, experiment_id):
    frames_file_path = os.path.join('data', 'experiments', str(experiment_id), 'before_processing', 'frames.h5')
    with h5py.File(frames_file_path, 'r+') as frames_file:
        frames_file.create_dataset(str(frame_id), data=frame, compression="gzip", compression_opts=1)
    logger.info('hdf5 file: add frame {} to experiment {} successfully'.format(frame_id, experiment_id))

    png_file_path = os.path.join('data', 'experiments', str(experiment_id), 'before_processing', 'png',
                                 str(frame_id) + '.png')
    # make_png(frame, png_file_path)
    Thread(target=make_png, args=(frame, png_file_path)).start()
    logger.info('png: start making png from frame {} of experiment {}'.format(frame_id, experiment_id))


def delete_frame(frame_id, experiment_id):
    frames_file_path = os.path.join('data', 'experiments', str(experiment_id), 'before_processing', 'frames.h5')
    with h5py.File(frames_file_path, 'r+') as frames_file:
        del frames_file[str(frame_id)]
    logger.info(
        'hdf5 file: frame {} was deleted from experiment {} successfully'.format(str(frame_id), str(experiment_id)))


def make_png(res, frame_path):
    logger.info('Going to make png...')
    # small_res = scipy.ndimage.zoom(np.rot90(res), zoom=0.25, order=2)
    # plt.imsave(frame_path, small_res, cmap=plt.cm.gray)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    enhanced_image = scipy.ndimage.filters.median_filter(np.rot90(res), size=3)
    im = ax.imshow(enhanced_image, cmap=plt.cm.gray) # vmin, vmax 
    fig.colorbar(im)
    fig.savefig(frame_path)
    plt.close(fig)
    logger.info('png was made')
