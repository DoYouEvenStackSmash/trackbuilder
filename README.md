# trackbuilder
## Overview
Trackbuilder is a form of tracking-by-detection for use on video findings, ingesting results from an object detector and outputting object tracks formatted as COCO-compliant JSON. 
## Usage

### Build
```
./trackbuilder.py build filelist.txt
```
### Draw
### Reload

```
./trackbuilder.py reload infile.json [final.json]
``` 
This is how tracks are modified by the user without needing to rebuild. `track_id` fiels of LOCO json is set to -1, and the `reload` mechanism removes all annotations which reference that track. <br>
For failsafe reasons, overwriting a file of the same name with reload is not permitted. (For those who would prefer streamlined workflow, this behavior can be patched in `trackbuilder.py` in the ``reload`` function.)


### Input format
### Output format

## ObjectTracks

## Linking tracks

[![See the video](https://img.youtube.com/vi/ZEZ0h9iTSXU/maxresdefault.jpg)](https://youtu.be/ZEZ0h9iTSXU)