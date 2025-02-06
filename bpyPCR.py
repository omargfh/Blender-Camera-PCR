#!/usr/bin/env python3
"""
Python script to mimic the Blender BPY API for JSON
export. The name is a play on the Blender DNA/RNA naming
convention. This script is intended to be used with
https://extensions.blender.org/add-ons/export-camera-animation/
as a dummy module to allow the Blender JSON export to work.

Example:
import bpyPCR as bpy

# ... your Blender JSON export code here ...

bpy.dump("Camera", "camera.json")
# OR
bpy.dump_index_on_frame("Camera", "camera.json")
"""

import json

# --- Begin PCR bpy definitions ---

class PCRDOF:
    def __init__(self):
        self.focus_distance = None

# Impl_ indicates that this is a class that
# is not meant to be part of the Blender API.
class Impl_PCRKeyframeCollection:
		def __init__(self):
				self.keyframes = {}
				self.frame_data = {} # index by frame

		def keyframe_insert(self, property_name):
				frame = bpy.context.scene.current_frame
				value = getattr(self, property_name, None)
				if property_name not in self.keyframes:
						self.keyframes[property_name] = []
				self.keyframes[property_name].append({"frame": frame, "value": value})
				if frame not in self.frame_data:
						self.frame_data[frame] = {}
				self.frame_data[frame][property_name] = value

class PCRCameraData(Impl_PCRKeyframeCollection):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.lens = None
        self.shift_x = None
        self.shift_y = None
        self.dof = PCRDOF()
        self.clip_start = None
        self.clip_end = None
        self.display_size = None

class PCRObject(Impl_PCRKeyframeCollection):
    def __init__(self, name, data):
        super().__init__()
        self.name = name
        self.data = data
        self.location = None
        self.scale = None
        self.rotation_euler = None
        self.hide_render = None

class PCRCameras:
    def __init__(self):
        self.items = {}

    def new(self, name):
        cam = PCRCameraData(name)
        self.items[name] = cam
        return cam

class PCRObjects:
    def __init__(self):
        self.items = {}

    def new(self, name, data):
        obj = PCRObject(name, data)
        self.items[name] = obj
        return obj

class PCRData:
    def __init__(self):
        self.cameras = PCRCameras()
        self.objects = PCRObjects()

class PCRCollectionObject:
  def __init__(self):
    self.objects = []

  def link(self, obj):
      self.objects.append(obj)

class PCRCollection:
    def __init__(self):
        self.objects = PCRCollectionObject()

class PCRScene:
    def __init__(self):
        # Set an initial frame (simulate Blender’s current frame)
        self.frame_current = 1
        self.current_frame = self.frame_current

    def frame_set(self, frame):
        self.current_frame = frame

class PCRContext:
    def __init__(self):
        self.scene = PCRScene()
        self.collection = PCRCollection()

# Our PCR bpy “module” that mimics just enough of Blender’s API.
class PCR:
    def __init__(self):
        self.context = PCRContext()
        self.data = PCRData()

    """
		Export the camera data to a JSON file.
		:param camera_name: The name of the camera to export.
		:param filename: The name of the file to write.
		:return: None

		:output: Exports the camera data to a JSON file.
  	"""
    def dump(self, camera_name, filename="camera.json"):
      camera_obj = self.data.objects.items[camera_name]
      outfile = open(filename, "w")
      return json.dump({
				"camera": {
						"name": camera_obj.name,
						"data": {
								"lens": camera_obj.data.lens,
								"shift_x": camera_obj.data.shift_x,
								"shift_y": camera_obj.data.shift_y,
								"dof": {"focus_distance": camera_obj.data.dof.focus_distance},
								"clip_start": camera_obj.data.clip_start,
								"clip_end": camera_obj.data.clip_end,
								"display_size": camera_obj.data.display_size,
								"keyframes": camera_obj.data.keyframes
						},
						"object": {
								"hide_render": camera_obj.hide_render,
								"keyframes": camera_obj.keyframes
						}
				}
    }, outfile, indent=2)

    def dump_index_on_frame(self, camera_name, filename="camera.json"):
      camera_obj = self.data.objects.items[camera_name]
      outfile = open(filename, "w")
      return json.dump({
					"camera": {
							"name": camera_obj.name,
							"data": {
									"lens": camera_obj.data.lens,
									"shift_x": camera_obj.data.shift_x,
									"shift_y": camera_obj.data.shift_y,
									"dof": {"focus_distance": camera_obj.data.dof.focus_distance},
									"clip_start": camera_obj.data.clip_start,
									"clip_end": camera_obj.data.clip_end,
									"display_size": camera_obj.data.display_size,
									"keyframes": camera_obj.data.frame_data
							},
							"object": {
									"hide_render": camera_obj.hide_render,
									"keyframes": camera_obj.frame_data
							}
					}
			}, outfile, indent=2)

bpy = PCR()