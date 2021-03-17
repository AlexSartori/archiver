import os, time
import subprocess

EXTENSIONS = ['.jpg', '.jpeg', '.png']

def rescale_pictures(folder):
    pics = os.listdir(folder)
    progress = 0

    for p in pics:
        p = os.path.join(folder, p)
        progress += 1
        bar_50 = int(50*progress/len(pics))
        print('  {:5.1f}% [{}{}]'.format(100*progress/len(pics), '#'*bar_50, ' '*(50-bar_50)), end='\r')

        fname, fext = os.path.splitext(p)
        if not os.path.isfile(p):
            continue
        if fext.lower() not in EXTENSIONS:
            continue

        cmd = ['convert', p, '-resize', '2048x2048>', '-interlace', 'plane', p]
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        ret = proc.wait()
        if ret != 0:
            print("\nError in subprocess for file:", p)
            for l in proc.stderr.read().decode('utf-8')[:-1].split('\n'):
                print(' ! ', l)
    print('')
