import bpy,json,hashlib
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
s=bpy.context.scene;bpy.context.view_layer.update();B=Path('/Users/USER/Documents/Codex/2026-09-11/new-chat/outputs/pocket-rove-studio-hifi')
screen=bpy.data.objects['SCREEN / replace original image'];phone=bpy.data.objects['PHONE / precision rounded titanium chassis'];support=bpy.data.objects['TYPE / support']
imgs=[i for i in bpy.data.images if i.type=='IMAGE']
assert len(imgs)==1 and imgs[0].packed_file and tuple(imgs[0].size)==(1206,2622)
assert (s.render.resolution_x,s.render.resolution_y,s.render.resolution_percentage)==(2160,3840,100)
assert s.cycles.samples==256 and s.camera.data.lens==95
screen_top=max(world_to_camera_view(s,s.camera,[REDACTED_EMAIL]).y for v in screen.data.vertices)
from mathutils import Vector
support_bottom=min(world_to_camera_view(s,s.camera,support.matrix_world@Vector(c)).y for c in support.bound_box)
assert screen_top < support_bottom, (screen_top,support_bottom)
lowest=min(([REDACTED_EMAIL]).z for v in phone.data.vertices)
assert abs(lowest-.802)<.002
src=Path('/Volumes/EXTERNAL/app/EarthOnlineGuide/Marketing/PocketRove-UI-1.6.3-b1-20260909/04-souvenirs-original.png');copy=B/'assets/screen-souvenirs-1.6.3.png'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(src)==sha(copy)
r={'scene_readback':'PASS','resolution':[2160,3840],'render_engine':s.render.engine,'device_setting':s.cycles.device,'samples_limit':s.cycles.samples,'camera_lens_mm':s.camera.data.lens,'screenshot_packed':True,'screenshot_unchanged_sha256':sha(copy),'screen_title_gap_pixels':round((support_bottom-screen_top)*3840,2),'phone_lowest_z':lowest,'podium_top_z':.80,'user_visual_acceptance':'PENDING'}
(B/'verification.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
