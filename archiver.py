import sys, os
import time

import pic_rescaler, vid_reencoder


def print_error(msg):
    print('{}: {}'.format(sys.argv[0], msg))

def to_time_str(t):
    t = int(t)
    res = ''

    h = t//60//60
    if h != 0:
        res += str(h) + 'h '
        t -= h*60*60

    m = t//60
    if m != 0:
        res += str(m) + 'm '
        t -= m*60

    if t != 0:
        res += str(t) + 's'

    return res


class Archiver:
    def __init__(self):
        self.target_folder = None
        self.rescale_pictures = False
        self.reencode_videos = False
        self.create_tarball = False

    def start(self):
        t_start = time.time()
        if not (self.rescale_pictures or self.reencode_videos or self.create_tarball):
            print_error('nothing to do, quitting')
            sys.exit(0)
        if self.target_folder is None or not os.path.exists(self.target_folder):
            print_error('cannot access target folder: ' + self.target_folder)
            sys.exit(-1)

        if self.rescale_pictures:
            print('[*] Rescaling pictures...')
            pic_rescaler.rescale_pictures(self.target_folder)
        if self.reencode_videos:
            print('[*] Re-encoding videos...')
            vid_reencoder.reencode_videos(self.target_folder)
        if self.create_tarball:
            print('[*] Archiving and compressing content...')
            self._create_tar()

        print('\nDone. Total time: {}'.format(to_time_str(time.time() - t_start)))

    def _create_tar(self):
        print_error('_create_tar not implemented')
        sys.exit(-1)
