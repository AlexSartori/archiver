import os, time
import subprocess
from threading import Thread, Lock
from time import sleep


EXTENSIONS = ['.mp4', '.m4a', '.avi', '.3gp', '.mov', '.mkv']
workload = []
workload_mutex = Lock()


def thread_worker():
    while len(workload) > 0:
        workload_mutex.acquire()
        fname, fext = workload.pop()
        vid_path = fname + fext
        workload_mutex.release()

        cmd = [
            'ffmpeg', '-i', vid_path, '-y',
            '-loglevel', 'warning',
            '-c:v', 'libx265', '-c:a', 'mp3', '-preset', 'fast',
            '-vf', 'scale=\'min(iw,1280)\':-2',
            fname + '_h265.mp4'
        ]

        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        ret = proc.wait()

        if ret == 0:
            os.unlink(vid_path)
            proc.stderr.read() # Empy buffer
        else:
            print("\nError in subprocess for file:", vid_path)
            for l in proc.stderr.read().decode('utf-8')[:-1].split('\n'):
                print(' ! ', l)


def reencode_videos(folder, n_threads=2):
    for v in os.listdir(folder):
        v = os.path.join(folder, v)

        fname, fext = os.path.splitext(v)
        if not os.path.isfile(v):
            continue
        if fext.lower() not in EXTENSIONS:
            continue

        workload.append((fname, fext))

    tot = len(workload)
    threads = []
    for t in range(n_threads):
        threads.append(
            Thread(target=thread_worker)
        )
        threads[-1].start()

    progess = tot
    while 1:
        workload_mutex.acquire()
        progress = tot - len(workload)
        workload_mutex.release()

        bar_50 = int(50*progress/tot)
        print('  {:5.1f}% [{}{}]'.format(100*progress/tot, '#'*bar_50, ' '*(50-bar_50)), end='\r')

        if progress == tot:
            break
        else:
            sleep(1)

    for t in threads:
        t.join()

    print('')
