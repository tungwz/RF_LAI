begin

 glass = addfile("../nc_data/Global_GLASS_LAI_0.5deg_2020.nc", "r")
 rf    = addfile("../nc_data/Global_Urban_LAI_2020_v61.nc","r")

 lc = 5

 glass_lai_= glass->GLASS_LAI(:,:,:)
 glass_lai_= where(glass_lai_.ne.glass_lai_, -999., glass_lai_)
 glass_lai = dim_avg_n_Wrap(glass_lai_,0)
 glass_lai!0="lat"
 glass_lai!1="lon"
 glass_lai&lat=glass_lai_&lat
 glass_lai&lon=glass_lai_&lon
 glass_lai@_FillValue=-999.

 rf_lai    = dim_avg_n_Wrap(rf->URBAN_TREE_LAI(lc,:,:,:),0)
 rf_lai    = where(rf_lai .eq.0, -999., rf_lai)

 cmap = read_colormap_file("colormap/12colors.rgb")

 igbp_tile   = (/"NET","BET","NDT","BDT","MF","Urban","Grid_tree"/)
 string_tile = (/"(A)","(B)","(C)","(D)","(E)","(F)","(G)","(H)","(I)","(J)","(K)","(L)","(M)","(N)","(O)"/)

 plot = new(2,graphic)
 wks  = gsn_open_wks("pdf", "Fig7AB")

 imod = 0
 irf  = 0
do i=0,0
 res                      = True
 res@gsnMaximize          = True
 res@gsnDraw              = False              ; don't draw
 res@gsnFrame             = False              ; don't advance frame

 res@cnLevelSelectionMode = "ExplicitLevels"
 res@gsnLeftStringFontHeightF = 0.022

 res@lbLabelFontHeightF   = 0.02
 res@cnLevels             = (/"0.1","0.5","1","1.5","2","2.5","3","3.5","4","5","6"/)

 res@cnFillOn         = True
 res@cnLinesOn        = False
 res@cnLineLabelsOn   = False
 res@lbLabelBarOn     = True
 res@cnFillMode       = "CellFill"
 res@cnFillColors     = cmap

 res@gsnLeftString    = "  Annual mean GLASS v6 Grid LAI"
 res@gsnRightString   = " "
 res@tiMainString     = ""

 res@tmYROn           = False     ; Turn off right and top tick marks
 res@tmXTOn           = False     ; Turn off right and top tick marks

 plot(i*3) = gsn_csm_contour_map(wks, glass_lai(::-1,:), res)

 res@gsnLeftString    = "  Annual mean RF Urban Tree LAI"
 res@cnLevels             = (/"0.1","0.5","1","1.5","2","2.5","3","3.5","4","5","6"/)
 plot(i*3+1) = gsn_csm_contour_map(wks, rf_lai(::-1,:), res)

 imod = imod + 1
 irf  = irf  + 1
end do
 pres                 = True
 gsn_panel(wks, plot, (/1,2/), pres)

end
