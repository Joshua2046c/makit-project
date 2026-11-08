support_t=param("lcd_support_height_mm",3.0)
rounding=param("lcd_support_edge_mm",0.6)
# OEM LCD glass outer size, not a replacement display model.
LCD_W=70.95
LCD_H=31.1
left=Pos(-30.2375,0)*RectangleRounded(10.475,LCD_H,rounding)
top=Pos(0,13.775)*RectangleRounded(LCD_W,3.55,rounding)
bottom=Pos(-17.7375,-13.775)*RectangleRounded(35.475,3.55,rounding)
support=extrude(left+top+bottom,support_t)
support.color=srgb("#e2c5ad")
publish("lcd_support",support,"屏幕C形支架",material="petg")
fit("display","mainboard",kind="nominal_contact",budget_mm=0.15,reason="OEM LCD flexible tail seated in FPC1 connector; glass and PCB bodies do not intersect")
