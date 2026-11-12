import bpy,json
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
from pathlib import Path
s=bpy.context.scene;bpy.context.view_layer.update();items={}
for o in s.objects:
    if o.type=='FONT':
        pts=[world_to_camera_view(s,s.camera,o.matrix_world@Vector(v)) for v in o.bound_box]
        b=[min(v.x for v in pts),min(v.y for v in pts),max(v.x for v in pts),max(v.y for v in pts)];assert b[0]>=0 and b[1]>=0 and b[2]<=1 and b[3]<=1,(o.name,b);items[o.name]=b
screen=bpy.data.objects['SCREEN / replace original image'];top=max(world_to_camera_view(s,s.camera,[REDACTED_EMAIL]).y for v in screen.data.vertices)
assert top<items['TYPE / support'][1]
r={'scene_readback':'PASS','text_in_frame':'PASS','screen_support_gap_pixels':round((items['TYPE / support'][1]-top)*3840,1),'screen_provenance':s['Screen provenance'],'user_visual_acceptance':'PENDING'}
Path('/Users/USER/Documents/Codex/2026-09-11/new-chat/outputs/pocket-rove-studio-welcome/verification.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
