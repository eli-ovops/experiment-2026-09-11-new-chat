import bpy,hashlib,json
from pathlib import Path
B=Path('/Users/USER/Documents/Codex/2026-09-11/new-chat/outputs/pocket-rove-studio-today-native');s=bpy.context.scene
o=bpy.data.objects['SCREEN / native Today PNG'];m=o.data.materials[0];n=m.node_tree.nodes
out=next(x for x in n if x.type=='OUTPUT_MATERIAL');em=out.inputs['Surface'].links[0].from_node
assert em.type=='EMISSION' and em.inputs['Strength'].default_value==1
tex=em.inputs['Color'].links[0].from_node;assert tex.type=='TEX_IMAGE' and tex.image.packed_file
sha=hashlib.sha256(bytes(tex.image.packed_file.data)).hexdigest();assert sha=='21788cba5245d011fc3eb464c920410f725c01a94e1c534032052b45f513c861'
assert s.view_settings.view_transform=='Standard' and s.view_settings.exposure==0 and s.view_settings.gamma==1
r={'scene_readback':'PASS','material_chain':'Packed original PNG -> Emission (1.0) -> Surface','packed_image_sha256':sha,'source_color_pipeline':'Standard / exposure 0 / gamma 1','screen_material_no_color_adjustment':True}
(B/'scene-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
