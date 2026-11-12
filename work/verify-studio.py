import bpy, json
from pathlib import Path
s=bpy.context.scene
base=Path('/Users/USER/Documents/Codex/2026-09-11/new-chat/outputs/pocket-rove-studio')
assert s.camera and len([o for o in s.objects if o.name.startswith('SCREEN |')])==1
imgs=[i for i in bpy.data.images if i.type=='IMAGE']
assert len(imgs)==1 and imgs[0].packed_file
assert tuple(imgs[0].size)==(1206,2622)
assert (s.render.resolution_x,s.render.resolution_y)==(1080,1920)
s.render.filepath=str(base/'pocket-rove-studio-1080x1920.png')
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(base/'pocket-rove-studio.blend'))
result={'blender':bpy.app.version_string,'objects':len(s.objects),'screen_objects':1,'source_image_size':list(imgs[0].size),'packed_image':True,'resolution':[1080,1920],'render_output':s.render.filepath,'status':'LOCAL_RENDER_AND_SCENE_PASS','visual_acceptance':'PENDING_USER'}
(base/'verification.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
