import os, time
import subprocess

EXTENSIONS = ['.mp4', '.m4a', '.avi', '.3gp', '.mov', '.mkv']

def reencode_videos(folder):
    videos = os.listdir(folder)
    progress = 0

    for v in videos:
        v = os.path.join(folder, v)
        progress += 1
        bar_50 = int(50*progress/len(videos))
        print('  {:5.1f}% [{}{}]'.format(100*progress/len(videos), '#'*bar_50, ' '*(50-bar_50)), end='\r')

        fname, fext = os.path.splitext(v)
        if not os.path.isfile(v):
            continue
        if fext.lower() not in EXTENSIONS:
            continue

        cmd = [
            'ffmpeg', '-i', v, '-y',
            '-c:v', 'libx265', '-c:a', 'mp2', '-preset', 'fast',
            '-vf', 'scale=\'min(iw,1280)\':-2',
            fname + '_h265.mp4'
        ]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ret = proc.wait()
        if ret == 0:
            os.unlink(v)
        else:
            print("\nError in subprocess for file:", v)
            for l in proc.stderr.read().decode('utf-8')[:-1].split('\n'):
                print(' ! ', l)
    print('')
