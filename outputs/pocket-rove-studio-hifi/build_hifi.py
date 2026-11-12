"""Pocket Rove — high fidelity reusable studio. Blender 4.5 LTS.
blender -b -t 6 --python build_hifi.py -- --preview
blender -b -t 6 --python build_hifi.py
"""
import bpy, math, argparse, sys, json
from pathlib import Path
from mathutils import Vector
B=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--screen',default=str(B/'assets/screen-souvenirs-1.6.3.png'));ap.add_argument('--tag',default='v1');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=48 if a.preview else 256;s.cycles.use_denoising=True;s.cycles.adaptive_threshold=.012;s.cycles.max_bounces=8;s.cycles.transparent_max_bounces=8
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
for d in p.devices:d.use=(d.type=='METAL')
s.cycles.device='GPU' if any(d.type=='METAL' for d in p.devices) else 'CPU'
s.render.resolution_x=2160;s.render.resolution_y=3840;s.render.resolution_percentage=25 if a.preview else 100
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.color_depth='8';s.render.film_transparent=False
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
s.world=bpy.data.worlds.new('Soft neutral studio ambient');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.7,.77,.74,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.28

def color(h):
    v=[int(h[i:i+2],16)/255 for i in (0,2,4)];return tuple(x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v)+(1,)
def material(name,h,metal=0,rough=.4,emit=False):
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();o=n.new('ShaderNodeOutputMaterial');b=n.new('ShaderNodeEmission' if emit else 'ShaderNodeBsdfPrincipled')
    if emit:b.inputs['Color'].default_value=color(h)
    else:b.inputs['Base Color'].default_value=color(h);b.inputs['Metallic'].default_value=metal;b.inputs['Roughness'].default_value=rough
    m.node_tree.links.new(b.outputs[0],o.inputs[0]);return m

def micro(m,scale,strength,distance,rough_lo=None,rough_hi=None):
    n=m.node_tree.nodes;l=m.node_tree.links;b=next(x for x in n if x.type=='BSDF_PRINCIPLED');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=scale;noise.inputs['Detail'].default_value=3
    tex=n.new('ShaderNodeTexCoord');l.new(tex.outputs['Generated'],noise.inputs['Vector']);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=strength;bump.inputs['Distance'].default_value=distance;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],b.inputs['Normal'])
    if rough_lo is not None:
        ramp=n.new('ShaderNodeMapRange');ramp.inputs['To Min'].default_value=rough_lo;ramp.inputs['To Max'].default_value=rough_hi;l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],b.inputs['Roughness'])
    return m
sage=micro(material('SET / mineral sage plaster','B2C6B4',rough=.9),90,.11,.009)
stone=micro(material('PLINTH / honed warm limestone','D9D2BF',rough=.63),130,.14,.012,.53,.7)
forest=micro(material('FRAME / satin forest titanium','3C6158',.82,.26),230,.045,.0006,.22,.29)
polish=material('FRAME / polished chamfer','81968D',.92,.19)
glass=material('GLASS / black ceramic edge','081311',.18,.16)
gold=micro(material('ACCENT / brushed champagne metal','CEAC68',.82,.31),180,.06,.0005,.25,.34)
rubber=material('DETAIL / antenna polymer','9EAEA5',.05,.52)
ink=material('TYPE / evergreen','153E32',emit=True)
secondary=material('TYPE / muted green','466150',emit=True)

def outline(w,h,r,n=24):
    pts=[]
    for cx,cy,start in [(w/2-r,h/2-r,0),(-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180),(w/2-r,-h/2+r,270)]:
        for j in range(n+1):
            t=math.radians(start+j*90/n);pts.append((cx+r*math.cos(t),cy+r*math.sin(t)))
    return pts

def rounded(name,w,h,r,layers,mat):
    # Layers=(z,inset); perimeter radius independent of thickness.
    vs=[]
    for z,inset in layers:vs += [(x,y,z) for x,y in outline(w-2*inset,h-2*inset,max(r-inset,.01))]
    N=len(vs)//len(layers);fs=[tuple(reversed(range(N)))]
    for k in range(len(layers)-1):
        for i in range(N):j=(i+1)%N;fs.append((k*N+i,k*N+j,(k+1)*N+j,(k+1)*N+i))
    fs.append(tuple((len(layers)-1)*N+i for i in range(N)))
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(vs,[],fs);mesh.update();o=bpy.data.objects.new(name,mesh);s.collection.objects.link(o);mesh.materials.append(mat)
    for p in mesh.polygons:p.use_smooth=(len(p.vertices)==4)
    return o

def box(name,loc,dim,mat,bev=.03):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
    if bev:
        b=o.modifiers.new('Machined bevel','BEVEL');b.width=bev;b.segments=5;o.modifiers.new('Surface normals','WEIGHTED_NORMAL')
    return o

def cylinder(name,loc,r,depth,mat):
    bpy.ops.mesh.primitive_cylinder_add(vertices=128,radius=r,depth=depth,location=loc);o=bpy.context.object;o.name=name;o.data.materials.append(mat);b=o.modifiers.new('Edge bevel','BEVEL');b.width=.025;b.segments=4;o.modifiers.new('Surface normals','WEIGHTED_NORMAL');return o

# Real curved backdrop, physically lit; no fake emission floor.
prof=[(-40,0),(2.5,0)]
for j in range(1,33):
    t=(math.pi/2)*j/32;prof.append((2.5+4*math.sin(t),4-4*math.cos(t)))
prof.append((6.5,25))
vs=[(x,y,z) for x in [-35,35] for y,z in prof];N=len(prof);fs=[(i,i+1,N+i+1,N+i) for i in range(N-1)]
m=bpy.data.meshes.new('Cyclorama mesh');m.from_pydata(vs,[],fs);m.materials.append(sage);o=bpy.data.objects.new('SET / seamless cyclorama',m);s.collection.objects.link(o)
for p in m.polygons:p.use_smooth=True
# Low oval limestone plinth, with a fine metal reveal.
pl=rounded('PLINTH / oval limestone block',5.9,3.8,1.35,[(.1,.055),(.15,.01),(.72,0),(.78,.025),(.80,.06)],stone);pl.location=(.18,.12,0)
rv=rounded('PLINTH / champagne shadow reveal',5.83,3.73,1.32,[(.06,.03),(.13,0)],gold);rv.location=pl.location
# Raised architectural roundel creates subtle depth behind the subject.
bpy.ops.mesh.primitive_cylinder_add(vertices=160,radius=2.35,depth=.20,location=(1.34,2.25,3.45),rotation=(math.pi/2,0,0));o=bpy.context.object;o.name='SET / sculpted sage roundel';o.data.materials.append(sage);b=o.modifiers.new('Soft perimeter','BEVEL');b.width=.1;b.segments=6;o.modifiers.new('Surface normals','WEIGHTED_NORMAL')
# Product geometry.
root=bpy.data.objects.new('PHONE / master transform',None);s.collection.objects.link(root);root.location=(.25,-.1,4.2);root.rotation_euler=(math.radians(90),math.radians(-9),math.radians(-13))
def child(o,loc=(0,0,0)):o.parent=root;o.location=loc;return o
body=child(rounded('PHONE / precision rounded titanium chassis',3.17,6.692,.41,[(-.165,.045),(-.15,.015),(-.12,0),(.11,0),(.145,.018),(.16,.04)],forest))
child(rounded('PHONE / polished front edge',3.125,6.647,.389,[(.143,.018),(.163,0),(.178,.013)],polish))
child(rounded('PHONE / continuous ceramic glass',3.094,6.616,.373,[(.167,.02),(.184,0),(.191,.009)],glass))
# Screenshot is the only source for all app pixels including its existing island.
w=3.0;h=w*2622/1206;r=.33;verts=[(x,y,.194) for x,y in outline(w,h,r,32)]
mesh=bpy.data.meshes.new('Original screen UV');mesh.from_pydata(verts,[],[tuple(range(len(verts)))]);mesh.update();uv=mesh.uv_layers.new(name='Unmodified screenshot')
for p in mesh.polygons:
    for li in p.loop_indices:
        co=mesh.vertices[mesh.loops[li].vertex_index].co;uv.data[li].uv=(co.x/w+.5,co.y/h+.5)
o=bpy.data.objects.new('SCREEN / replace original image',mesh);s.collection.objects.link(o);o.parent=root
screenmat=bpy.data.materials.new('SCREEN / faithful pixels with subtle glass reflection');screenmat.use_nodes=True;n=screenmat.node_tree.nodes;n.clear();links=screenmat.node_tree.links
out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(a.screen);tex.image.pack();tex.interpolation='Linear';links.new(tex.outputs['Color'],em.inputs['Color'])
# 0.8% surface reflection adds glass cues without obscuring text.
ref=n.new('ShaderNodeBsdfGlossy');ref.inputs['Roughness'].default_value=.10
mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=.008;links.new(em.outputs[0],mix.inputs[1]);links.new(ref.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],out.inputs[0]);mesh.materials.append(screenmat)
for name,x,y,hh in [('Power',1.60,.65,.73),('Volume up',-1.60,.96,.40),('Volume down',-1.60,.37,.40),('Action',-1.60,1.65,.26)]:
    child(box('DETAIL / '+name,(0,0,0),(.054,hh,.14),forest,.022),(x,y,-.01))
for x in [-1.587,1.587]:
    for y in [-2.38,2.38]:child(box('DETAIL / antenna separator',(0,0,0),(.004,.036,.19),rubber,.001),(x,y,-.015))
# Bottom USB-C port and machined speaker perforations, only visible at close angles.
child(box('DETAIL / USB-C recess',(0,0,0),(.34,.009,.085),glass,.004),(0,-3.343,-.007))
for x in [-.97,-.86,-.75,-.64,-.53,.53,.64,.75,.86,.97]:
    child(box('DETAIL / speaker aperture',(0,0,0),(.044,.009,.043),glass,.004),(x,-3.343,-.008))
bpy.context.view_layer.update();lowest=min(([REDACTED_EMAIL]).z for v in body.data.vertices);root.location.z += .802-lowest
# Small off-axis metallic sphere; no duplicated collectibles or floating ring.
cylinder('ACCENT / flat champagne puck',(-1.91,.46,.86),.43,.12,gold)
# Broad key plus shaped edge reflections and backdrop wash.
def light(name,loc,target,power,sx,sy,color=(1,1,1)):
    d=bpy.data.lights.new(name,'AREA');d.shape='RECTANGLE';d.energy=power;d.size=sx;d.size_y=sy;d.color=color;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
light('LIGHT / broad window key',(-5,-6,11),(0,0,3.3),450,5,7,(1,.97,.90))
light('LIGHT / vertical right reflection',(4,-2,7),(0,0,3.8),240,1.2,6,(.91,.97,1))
light('LIGHT / soft camera fill',(-1,-9,5),(0,0,3),130,4,4)
light('LIGHT / top separation',(1,3,11),(0,0,3.4),280,3,3,(1,.96,.85))
light('LIGHT / cyclorama wash',(-2,0,13),(0,6.5,9),450,9,9)
# Tall black reflector cards are excluded only from camera visibility.
for x in [-5.6,5.6]:
    card=box('FLAG / side negative fill',(x,0,4),(1,.12,8),material('Flag black '+str(x),'101010',rough=1),0);card.rotation_euler.z=math.radians(-30 if x<0 else 30);card.visible_camera=False
# Long lens produces a restrained, photographic perspective.
d=bpy.data.cameras.new('Product camera / 95mm');cam=bpy.data.objects.new('CAMERA / 4K portrait',d);s.collection.objects.link(cam);cam.location=(.2,-33.5,11.7);target=Vector((0,0,5.20));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();d.lens=95;d.sensor_fit='VERTICAL';d.sensor_height=36;d.clip_end=200;s.camera=cam
# Fine surface detail remains sharp; no fake blur on the product screen.
d.dof.use_dof=False
# Editorial, editable type on a camera-aligned plane.
regular=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial.ttf');bold=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Bold.ttf')
serif=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Baskerville.ttc')
frame=d.view_frame(scene=s);D=10;W=2*max(abs(v.x/v.z*D) for v in frame);H=2*max(abs(v.y/v.z*D) for v in frame)
def text(name,body,x,y,size,mat,font=regular,spacing=1):
    c=bpy.data.curves.new(name,'FONT');c.body=body;c.font=font;c.size=size*H;c.space_line=1.02;c.space_character=spacing;o=bpy.data.objects.new(name,c);s.collection.objects.link(o);o.parent=cam;o.location=(x*W,y*H,-D);c.materials.append(mat);o.visible_shadow=False;o.visible_diffuse=False;o.visible_glossy=False;return o
text('TYPE / brand','POCKET ROVE',-.414,.417,.018,ink,bold,1.18)
text('TYPE / collection index','THE SOUVENIR EDIT',.18,.417,.0105,secondary,regular,1.06)
text('TYPE / headline','Small adventures.\nWorth keeping.',-.419,.342,.061,ink,serif)
text('TYPE / support','Turn everyday curiosity into something to keep.',-.413,.229,.015,secondary)
text('TYPE / footer','A LITTLE MORE WONDER. EVERY DAY.',-.413,-.451,.0125,ink,bold,1.06)
# View presets and provenance.
s['Screen provenance']='1.6.3(1) Simulator, 2026-09-09; unchanged source; current production version not certified.'
s['Geometry']='Procedural rounded rectangle perimeter independent of thickness; 3 chassis layers; polymer separators and controls.'
s['Render']='2160x3840 / Cycles / Metal / 256 samples / adaptive / denoise / 95mm'
for ar in (bpy.context.screen.areas if bpy.context.screen else []):
    if ar.type=='VIEW_3D':ar.spaces.active.region_3d.view_perspective='CAMERA'
tag=('preview-'+a.tag) if a.preview else 'pocket-rove-hifi-2160x3840'
s.render.filepath=str(B/(tag+'.png'));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(B/(tag+'.blend')));bpy.ops.render.render(write_still=True)
print('HIFI_RENDER_COMPLETE',s.render.filepath)
