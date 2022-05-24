#!/usr/bin/python3
import getopt, sys
from archiver import Archiver


def print_header():
    print('Media archiver version 1.1')
    print('Copyright Alex Sartori')
    print('')

def print_help():
    print('Usage: archive [OPTIONS] FOLDER')
    print('')
    print('Options:')
    print('   -h, --help .............. Show this message')
    print('   -p, --pictures .......... Rescale pictures')
    print('   -v, --videos ............ Re-encode videos')
    print('   -t, --tarball ........... Create a .xz tarball')
    print('')
    print('Picture rescaling:')
    print('  Pictures are rescaled so that their largest dimension is 2048px,')
    print('  and are reinterlaced as "plane". If their resolution is already')
    print('  smaller than 2048px, they are only reainterlaced.')
    print('')
    print('Video re-encoding:')
    print('  Videos are converted to the MP4 format using HEVC (h265) for the')
    print('  video track and MP2 for the audio stream. Their size, if greater')
    print('  than 1280x720, is reduced to those dimensions (while keeping the')
    print('  original aspect ratio).')
    print('')
    print('Tarball archiving: (NOT implemented yet)')
    print('  All files contained in the target folder will be compressed')
    print('  into a .tar.xz archive using the LZMA2 compression filter.')
    print('')


def print_error(msg):
    print('archive: ' + str(msg))
    print('Use "archive --help" for info on the usage')

if __name__ == '__main__':
    print_header()
    archiver = Archiver()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hpvt", ["help", "pictures", "videos", "tarball"])
    except getopt.GetoptError as err:
        print_error(err)
        sys.exit(2)

    for o, v in opts:
        if o in ('-h', '--help'):
            print_help()
            sys.exit(0)
        elif o in ('-p', '--pictures'):
            archiver.rescale_pictures = True
        elif o in ('-v', '--videos'):
            archiver.reencode_videos = True
        elif o in ('t', '--tarball'):
            archiver.create_tarball = True
        else:
            print_error('unknown option, ignoring: ' + o + ' ' + v)

    if len(args) == 0:
        print_error('no target folder specified')
    elif len(args) == 1:
        archiver.target_folder = args[0]
    else:
        archiver.target_folder = ' '.join(args)

    archiver.start()
