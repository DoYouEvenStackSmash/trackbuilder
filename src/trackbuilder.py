#!/usr/bin/python3
import numpy as np
from PIL import Image, ImageDraw
import collections
from aux_functions import *
# from Dataloader import Dataloader
from YoloBox import YoloBox
from ObjectTrackManager import ObjectTrackManager
from ObjectTrack import ObjectTrack
from AnnotationLoader import AnnotationLoader as al
import sys
import os
import json

CUTOFF = 0
# loader
LOAD_CUTOFF = 1

#builder
def file_list_loader(valid_filename, sys_path="."):
  '''
  Load a list of files and paths:
    sys/path/foo.000.jpg
    sys/path/foo.001.jpg
    sys/path/foo.002.jpg
  
  Returns a list of files,paths
  '''
  fl = al.load_annotation_file_list(valid_filename)
  # sys_path = sys.argv[2]

  # sort the files to be in frame order
  sortkey = lambda s: int(s.split(".")[1])
  fl = sorted(fl, key=sortkey)
  
  # separate each file into path and filename
  files = []
  sys_paths = []
  for i in range(len(fl)):
    filename = fl[i].split('/')[-1]
    # sys_path = fl[i][:-1 * len(filename)]
    files.append(filename)
    sys_paths.append(sys_path)
  
  return files,sys_paths


def json_loader(filename, sys_path):
  '''
  LOADER
  legacy json loader
  Takes a filename and sys_path, opens a json file
  
  Returns a python dict
  '''
  an_json = al.load_annotations_from_json_file(filename,sys_path)
  if len(an_json) == 0:
    print("failed to load tracks")
    return None
  return an_json, sys_path


def load_layers(files, sys_paths, construct = False):
  '''
  BUILDER
  For each file, load all bounding boxes into a layer
  
  Returns an array of layers, 
  '''
  layer_list = []
  for i in range(len(files)):
    layer_list.append(al.load_yolofmt_layer(files[i], sys_paths[i]))
  return layer_list


def import_tracks(an_json, sys_path="."):
  '''
  LOADER
  Wrapper function for loading a json file into a newly created ObjectTrackManager
  
  Returns an ObjectTrackManager
  '''
  otm = ObjectTrackManager()
  otm.import_loco_fmt(an_json,sys_path)
  return otm


def build_tracks(files,sys_paths,layer_list):
  '''
  Builder
  Wrapper function for constructing tracks from layers.
    Note: Files and syspaths metadata are not necessary in this step.

  Returns a newly created ObjectTrackManager containing tracks through layer_list
  '''
  otm = ObjectTrackManager(filenames=files,sys_paths=sys_paths,layers=layer_list)
  otm.initialize_tracks()
  otm.process_all_layers()
  return otm


def freeze_tracks(otm):
  '''
  BUILDER, LOADER
  Wrapper function for the "irreversible" process of ossifying tracks as doubly linked lists.
  
  Does not return anything
  '''
  otm.close_all_tracks()
  otm.link_all_tracks(CUTOFF)
  # return otm

def export_tracks(otm,filehandle=None):
  '''
  BUILDER, LOADER
  Wrapper function for exporting the contents of ObjectTrackManager in LOCO format.
  
  Writes output to a file handle or stdout
  Does not return anything
  '''
  coco_s = otm.export_loco_fmt()
  if filehandle == None:
    f = open("out.json","w")
    f.write(json.dumps(coco_s,indent=2))
    f.close()
  else:
    filehandle.write(json.dumps(coco_s,indent=2))


#track builder
def build_annotations(afl,sys_path,outfile=None):
  '''
  BUILDER
  Builds a list of tracks 
  sys.argv[1]: annotation file list
  sys.argv[2]: image sys_path
  sys.argv[3]: output file
  '''
  f,s = file_list_loader(sys.argv[1],sys.argv[2])
  ll = load_layers(f,s)
  o = build_tracks(f,s,ll)
  freeze_tracks(o)
  # Export
  if outfile == None:
    export_tracks(o,sys.stdout)
  elif outfile != infile:
    f = open(outfile,"w")
    export_tracks(o,f)
    f.close()
  else:
    print(f"danger of overwriting {infile}\naborting...")
  

def reload_annotations(infile, outfile=None):
  '''
  LOADER
  Reloads and corrects a json annotation file
  Does not return
  '''
  s = al.load_annotations_from_json_file(infile)
  o = import_tracks(s)
  freeze_tracks(o)
  # export
  if outfile == None:
    export_tracks(o,sys.stdout)
  elif outfile != infile:
    f = open(outfile,"w")
    export_tracks(o,f)
    f.close()
  else:
    print(f"danger of overwriting {infile}\naborting...")


def draw_annotations(infile, sys_path):
  '''
  DRAW
  Loads annotations from LOCO json and draws them on their image files
  Does not return
  '''
  s = al.load_annotations_from_json_file(infile)
  o = import_tracks(s,sys_path)
  freeze_tracks(o)
  # "export"
  o.draw_ybbox_data_on_images()

def main():
  '''
  CLI but not with argparse
  '''
  print(sys.argv)
  command = sys.argv[1]
  outfile = None
  
  match command:
    case 'reload':  # reload annotations file
      if len(sys.argv) == 4:
        reload_annotations(sys.argv[2], sys.argv[3])
      else:
        reload_annotations(sys.argv[2])
      
    case 'build': # build tracks from scratch
      if len(sys.argv) == 5:
        build_annotations(sys.argv[2],sys.argv[3],sys.argv[4])
      else:
        build_annotations(sys.argv[2],sys.argv[3])
      
    case 'draw':
      if len(sys.argv) != 4:
        print("must specify draw [input_file] [path_to_images]")
      else:
        draw_annotations(sys.argv[2],sys.argv[3])

    case other:
      print("unknown")
main()