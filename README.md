# Archiver
Archiver is a very basic tool I built to help me manage my media backups.

## What it does
In essence, it compresses different types of media files with different methods based on their type. I am not a person who loves huge Ultra-HD videos weighing several GBs for just a couple of minutes of content, or photos shot with a DSLR that are 10+ Mb in size when a 1 Mb picture does just fine for me.

So this is it, when invoking this program with a target folder, it rescales all pictures to a 2048px definition, and all videos are re-encoded with a HEVC/MP2 codec and scaled down to standard HD dimensions.

## Result
Overall, I found directory sizes to literally halve in size, if not more. One extreme example is a folder of MP4 (h264) videos that weighed 4.2 Gb, for which I would have to have used an entire DVD just to backup this folder alone. After re-encoding (which to be honest took a couple of hours...), the total size went down to **672 Mb**, and the visual quality was the very same as the original files.

## How to use

##### Requirements
- Python 3
- FFMpeg
- ImageMagick

##### Installation
So far, I haven't yet created an installable package, so what you can do is clone or download the repository and create an alias to the `main.py` file in your `.bashrc`.

```shell
alias archive='python3 ~/Downloads/archiver/main.py'
```

##### Usage
From the built-in help:
```
Media archiver version 1.0
Copyright Alex Sartori

Usage: archive [OPTIONS] FOLDER

Options:
   -h, --help .............. Show this message
   -p, --pictures .......... Rescale pictures
   -v, --videos ............ Re-encode videos
   -t, --tarball ........... Create a .xz tarball

Picture rescaling:
  Pictures are rescaled so that their largest dimension is 2048px,
  and are reinterlaced as "plane". If their resolution is already
  smaller than 2048px, they are only reainterlaced.

Video re-encoding:
  Videos are converted to the MP4 format using HEVC (h265) for the
  video track and MP2 for the audio stream. Their size, if greater
  than 1280x720, is reduced to those dimensions (while keeping the
  original aspect ratio).

Tarball archiving: (NOT implemented yet)
  All files contained in the target folder will be compressed
  into a .tar.xz archive using the LZMA2 compression filter.
```

For example, `archive -p Summer_2018/` will only rescale pictures in the folder but not touch your videos.
