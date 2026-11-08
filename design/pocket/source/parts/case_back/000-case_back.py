d=part("front_panel")
from screwjoint import make_screw_joint_v1
edge_clearance=param("rear_post_clearance_mm",0.3)
battery_clearance=param("battery_side_clearance_mm",0.5)
rail_t=param("battery_guide_wall_mm",1.2)
rail_height=param("battery_guide_height_mm",3.1)
foam_t=param("battery_foam_tape_mm",0.5)
board_engage=param("pcb_screw_engagement_mm",3.6)

cx,cy,cz=d.case_origin
rear=d.rear_wedge_blank+d.rear_sleeves-d.port_tools-d.closure_cuts-d.sleeve_lip_keepout
# Tool access wells terminate at the kit's unchanged flat countersink seats.
tool_well_d=param("closure_tool_well_diameter_mm",8.0)
corner_well_d=param("curved_bore_tool_access_mm",5.5)
for x,y in d.closure_xy:
    rear-=Pos(x,y,-d.wedge_rise-0.2)*Cylinder((corner_well_d if x>0 and y>0 else tool_well_d)/2,d.wedge_rise+0.2,align=(Align.CENTER,Align.CENTER,Align.MIN))

post_radius=(d.joint.boss_outer_diameter_mm or d.closure_post_d)/2
for x,y in d.closure_xy:
    rear-=Pos(x,y,d.rear_floor)*Cylinder(post_radius+edge_clearance,d.rear_depth+2.3-d.rear_floor,align=(Align.CENTER,Align.CENTER,Align.MIN))
# Original HAC-006 cell section, distinct from the straight CAD wire.
CELL_W=51.0
CELL_H=24.2
cell_xy=(12.976318023282,-29.455820590922)
cell_bottom=-11.5050809258538-cz
bx,by=d.local_xy(cell_xy)
pad_h=cell_bottom-foam_t-d.rear_floor
assert pad_h>0
rear+=Pos(bx,by,d.rear_floor-0.05)*extrude(RectangleRounded(CELL_W-0.4,CELL_H-0.4,1.0),pad_h+0.05)
inner_w=CELL_W+2*battery_clearance
inner_h=CELL_H+2*battery_clearance
rail=Pos(bx,by,d.rear_floor-0.05)*extrude(RectangleRounded(inner_w+2*rail_t,inner_h+2*rail_t,2.2)-RectangleRounded(inner_w,inner_h,1.0),rail_height+0.05)
rail-=Pos(-13.6-cx,-21.1058-cy,d.rear_floor+rail_height/2)*Box(4.5,6.0,rail_height+0.4)
rear+=rail
board=Pos(-cx,-cy,-cz)*Pos(-73.7781252498037,-52.9294502798149,-5.72001517401775)*asset("design/pocket/source/assets/53d7209ca18c5d4aa690723ef7e639b336ca0cfdc735c3f48faaba731ad1a133.step")
joystick=Pos(-cx,-cy,-cz)*Pos(-150.725,-46.35,-6.1)*Rot(-90,0,-90)*asset("design/pocket/source/assets/f2cc66c38d4aa91f9d587cdfef6a2b50491d38117eb2db6cf510732895c8e409.step")
PCB_T=1.200152400305
PCB_TOP=-4.51986277371275
board_holes=[(-51.2990802917137,15.3966863724581),(-40.5040587016707,-25.7513959237059),(45.8177091418563,-39.7976240161619),(50.0091239246863,14.9140854072561)]
board_bom=[]
for i,(x,y) in enumerate(board_holes):
    joint=make_screw_joint_v1(size="M2.5",at=Pos(x-cx,y-cy,PCB_TOP-cz),through=[(board,PCB_T)],seat="surface",engage_depth=board_engage,into=rear,material="PETG",label="pcb:"+str(i))
    if joint.bosses.wrapped is not None:
        rear+=joint.bosses
    rear-=joint.engage_cuts
    publish("pcb_screw_"+str(i+1),Pos(cx,cy,cz)*joint.hardware,"主板固定螺钉",material="stainless_steel",role="fastener")
    board_bom.extend(joint.bom)
    print("PCB joint",i,joint.screw_length_mm,joint.boss_length_mm,joint.boss_outer_diameter_mm,joint.notes)
retainer=part("joystick_retainer")
for boss in retainer.bosses:
    if boss.wrapped is not None:
        rear+=boss
rear=rear-retainer.cuts
# Broad underside seat takes joystick finger load; the thin ear spacers carry only screw preload.
rear+=Pos(-49.525-cx,0.75-cy,d.rear_floor-0.05)*extrude(RectangleRounded(18.0,15.0,1.0),-6.45-cz-d.rear_floor+0.05)
connections={"case":4,"pcb":4,"joystick_retainer":2}
assert sum(connections.values())==10
# Large scoops use the added wedge volume, with smaller caps on thin side regions.
from math import sin,cos,tan,radians
# The marked side bowls are the two ends of a curved through-passage.
curve_d=param("curved_bore_diameter_mm",4.0)
curve_lip_r=param("curved_bore_lip_radius_mm",0.5)
curve_R=param("ring_passage_radius_mm",18.0)
curve_plane_z=param("ring_passage_plane_z_mm",-18.5)
curve_overrun=param("ring_passage_overrun_deg",10.0)
entry_face=cx+d.case_w/2
exit_face=cy+d.case_h/2
curve_entry_y=exit_face-curve_R
curve_exit_x=entry_face-curve_R
curve_entry_z=curve_plane_z
curve_exit_z=curve_plane_z
ring_axis_layout=(entry_face,exit_face,curve_plane_z)

back_sides=[
    ((cx-d.case_w/2,18,-18),(-1,0,0),12,2.1),
    ((cx-d.case_w/2,-4,-16),(-1,0,0),7,1.4),
    ((cx-d.case_w/2,-40,-12.5),(-1,0,0),5,0.8),
    ((cx+d.case_w/2,curve_entry_y,curve_entry_z),(1,0,0),13,2.2),
    ((cx+d.case_w/2,-7,-15.5),(1,0,0),8,1.5),
    ((cx+d.case_w/2,-37,-12.3),(1,0,0),5.8,0.75),
    ((-35,cy+d.case_h/2,-18),(0,1,0),9,1.6),
    ((10,cy+d.case_h/2,-19.5),(0,1,0),12,2.0),
    ((curve_exit_x,cy+d.case_h/2,curve_exit_z),(0,1,0),7,1.2),
    ((-10,cy-d.case_h/2,-12),(0,-1,0),3.8,0.7),
    ((34,cy-d.case_h/2,-12.4),(0,-1,0),5,0.8)
]
rear_cheese_tools=[]
for p,n,diameter,depth in back_sides:
    rear_cheese_tools.append(d.cap_tool(p,n,diameter*d.cheese_size,depth*d.cheese_side_depth))
# Restored spherical bottom pits and the original three scoops crossing the bottom rim.
bottom_depth_scale=param("bottom_cheese_depth_scale",1.0)
bottom_layout=[(-32,12,19,2.8),(7,3,12,2.0),(33,18,22,3.1),(-17,-20,13,1.8),(25,-30,10,1.2),(-41,-31,8,0.85),(4,-44,5,0.65),(9,29,6,0.95),(-68.2,5,12,1.4),(66,-15,9,1.0),(-12,34.4,8,1.0)]
bottom_normal=(0,-sin(radians(d.slope_angle)),-cos(radians(d.slope_angle)))
bottom_dimple_tools=[]
for x,y,diameter,depth in bottom_layout:
    z=cz-(y-cy+d.case_h/2)*tan(radians(d.slope_angle))
    bottom_dimple_tools.append(d.cap_tool((x,y,z),bottom_normal,diameter*d.cheese_size,depth*d.cheese_back_depth*bottom_depth_scale))
rear_before_decoration=rear
rear=rear-rear_cheese_tools-bottom_dimple_tools
print("Decoration:",len(d.cheese_front_tools),len(rear_cheese_tools),"bottom spherical scoops",len(bottom_dimple_tools))


# Constant-radius bore shared with the independent circular snap ring.
curved_bore_path=Pos(entry_face-cx,exit_face-cy,curve_plane_z-cz)*CenterArc((0,0),curve_R,-90+curve_overrun,-90-2*curve_overrun)
curve_origin=curved_bore_path.position_at(0)
curved_bore_profile=Plane(origin=curve_origin,x_dir=(0,0,1),z_dir=curved_bore_path.tangent_at(0))*Circle(curve_d/2)
curved_bore_tool=sweep(curved_bore_profile,curved_bore_path,is_frenet=False)
rear_before_bore=rear
rear-=curved_bore_tool
# Identify the two actual round-surface/bore lips; no extra blind scoops.
curve_lip_edges=[]
for edge in rear.edges():
    box=edge.bounding_box()
    mid=box.center()
    at_a=entry_face-cx-3<mid.X<entry_face-cx and abs(mid.Y-(curve_entry_y-cy))<0.5 and abs(mid.Z-(curve_plane_z-cz))<0.2 and box.size.X<1 and curve_d-0.5<box.size.Y<curve_d+0.6 and curve_d-0.2<box.size.Z<curve_d+0.2
    at_b=exit_face-cy-2<mid.Y<exit_face-cy and abs(mid.X-(curve_exit_x-cx))<0.5 and abs(mid.Z-(curve_plane_z-cz))<0.2 and box.size.Y<1 and curve_d-0.5<box.size.X<curve_d+0.6 and curve_d-0.2<box.size.Z<curve_d+0.2
    if at_a or at_b:
        curve_lip_edges.append(edge)
assert len(curve_lip_edges)==2,"Both circular bowl-to-bore lips must be present"
rear=fillet(curve_lip_edges,curve_lip_r)
print("Curved passage diameter",curve_d,"lip blend",curve_lip_r,"path length",curved_bore_path.length)

rear.color=srgb("#d6b79f")
publish("case_back",rear,"独立电池槽后壳",material="petg")
fit("joystick","mainboard",kind="nominal_contact",budget_mm=0.2,reason="Lowered OEM joystick flex now mates to CN2 beneath the PCB; overlap is confined to the connector")
