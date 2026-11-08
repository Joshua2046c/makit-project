case_w=param("front_width_mm",130.0)
case_h=param("front_height_mm",88.0)
corner_r=param("front_corner_radius_mm",9.0)
wall=param("wall_thickness_mm",2.4)
front_t=param("front_thickness_mm",2.0)
body_depth=param("body_depth_mm",17.2)
rear_depth=param("rear_depth_mm",6.5)
seam_gap=param("seam_shadow_mm",0.35)
case_origin=(-1.1368409883593,-9.80938572124045,-15.2)
front_bottom=rear_depth+seam_gap
front_underside=body_depth-front_t
outer_front=Pos(0,0,front_bottom)*extrude(RectangleRounded(case_w,case_h,corner_r),body_depth-front_bottom)
outer_front=fillet(outer_front.edges().group_by(Axis.Z)[-1],1.0)
outer_front=chamfer(outer_front.edges().group_by(Axis.Z)[0],0.25)
cavity=Pos(0,0,front_bottom-0.1)*extrude(RectangleRounded(case_w-2*wall,case_h-2*wall,corner_r-wall),front_underside-front_bottom+0.1)
shell_blank=outer_front-cavity
rear_floor=param("rear_floor_mm",2.4)
rear_outer=extrude(RectangleRounded(case_w,case_h,corner_r),rear_depth)
rear_outer=chamfer(rear_outer.edges().group_by(Axis.Z)[0],0.6)
rear_blank=rear_outer-Pos(0,0,rear_floor)*extrude(RectangleRounded(case_w-2*wall,case_h-2*wall,corner_r-wall),rear_depth)
lip_root=Pos(0,0,rear_depth-1.0)*extrude(RectangleRounded(case_w-2*wall+0.6,case_h-2*wall+0.6,corner_r-wall+0.3)-RectangleRounded(case_w-2*wall-3.4,case_h-2*wall-3.4,corner_r-wall-1.7),1.0)
lip=Pos(0,0,rear_depth)*extrude(RectangleRounded(case_w-2*wall-0.6,case_h-2*wall-0.6,corner_r-wall-0.3)-RectangleRounded(case_w-2*wall-3.4,case_h-2*wall-3.4,corner_r-wall-1.7),2.15)
rear_blank=rear_blank+lip_root+lip

# The rear exterior establishes an 8 degree wedge; the internal datum stays flat.
from math import tan, radians
slope_angle=param("wedge_angle_deg",8.0)
wedge_edge=param("wedge_edge_chamfer_mm",0.6)
wedge_rise=case_h*tan(radians(slope_angle))
rear_slope_outer=Pos(0,0,-wedge_rise)*extrude(RectangleRounded(case_w,case_h,corner_r),rear_depth+wedge_rise)
under_slope=Pos(0,0,-wedge_rise/2)*Rot(-slope_angle,0,0)*Pos(0,0,-150)*Box(500,500,300)
rear_slope_outer-=under_slope
bottom_face=[face for face in rear_slope_outer.faces() if face.geom_type==GeomType.PLANE and face.normal_at().Z < -0.95][0]
rear_slope_outer=chamfer(bottom_face.edges(),wedge_edge)
rear_wedge_blank=rear_slope_outer-Pos(0,0,rear_floor)*extrude(RectangleRounded(case_w-2*wall,case_h-2*wall,corner_r-wall),rear_depth)
rear_wedge_blank=rear_wedge_blank+lip_root+lip


# All hardware positions below come from the official Rev-C assembly.
from screwjoint import make_screw_joint_v1, ScrewJointNotApplicableV1
window_w=param("display_aperture_width_mm",72.5)
window_h=param("display_aperture_height_mm",32.5)
lens_w=param("lens_width_mm",79.0)
lens_h=param("lens_height_mm",39.0)
lens_t=param("lens_thickness_mm",1.0)
lens_clearance=param("lens_edge_clearance_mm",0.2)
mask_w=param("black_face_width_mm",118.0)
mask_h=param("black_face_height_mm",54.0)
mask_t=param("black_face_thickness_mm",1.0)
joy_hole=param("joystick_clearance_mm",17.4)
mic_hole=param("microphone_port_mm",2.4)
speaker_slot=param("speaker_slot_width_mm",1.4)
usb_w=param("usb_well_width_mm",14.0)
usb_h=param("usb_well_height_mm",7.0)
sd_w=param("sd_opening_width_mm",19.5)
sd_h=param("sd_opening_height_mm",5.8)
power_w=param("power_slot_width_mm",10.2)
power_h=param("power_slot_height_mm",3.0)
closure_engage=param("case_screw_engagement_mm",3.6)
closure_post_d=param("closure_receiver_post_mm",6.0)
cx,cy,cz=case_origin
lcd_xy=(-0.00405870167067,-0.067211235931)
mask_xy=(cx,4.0)
key_centres=[(49.7881815828,4.6270648332),(40.5881612628,-4.7709539628),(49.3403659872,-15.6007736225),(-40.5040587017,-36.0384164977),(-49.2670762277,-35.9114162437)]
mic_centres=[(-29.5431468217,19.8452436435),(27.4095506274,19.8234021511)]
speaker_xy=(48.7231155427,-28.3422011053)
power_xy=(-43.4545743227,23.8)
closure_xy=[(-58.5,-37.5),(-58.5,37.5),(58.5,-37.5),(58.5,37.5)]
def local_xy(xy):
    return (xy[0]-cx,xy[1]-cy)
# Compact, mirror-symmetric side openings with inward return walls and floors.
port_wall=param("port_return_wall_mm",1.4)
usb_axial_relief=param("usb_throat_axial_relief_mm",0.6)
usb_mouth_w=param("usb_mouth_width_mm",16.0)
usb_mouth_h=param("usb_mouth_height_mm",7.0)
usb_r=param("usb_mouth_radius_mm",1.5)
header_mouth_w=param("header_mouth_width_mm",29.5)
header_mouth_h=param("header_mouth_height_mm",5.2)
header_inner_w=param("header_throat_width_mm",27.6)
header_inner_h=param("header_throat_height_mm",4.2)
header_r=param("header_mouth_radius_mm",1.3)
tf_mouth_w=param("tf_mouth_width_mm",20.5)
tf_mouth_h=param("tf_mouth_height_mm",8.0)
tf_r=param("tf_mouth_radius_mm",1.8)
tf_centre_y=param("tf_recess_centre_y_mm",-21.0)
retainer_margin=param("tf_retainer_relief_mm",0.3)
# Connector datums read from official Rev-C STEP; U14 z -8.1200 .. -5.7200.
USB_X=41.9191061447
USB_Z=-2.745
HEADER_X=-1.134125
HEADER_Z=-6.920016257
TF_Z=-3.9
def side_section(point,width,height,radius,side):
    x,y,z=point
    if side=="top":
        return Pos(x-cx,y-cy,z-cz)*Rot(-90,0,0)*RectangleRounded(width,height,radius)
    return Pos(x-cx,y-cy,z-cz)*Rot(0,-90,0)*RectangleRounded(height,width,radius)
def stepped_tunnel(p0,p1,inner,outer,side,extra_wall=0.0,lead_clearance=0.25):
    wall_t=port_wall+extra_wall
    axis=(0,1,0) if side=="top" else (-1,0,0)
    before=tuple(p0[i]-lead_clearance*axis[i] for i in range(3))
    after=tuple(p1[i]+0.25*axis[i] for i in range(3))
    iw,ih,ir=inner
    ow,oh,orr=outer
    bore=loft([side_section(before,iw,ih,ir,side),side_section(p0,iw,ih,ir,side),side_section(p1,ow,oh,orr,side),side_section(after,ow,oh,orr,side)],ruled=True)
    surround=loft([side_section(p0,iw+2*wall_t,ih+2*wall_t,ir+wall_t,side),side_section(p1,ow+2*wall_t,oh+2*wall_t,orr+wall_t,side)],ruled=True)
    return bore,surround
usb_spec=((USB_X,25.8,USB_Z),(USB_X,cy+case_h/2,USB_Z),(usb_w,usb_h,usb_r),(usb_mouth_w,usb_mouth_h,usb_r),"top")
header_spec=((HEADER_X,27.5,HEADER_Z),(HEADER_X,cy+case_h/2,HEADER_Z),(header_inner_w,header_inner_h,1.0),(header_mouth_w,header_mouth_h,header_r),"top")
tf_spec=((-59.7,tf_centre_y,TF_Z),(cx-case_w/2,tf_centre_y,TF_Z),(sd_w,sd_h,1.5),(tf_mouth_w,tf_mouth_h,tf_r),"left")
usb_cut,usb_surround=stepped_tunnel(*usb_spec,lead_clearance=usb_axial_relief)
expansion_cut,header_surround=stepped_tunnel(*header_spec)
sd_cut,tf_surround=stepped_tunnel(*tf_spec)
# Clear the confirmed lower-left joystick-retainer wing, leaving the outer rim intact.
kx0,kx1=-65.375-retainer_margin,-59.7+retainer_margin
ky0,ky1=-11.7-retainer_margin,-7.5
kz0,kz1=-3.525-retainer_margin,-1.525+retainer_margin
retainer_relief=Pos((kx0+kx1)/2-cx,(ky0+ky1)/2-cy,(kz0+kz1)/2-cz)*Box(kx1-kx0,ky1-ky0,kz1-kz0)
tf_surround-=retainer_relief
surrounds=usb_surround+header_surround+tf_surround
front_sleeves=((usb_surround+tf_surround) & outer_front)+header_surround
rear_sleeves=(usb_surround+tf_surround) & rear_slope_outer
# Relieve the old guiding lip locally so front return walls cannot trap the rear lid.
inflated_surrounds=[]
for spec in [usb_spec,header_spec,tf_spec]:
    unused,wide=stepped_tunnel(*spec,extra_wall=0.3)
    inflated_surrounds.append(wide)
lip_zone=Pos(0,0,front_bottom-0.3+50)*Box(400,400,100)
sleeve_lip_keepout=((inflated_surrounds[0]+inflated_surrounds[2]) & lip_zone)+inflated_surrounds[1]
power_cut=Pos(power_xy[0]-cx,33.0-cy,-2.2-cz)*Rot(90,0,0)*extrude(RectangleRounded(power_w,power_h,0.6),4.5,both=True)
access_tools=[usb_cut,expansion_cut,sd_cut]
port_tools=access_tools+[power_cut]

shell=shell_blank+front_sleeves
# Curated non-grid cheese pattern; all dimples are blind spherical caps.
cheese_size=param("cheese_size_scale",1.0)
cheese_front_depth=param("cheese_front_depth_scale",1.0)
cheese_side_depth=param("cheese_side_depth_scale",1.0)
cheese_back_depth=param("cheese_back_depth_scale",1.0)
front_pit_floor=param("cheese_front_remaining_mm",1.6)
cheese_front_layout=[(-22,-36,13,1.2),(3,-45,8,1.53),(22,-33,15,1.98),(38,-45,5,1.26),(-5,-27.5,4.5,1.08),(-9,-53.3,9,1.35),(-65.2,15,4.5,1.08),(-54,35.3,7,1.17),(64,-5,5.2,1.17)]
# A matching blind spherical scoop straddles the lower-left rolled corner.
from math import sqrt
corner_pit_d=param("corner_cheese_diameter_mm",8.0)
corner_pit_depth=param("corner_cheese_depth_mm",1.0)
corner_pit_inset=param("corner_cheese_plan_inset_mm",1.2)
corner_pit_x=cx-case_w/2+corner_r-(corner_r-corner_pit_inset)/sqrt(2)
corner_pit_y=cy-case_h/2+corner_r-(corner_r-corner_pit_inset)/sqrt(2)
cheese_front_layout.append((corner_pit_x,corner_pit_y,corner_pit_d,corner_pit_depth))

def cap_tool(p,n,diameter,depth):
    radius=((diameter/2)**2+depth**2)/(2*depth)
    centre=[p[i]+n[i]*(radius-depth) for i in range(3)]
    # Keep each spherical cap away from the sphere seam and polar singularities.
    if abs(n[0])>0.9:
        orientation=Rot(0,0,90*n[0])
    elif n[2]>0.9:
        orientation=Rot(-90,0,0)
    elif n[2]<-0.9:
        orientation=Rot(90-slope_angle,0,0)
    elif n[1]>0.9:
        orientation=Rot(0,0,180)
    else:
        orientation=Rot(0,0,0)
    return Pos(centre[0]-cx,centre[1]-cy,centre[2]-cz)*orientation*Sphere(radius)
cheese_front_tools=[]
cheese_front_pads=[]
for x,y,diameter,depth in cheese_front_layout:
    diameter*=cheese_size
    depth*=cheese_front_depth
    pad=max(0.0,depth+front_pit_floor-front_t)
    cheese_front_pads.append((Pos(x-cx,y-cy,front_underside-pad)*Cylinder(diameter/2+1.0,pad+0.1,align=(Align.CENTER,Align.CENTER,Align.MIN))) & outer_front)
    cheese_front_tools.append(cap_tool((x,y,body_depth+cz),(0,0,1),diameter,depth))
cheese_front_sides=[
    ((cx-case_w/2,18,-4),(-1,0,0),7,0.7),
    ((cx-case_w/2,-41,-4),(-1,0,0),5.5,0.6),
    ((cx+case_w/2,10,-4),(1,0,0),5,0.7),
    ((cx+case_w/2,-37,-3),(1,0,0),6,0.65),
    ((-25,cy+case_h/2,-4),(0,1,0),5,0.65),
    ((-60,cy+case_h/2,-4),(0,1,0),6,0.65),
    ((-28,cy-case_h/2,-3),(0,-1,0),5,0.6),
    ((20,cy-case_h/2,-4),(0,-1,0),7,0.7)
]
for p,n,diameter,depth in cheese_front_sides:
    cheese_front_tools.append(cap_tool(p,n,diameter*cheese_size,depth*cheese_side_depth))

for pad in cheese_front_pads:
    shell+=pad
sx,sy=local_xy(lcd_xy)
# A stepped lens seat: adhesive carries the lens, never the LCD glass.
shell-=Pos(sx,sy,body_depth-1.1)*extrude(RectangleRounded(lens_w+2*lens_clearance,lens_h+2*lens_clearance,2.2),1.3)
shell-=Pos(sx,sy,front_underside-0.1)*extrude(RectangleRounded(window_w,window_h,0.9),front_t+0.3)
mx,my=local_xy(mask_xy)
shell-=Pos(mx,my,body_depth-0.12)*extrude(RectangleRounded(mask_w+0.4,mask_h+0.4,3.5),0.25)
middle_key_hole=param("middle_key_hole_mm",7.2)
key_b_cut=Circle(middle_key_hole/2)
for i,(x,y) in enumerate(key_centres):
    x,y=local_xy((x,y))
    if i==1:
        shell-=Pos(x,y,front_underside-0.1)*extrude(key_b_cut,front_t+0.3)
    else:
        diameter=[8.6,0,11.1,7.2,7.2][i]
        shell-=Pos(x,y,front_underside+front_t/2)*Cylinder(diameter/2,front_t+0.4)
jx,jy=local_xy((-49.525,0.75))
shell-=Pos(jx,jy,front_underside+front_t/2)*Cylinder(joy_hole/2,front_t+0.4)
for xy in mic_centres:
    x,y=local_xy(xy)
    shell-=Pos(x,y,front_underside+front_t/2)*Cylinder(mic_hole/2,front_t+0.4)
spx,spy=local_xy(speaker_xy)
for dx in [-2.8,0,2.8]:
    shell-=Pos(spx+dx,spy,front_underside-0.1)*extrude(RectangleRounded(speaker_slot,7.0,0.69),front_t+0.3)
shell=shell-port_tools
# Short guides keep the captured top-edge power key square to the switch.
px,py=local_xy(power_xy)
for dx in [-7.5,7.5]:
    shell+=Pos(px+dx,29.2-cy,-2.0-cz)*Box(1.2,6.5,4.2)
closure_cuts=[]
closure_bom=[]
closure_ids=[]
for i,(x,y) in enumerate(closure_xy):
    try:
        joint=make_screw_joint_v1(size="M2.5",at=Pos(x,-y,0),through=[(Rot(180,0,0)*rear_blank,rear_floor)],seat="countersink",engage_depth=closure_engage,into=Rot(180,0,0)*shell,material="PETG",label="case:back-"+str(i))
    except ScrewJointNotApplicableV1 as rejected:
        print("Free structural post after kit rejection:",str(rejected))
        # Explicit free structural bridge; the kit still owns the compensated pilot,
        # countersink and screw. The post joins the inner face, clear of the PCB.
        shell+=Pos(x,y,rear_floor)*Cylinder(closure_post_d/2,front_underside-rear_floor+0.2,align=(Align.CENTER,Align.CENTER,Align.MIN))
        joint=make_screw_joint_v1(size="M2.5",at=Pos(x,-y,0),through=[(Rot(180,0,0)*rear_blank,rear_floor)],seat="countersink",engage_depth=closure_engage,into=Rot(180,0,0)*shell,material="PETG",boss="none",label="case:back-"+str(i))
    if joint.bosses.wrapped is not None:
        shell+=Rot(180,0,0)*joint.bosses
    shell-=Rot(180,0,0)*joint.engage_cuts
    closure_cuts.extend([Rot(180,0,0)*cut for cut in joint.through_cuts])
    closure_bom.extend(joint.bom)
    sid="case_screw_"+str(i+1)
    closure_ids.append(sid)
    publish(sid,Pos(cx,cy,cz)*Rot(180,0,0)*joint.hardware,"后壳沉头螺钉",material="stainless_steel",role="fastener")
    print("Closure",i,joint.screw_length_mm,joint.boss_length_mm,joint.head_land_mm,joint.notes)
assert len(closure_ids)==4
shell=shell-cheese_front_tools
shell.color=srgb("#e2c5ad")
publish("front_panel",shell,"米杏色结构前壳",material="petg")
