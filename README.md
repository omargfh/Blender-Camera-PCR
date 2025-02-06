Python script to mimic the Blender BPY API for JSON
export. The name is a play on the Blender DNA/RNA naming
convention. This script is intended to be used with
https://extensions.blender.org/add-ons/export-camera-animation/
as a dummy module to allow the Blender JSON export to work.

Example:
```py
import bpyPCR as bpy

# ... your Blender JSON export code here ...

bpy.dump("Camera", "camera.json")
# OR
bpy.dump_index_on_frame("Camera", "camera.json")
```
