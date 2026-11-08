d=part("front_panel")
edge_r=param("black_face_corner_mm",3.3)
face=extrude(RectangleRounded(d.mask_w,d.mask_h,edge_r),d.mask_t)
mx,my=d.mask_xy
lx,ly=d.lcd_xy
face-=Pos(lx-mx,ly-my,-0.1)*extrude(RectangleRounded(d.window_w,d.window_h,0.9),d.mask_t+0.2)
for i,(x,y) in enumerate(d.key_centres[:3]):
    if i==1:
        face-=Pos(x-mx,y-my,-0.1)*extrude(d.key_b_cut,d.mask_t+0.2)
    else:
        dia=[8.6,0,11.1][i]
        face-=Pos(x-mx,y-my,d.mask_t/2)*Cylinder(dia/2,d.mask_t+0.2)
face-=Pos(-49.525-mx,0.75-my,d.mask_t/2)*Cylinder(d.joy_hole/2,d.mask_t+0.2)
for x,y in d.mic_centres:
    face-=Pos(x-mx,y-my,d.mask_t/2)*Cylinder(d.mic_hole/2,d.mask_t+0.2)
# Smaller blind bowls in the bezel margins; optical and acoustic holes stay clear.
bezel_pit_depth=param("bezel_cheese_depth_scale",1.0)
bezel_layout=[(-17,25,5,0.35),(14,24,7,0.45),(-44,23,4,0.3),(53,23,4,0.3),(-54,-17,4,0.3)]
for x,y,diameter,depth in bezel_layout:
    cutter=d.cap_tool((x,y,3.0),(0,0,1),diameter*d.cheese_size,depth*bezel_pit_depth)
    face-=Pos(d.cx-mx,d.cy-my,-d.body_depth)*cutter

face.color=srgb("#141719")
publish("black_face",face,"黑色屏幕面板",material="petg")
