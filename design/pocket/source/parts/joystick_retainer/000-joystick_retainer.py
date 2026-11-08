d=part("front_panel")
from screwjoint import make_screw_joint_v1
width=param("retainer_width_mm",29.0)
height=param("retainer_height_mm",24.4)
thickness=param("retainer_thickness_mm",2.0)
body_clear_w=param("retainer_body_clearance_width_mm",19.8)
body_clear_h=param("retainer_body_clearance_height_mm",17.8)
engagement=param("retainer_screw_engagement_mm",3.5)
pad_gap=param("retainer_pad_compressed_gap_mm",0.3)
cx,cy,cz=d.case_origin
rx,ry=d.local_xy((-50.875,0.5))
jx,jy=d.local_xy((-49.475,0.0))
bottom=-3.825-cz+pad_gap
retainer=Pos(rx,ry,bottom)*extrude(RectangleRounded(width,height,2.0),thickness)
retainer-=Pos(jx,jy,bottom-0.1)*extrude(RectangleRounded(body_clear_w,body_clear_h,0.7),thickness+0.2)
bosses=[]
cuts=[]
mount_bom=[]
for i,(x,y) in enumerate([(-62.3,-6.2),(-62.3,7.0)]):
    j=make_screw_joint_v1(size="M2",at=Pos(x-cx,y-cy,bottom+thickness),through=[(retainer,thickness)],seat="countersink",engage_depth=engagement,into=d.rear_blank,material="PETG",label="joystick-retainer:"+str(i))
    retainer-=j.through_cuts[0]
    bosses.append(j.bosses)
    cuts.append(j.engage_cuts)
    mount_bom.extend(j.bom)
    publish("retainer_screw_"+str(i+1),Pos(cx,cy,cz)*j.hardware,"摇杆压框沉头螺钉",material="stainless_steel",role="fastener")
    print("Retainer",i,j.screw_length_mm,j.boss_length_mm,j.head_land_mm,j.notes)
retainer.color=srgb("#e2c5ad")
publish("joystick_retainer",retainer,"摇杆独立压框",material="petg")
