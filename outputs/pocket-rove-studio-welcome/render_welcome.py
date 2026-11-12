"""Load the included Welcome scene and optionally replace its screen image.
blender -b pocket-rove-welcome-2160x3840.blend --python render_welcome.py
"""
import bpy,sys
from pathlib import Path
B=Path(__file__).resolve().parent
s=bpy.context.scene
# The initial execution loads the previous studio. Subsequent runs can load the delivered scene.
old=[i for i in bpy.data.images if i.type=='IMAGE']
new=bpy.data.images.load(str(B/'assets/welcome-reference-screen.png'));new.pack()
obj=bpy.data.objects['SCREEN / replace original image']
for mat in obj.data.materials:
    mat.name='SCREEN / Welcome reference reconstruction'
    for n in mat.node_tree.nodes:
        if n.type=='TEX_IMAGE':n.image=new
# Preserve exact texture aspect within the existing screen UV with negligible edge cropping.
w,h=new.size;source_ratio=h/w;target_ratio=2622/1206
u_scale=min(1.,source_ratio/target_ratio);v_scale=min(1.,target_ratio/source_ratio)
for poly in obj.data.polygons:
    for li in poly.loop_indices:
        co=obj.data.vertices[obj.data.loops[li].vertex_index].co
        obj.data.uv_layers.active.data[li].uv=((co.x/3+.5-.5)*u_scale+.5,(co.y/(3*target_ratio)+.5-.5)*v_scale+.5)
headline=bpy.data.objects['TYPE / headline'];headline.data.body='Your next little\nadventure starts here.';headline.data.size=(20*max(abs(v.y/v.z) for v in s.camera.data.view_frame(scene=s)))*.061*.89
bpy.data.objects['TYPE / collection index'].data.body='MEET POCKET ROVE'
bpy.data.objects['TYPE / support'].data.body='A name. A little curiosity. A place to begin.'
s['Screen provenance']='AI reconstruction of inner Welcome UI from the user-provided 1-Welcome marketing image, 2026-09-11; not a native App screenshot.'
s['Screen source reference']='/Volumes/EXTERNAL/app/Pocket-Rove-人工上传-五张截图-20260911/1-欢迎页-Welcome.png'
s['Usage']='Reference-based design sample. Replace with an approved native target-version Welcome screenshot before claiming native UI fidelity.'
s.render.resolution_percentage=100;s.cycles.samples=256
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
for d in p.devices:d.use=(d.type=='METAL')
s.cycles.device='GPU'
s.render.filepath=str(B/'pocket-rove-welcome-2160x3840.png')
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(B/'pocket-rove-welcome-2160x3840.blend'));bpy.ops.render.render(write_still=True)
print('WELCOME_RENDER_COMPLETE',s.render.filepath)
