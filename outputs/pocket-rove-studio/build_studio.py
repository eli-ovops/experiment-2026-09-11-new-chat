"""Reusable Pocket Rove studio. Run: blender -b -t 6 --python build_studio.py -- --preview
Replace assets/screen-souvenirs-1.6.3.png or use --screen /absolute/file.png.
"""
import bpy, math, sys, argparse
from pathlib import Path
from mathutils import Vector
BASE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser()
ap.add_argument('--preview',action='store_true')
ap.add_argument('--screen',default=str(BASE/'assets/screen-souvenirs-1.6.3.png'))
args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.render.engine='CYCLES'
scene.cycles.samples=24 if args.preview else 64
scene.cycles.use_denoising=True
scene.cycles.max_bounces=5
scene.render.resolution_x=1080
scene.render.resolution_y=1920
scene.render.resolution_percentage=50 if args.preview else 100
scene.render.image_settings.file_format='PNG'
scene.view_settings.view_transform='Standard'
scene.view_settings.look='None'
scene.world=bpy.data.worlds.new('Studio ambient')
scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(0.8,0.88,0.82,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.3

def rgb(h):
    vals=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return tuple(v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4 for v in vals)+(1,)
def mat(name,h,metal=0,rough=.45,emit=False):
    m=bpy.data.materials.new(name);m.use_nodes=True
    nt=m.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial')
    n=nt.nodes.new('ShaderNodeEmission' if emit else 'ShaderNodeBsdfPrincipled')
    if emit:n.inputs['Color'].default_value=rgb(h)
    else:
        n.inputs['Base Color'].default_value=rgb(h);n.inputs['Metallic'].default_value=metal;n.inputs['Roughness'].default_value=rough
    nt.links.new(n.outputs[0],out.inputs['Surface']);return m
cream=mat('Backdrop | warm ivory','F4EEDA',rough=.8)
cream_shader=next(n for n in cream.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
nt=cream.node_tree
out=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL')
flat=nt.nodes.new('ShaderNodeEmission');flat.inputs['Color'].default_value=rgb('F4EEDA')
soft=nt.nodes.new('ShaderNodeMixShader');soft.inputs[0].default_value=.9
nt.links.new(cream_shader.outputs[0],soft.inputs[1]);nt.links.new(flat.outputs[0],soft.inputs[2])
path=nt.nodes.new('ShaderNodeLightPath');camera_only=nt.nodes.new('ShaderNodeMixShader')
nt.links.new(path.outputs['Is Camera Ray'],camera_only.inputs[0])
nt.links.new(cream_shader.outputs[0],camera_only.inputs[1]);nt.links.new(soft.outputs[0],camera_only.inputs[2])
nt.links.new(camera_only.outputs[0],out.inputs['Surface'])
mint=mat('Podium | soft mint','A7CFC0',rough=.65)
green=mat('Device | forest anodized metal','164D43',.72,.27)
black=mat('Bezel | near black','101A18',.2,.28)
gold=mat('Accent | satin brass','DDB963',.6,.3)
ink=mat('Type | forest','164D43',emit=True)
muted=mat('Type | secondary','557164',emit=True)

def cube(name,loc,scale,material,bevel=.08):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(material)
    if bevel:
        mod=o.modifiers.new('Soft machined edges','BEVEL');mod.width=bevel;mod.segments=6
        o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return o

def cyl(name,loc,r,depth,material):
    bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=r,depth=depth,location=loc)
    o=bpy.context.object;o.name=name;o.data.materials.append(material)
    b=o.modifiers.new('Soft edges','BEVEL');b.width=.055;b.segments=4
    o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');return o

cube('Infinite studio floor',(0,0,-.12),(200,200,.2),cream,.02)
cyl('Main circular plinth',(.35,0,.22),2.48,.44,mint)
cyl('Brass base reveal',(.35,0,.035),2.43,.06,gold)
# Device constructed around a single front screenshot, with no duplicated island or UI.
root=bpy.data.objects.new('PHONE | rotate or reposition entire device',None);scene.collection.objects.link(root)
root.location=(.3,0,3.96);root.rotation_euler=(math.radians(90),math.radians(-7),math.radians(-8))
def part(o,loc):o.parent=root;o.location=loc;return o
part(cube('Phone metal body',(0,0,0),(3.12,6.75,.25),green,.21),(0,0,0))
part(cube('Black glass bezel',(0,0,0),(3.035,6.665,.06),black,.205),(0,0,.14))
# Rounded screen polygon and pixel-faithful UV mapping.
w=2.92;h=w*2622/1206;r=.22
verts=[]
for cx,cy,start in [(w/2-r,h/2-r,0),(-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180),(w/2-r,-h/2+r,270)]:
    for j in range(13):
        a=math.radians(start+j*90/12);verts.append((cx+r*math.cos(a),cy+r*math.sin(a),.18))
mesh=bpy.data.meshes.new('Screen rounded UV mesh');mesh.from_pydata(verts,[],[list(range(len(verts)))]);mesh.update()
uv=mesh.uv_layers.new(name='Screen UV')
for p in mesh.polygons:
    for li in p.loop_indices:
        v=mesh.vertices[mesh.loops[li].vertex_index].co;uv.data[li].uv=(v.x/w+.5,v.y/h+.5)
screen=bpy.data.objects.new('SCREEN | replace image texture here',mesh);scene.collection.objects.link(screen);screen.parent=root
m=bpy.data.materials.new('SCREEN | original screenshot emission');m.use_nodes=True;n=m.node_tree.nodes;n.clear()
out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');tex=n.new('ShaderNodeTexImage')
tex.image=bpy.data.images.load(str(Path(args.screen).resolve()));tex.image.pack();tex.interpolation='Linear'
m.node_tree.links.new(tex.outputs['Color'],em.inputs['Color']);m.node_tree.links.new(em.outputs[0],out.inputs['Surface']);mesh.materials.append(m)
part(cube('Power button',(0,0,0),(.065,.67,.1),gold,.025),(1.575,.8,0))
part(cube('Volume button',(0,0,0),(.065,.6,.1),green,.025),(-1.575,.85,0))
# Abstract studio props; deliberately no duplicated app collectibles.
bpy.ops.mesh.primitive_torus_add(major_radius=.63,minor_radius=.10,major_segments=80,minor_segments=16,location=(-2.25,.85,1.09),rotation=(math.pi/2,0,.25))
bpy.context.object.name='Satin brass orbit';bpy.context.object.data.materials.append(gold)
for p in bpy.context.object.data.polygons:p.use_smooth=True
cube('Mint display block',(2.2,1.1,.8),(1.2,1.15,1.6),mint,.12)
cyl('Small brass disc',(2.2,1.1,1.64),.42,.08,gold)
# Lighting

def area(name,loc,energy,size,target,color=(1,1,1)):
    d=bpy.data.lights.new(name,'AREA');d.energy=energy;d.shape='DISK';d.size=size;d.color=color
    o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
area('KEY | large softbox',(-5,-8,12),550,7,(0,0,3),(1,.93,.81))
area('FILL | neutral',(6,-4,7),325,5,(0,0,3))
area('RIM | upper rear',(2,5,10),600,4,(0,0,4),(1,.98,.87))
d=bpy.data.cameras.new('Portrait camera');cam=bpy.data.objects.new('CAMERA | 1080 x 1920',d);scene.collection.objects.link(cam)
cam.location=(4,-23,11);target=Vector((0,0,4.8));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
d.type='ORTHO';d.ortho_scale=13.8;d.lens=55;scene.camera=cam
# Editable camera-facing typography. Emission keeps exact brand colors.
font=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial.ttf')
bold=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Bold.ttf')
def label(name,body,x,y,size,material,font=font):
    curve=bpy.data.curves.new(name,'FONT');curve.body=body;curve.font=font;curve.size=size;curve.space_line=1.08
    o=bpy.data.objects.new(name,curve);scene.collection.objects.link(o);o.parent=cam;o.location=(x,y,-12);o.rotation_euler=(0,0,0);curve.materials.append(material)
    if hasattr(o,'visible_shadow'):o.visible_shadow=False
    return o
label('Brand','POCKET ROVE',-3.12,5.62,.25,ink,bold)
label('Headline','Small adventures.\nWorth keeping.',-3.15,4.62,.66,ink,bold)
label('Subheading','A little curiosity. A new story to collect.',-3.10,2.96,.22,muted)
label('Footer left','MAKE TODAY AN ADVENTURE',-3.1,-5.8,.19,ink,bold)

# Save useful metadata and make camera view the default.
scene['Screen provenance']='Pocket Rove 1.6.3(1), Simulator capture 2026-09-09; studio concept only, not certified current store UI.'
scene['Usage']='Edit SCREEN material image, headline objects, or PHONE parent; original screenshot is packed.'
for a in (bpy.context.screen.areas if bpy.context.screen else []):
    if a.type=='VIEW_3D':a.spaces.active.region_3d.view_perspective='CAMERA'
scene.render.filepath=str(BASE/('preview-r2.png' if args.preview else 'pocket-rove-studio-1080x1920.png'))
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(BASE/('studio-preview-r2.blend' if args.preview else 'pocket-rove-studio.blend')))
bpy.ops.render.render(write_still=True)
print('STUDIO_RENDER_COMPLETE',scene.render.filepath)
