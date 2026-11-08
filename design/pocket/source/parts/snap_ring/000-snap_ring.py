b=part("case_back")
from math import sin,cos,radians
R=b.curve_R
width=param("lap_ring_radial_width_mm",3.0)
height=param("lap_ring_thickness_mm",2.4)
section_r=param("lap_ring_edge_radius_mm",0.5)
gap=param("lap_ring_tongue_gap_mm",0.4)
joint_angle=param("lap_ring_joint_sector_deg",40.0)
tip_angle=param("lap_ring_tip_angle_deg",15.0)
root_overlap=param("lap_ring_root_overlap_deg",0.5)
groove_w=param("lap_ring_face_groove_width_mm",0.35)
groove_depth=param("lap_ring_face_groove_depth_mm",0.25)
hook_angle=param("lap_ring_hook_angle_deg",-10.0)
hook_tip=param("lap_ring_hook_outer_offset_mm",0.45)
hook_root=param("lap_ring_hook_root_offset_mm",0.55)
hook_length=param("lap_ring_hook_length_mm",1.35)
hook_ramp=param("lap_ring_hook_ramp_mm",0.5)
latch_clearance=param("lap_ring_keeper_clearance_mm",0.25)
hook_round=param("lap_ring_hook_edge_radius_mm",0.12)
lane=(width-gap)/2
inner_R=R-(gap+lane)/2
outer_R=R+(gap+lane)/2
notch_inner=gap/2-0.08
notch_outer=hook_tip+latch_clearance
assert lane>=1.2 and width/2-notch_outer>=0.8-1e-7
assert 0<section_r<lane/2 and height>2*section_r and groove_depth<height/3
def arc_band(radius,w,start,span):
    path=CenterArc((0,0),radius,start,span)
    u=radians(start)
    profile=Plane(origin=path.position_at(0),x_dir=(cos(u),sin(u),0),z_dir=path.tangent_at(0))*RectangleRounded(w,height,section_r)
    return sweep(profile,path,is_frenet=False)
body=arc_band(R,width,joint_angle/2,360-joint_angle)
groove=Circle(R+groove_w/2)-Circle(R-groove_w/2)
body-=Pos(0,0,height/2-groove_depth)*extrude(groove,groove_depth+0.15)+Pos(0,0,-height/2-0.15)*extrude(groove,groove_depth+0.15)
outer=arc_band(outer_R,lane,-joint_angle/2-root_overlap,joint_angle/2+root_overlap+tip_angle)
inner=arc_band(inner_R,lane,-tip_angle,tip_angle+joint_angle/2+root_overlap)
frame=Rot(0,0,hook_angle)*Pos(R,0,0)
window=frame*Pos((notch_inner+notch_outer)/2,0,0)*Box(notch_outer-notch_inner,hook_length+2*0.3,height+0.4)
outer-=window
hook_h=height-0.4
hook=Pos(0,0,-hook_h/2)*extrude(Polygon((-hook_root,-hook_length/2),(gap/4,-hook_length/2),(hook_tip,-hook_length/2+hook_ramp),(hook_tip,hook_length/2),(-hook_root,hook_length/2),align=None),hook_h)
hook=fillet(hook.edges().filter_by(Axis.Z),hook_round)
hook=frame*hook
inner+=hook
ring=body+outer+inner
def volume_of(shape):
    if shape is None:return 0
    if hasattr(shape,"volume"):return shape.volume
    return sum(s.volume for s in shape)
assert ring.is_valid and len(ring.solids())==1
assert volume_of(inner&outer)<1e-6
keeper_wall=width/2-notch_outer
catch_engagement=hook_tip-gap/2
flex_length=inner_R*radians(joint_angle/2-hook_angle)
connections={"snap_ring_mount":"free: flat constant-radius integral ring threaded through R18 bore with elastic opening","integral_ring_snap":"free: staggered radial lap tongues and inward-releasable catch"}
print("Flat lap ring OD ID",2*R+width,2*R-width,"section",width,height,"keeper wall",keeper_wall,"engagement",catch_engagement)
ring.color=srgb("#b6b15c")
publish("snap_ring",ring,"PA11扁平搭接挂环",material="nylon")
