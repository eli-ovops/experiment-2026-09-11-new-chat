"""Render the included studio using the byte-identical native Today screenshot.
Run with the delivered .blend or the earlier high-fidelity .blend loaded.
"""
import bpy,hashlib,json
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parent;s=bpy.context.scene
src=B/'assets/today-native-1.6.9-debug.png'
expected='21788cba5245d011fc3eb464c920410f725c01a94e1c534032052b45f513c861'
assert hashlib.sha256(src.read_bytes()).hexdigest()==expected
im=bpy.data.images.load(str(src));assert tuple(im.size)==(1206,2622);im.pack()
o=bpy.data.objects.get('SCREEN / native Today PNG') or bpy.data.objects['SCREEN / replace original image'];o.name='SCREEN / native Today PNG'
for m in o.data.materials:
    m.name='SCREEN / native PNG unaltered color';n=m.node_tree.nodes;l=m.node_tree.links
    tex=next(x for x in n if x.type=='TEX_IMAGE');tex.image=im
    em=next(x for x in n if x.type=='EMISSION');out=next(x for x in n if x.type=='OUTPUT_MATERIAL');em.inputs['Strength'].default_value=1;l.new(em.outputs[0],out.inputs[0])
for poly in o.data.polygons:
    for li in poly.loop_indices:
        co=o.data.vertices[o.data.loops[li].vertex_index].co;o.data.uv_layers.active.data[li].uv=(co.x/3+.5,co.y/(3*2622/1206)+.5)
head=bpy.data.objects['TYPE / headline'];head.data.body='A little more\ncuriosity, every day.'
H=20*max(abs(v.y/v.z) for v in s.camera.data.view_frame(scene=s));head.data.size=H*.054
bpy.data.objects['TYPE / collection index'].data.body='YOUR DAILY ADVENTURE'
bpy.data.objects['TYPE / support'].data.body='Three daily prompts. One small start.'
s['Screen provenance']='Native Pocket Rove 1.6.9(1) Debug Simulator screenshot captured 2026-09-10 09:10:53. EARTH_GUIDE_SKY_CAPTURE demo: sky task revealed, not completed. Not release UI or natural random task state.'
s['Screen SHA256']=expected
s['Usage']='The source PNG is unchanged; no image generation, repainting, retouching, or UI reconstruction is used in this Today version.'
s.render.resolution_x=2160;s.render.resolution_y=3840;s.render.resolution_percentage=100;s.cycles.samples=256;s.cycles.use_denoising=True
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
for d in p.devices:d.use=d.type=='METAL'
s.cycles.device='GPU'
s.render.filepath=str(B/'pocket-rove-today-native-2160x3840.png')
bpy.context.view_layer.update()
# Ensure all captions fit and leave the real screen unobstructed.
bounds={}
for obj in s.objects:
    if obj.type=='FONT':
        pts=[world_to_camera_view(s,s.camera,obj.matrix_world@Vector(v)) for v in obj.bound_box]
        b=[min(v.x for v in pts),min(v.y for v in pts),max(v.x for v in pts),max(v.y for v in pts)];assert b[0]>=0 and b[1]>=0 and b[2]<=1 and b[3]<=1,(obj.name,b);bounds[obj.name]=b
screen_top=max(world_to_camera_view(s,s.camera,[REDACTED_EMAIL]).y for v in o.data.vertices)
assert screen_top<bounds['TYPE / support'][1]
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(B/'pocket-rove-today-native-2160x3840.blend'))
bpy.ops.render.render(write_still=True)
result={'render_completed':True,'source_png_sha256':expected,'source_dimensions':[1206,2622],'source_bytes_unchanged':True,'output_dimensions':[2160,3840],'screen_material':'Original PNG emission, strength 1, no added reflection or recoloring','screen_support_gap_pixels':round((bounds['TYPE / support'][1]-screen_top)*3840,1),'provenance':s['Screen provenance'],'user_visual_acceptance':'PENDING'}
(B/'verification.json').write_text(json.dumps(result,indent=2));print('NATIVE_TODAY_RENDER_COMPLETE')
