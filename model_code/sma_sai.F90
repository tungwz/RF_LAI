PROGRAM merge_var

 ! gfortran -g -fbounds-check -o sma_merge sma_sai.F90 -I/usr/include -lnetcdf -lnetcdff

 USE netcdf

 IMPLICIT NONE

 integer , parameter :: nx = 1200, ny = 1200
 integer , parameter :: r8 = selected_real_kind(12)
 real(r8), parameter :: delta = 1./240._r8
 real(r8), parameter :: sairtn= 0.5
 real(r8), parameter :: saimin= 1
 real(r8), parameter :: laimax= 5.5

 real(r8), dimension(12  ) :: lai_diff
 integer , dimension(12  ) :: mon
 real(r8), dimension(1200) :: lat, lon, latn, lats, lonw, lone
 integer , dimension(1200, 1200) :: lc_
 integer , dimension(1200, 1200, 22) :: lc
 real(r8), dimension(1200, 1200, 12) :: lai, sai
 real(r8), dimension(1200, 1200, 12) :: lai_

 integer :: ncid, mon_id, lat_id, lon_id, lai_id, lc_id, sai_id
 integer :: latn_id, lats_id, lonw_id, lone_id
 integer :: lat_dimid, lon_dimid, mon_dimid

 integer :: iloop
 integer :: ei, ej, si, sj, imon, year, argn, ii, lc_year, ix, iy, ireg
 integer :: reglat,reglon,reglon_,sreglat,sreglon,ereglat,ereglon
 integer :: XY3D(3), reg(4)

 REAL(r8), dimension(12) :: saiini, saiini1, laidiff

 real(r8):: saimin1, saires, sum_judg, x1, x2
 character(len=256) :: reg1, reg2, reg3, reg4
 character(len=256) :: cmon, lndname
 character(len=4  ) :: iyear, cyear

 logical  :: fileExists

 argn = IARGC()
 IF (argn > 0) THEN
    CALL getarg(1, iyear)
 ENDIF

 sreglat =   90
 ereglat =  -90
 sreglon = -180
 ereglon =  180

 DO imon = 1, 12
    mon(imon) = imon
 ENDDO

 !write(iyear, "(i4.4)") year

 DO reglat = sreglat, ereglat, -5
    DO reglon_ = sreglon, ereglon, 5

       reglon = reglon_
       IF (reglon_ > 180) reglon = reglon_ - 360
       reg(1) = reglat
       reg(2) = reglon
       reg(3) = reglat - 5
       reg(4) = reglon + 5

       write(reg1, "(i4)") reg(1)
       write(reg2, "(i4)") reg(2)
       write(reg3, "(i4)") reg(3)
       write(reg4, "(i4)") reg(4)

       lndname = '/tera10/yuanhua/dongwz/mksrf/lc_5x5/RG_'//TRIM(adjustL(reg1))//'_'//&
                    TRIM(adjustL(reg2))//'_'//TRIM(adjustL(reg3))//'_'//TRIM(adjustL(reg4))//&
                    '.LC_'//TRIM(iyear)//'.nc'
       inquire (file=lndname, exist=fileExists)
       IF (.not. fileExists) CYCLE

       DO lc_year = 0,21
          write(cyear, "(i4)") (lc_year+2001)
          ! print*, cyear

          lndname = '/tera10/yuanhua/dongwz/mksrf/lc_5x5/RG_'//TRIM(adjustL(reg1))//'_'//&
                    TRIM(adjustL(reg2))//'_'//TRIM(adjustL(reg3))//'_'//TRIM(adjustL(reg4))//&
                    '.LC_'//TRIM(cyear)//'.nc'

          CALL nccheck( nf90_open(trim(lndname), nf90_nowrite    , ncid) )

          CALL nccheck( nf90_inq_varid(ncid, "landtype", lc_id              ) )
          CALL nccheck( nf90_get_var  (ncid, lc_id     , lc(:,:,(lc_year+1))) )
          CALL nccheck( nf90_close(ncid) )
       ENDDO

       lc_ = 0  ! Initialize lc_ array to 0

       ! Set elements of lc_ to 1 based on conditions
       lc_ = merge(1, lc_, any(lc <= 5, dim=3) .or. any(lc == 13, dim=3))
       IF (reg(1)==40 .and. reg(2)==-80 .and. reg(3)==35 .and. reg(4)==-75) THEN
          lc_(835,141) = 1
       ENDIF

       IF (reg(1)==45 .and. reg(2)==-95 .and. reg(3)==40 .and. reg(4)==-90) THEN
          lc_(435,1) = 1
       ENDIF

       IF (reg(1)==65 .and. reg(2)==20 .and. reg(3)==60 .and. reg(4)==25) THEN
          lc_(1186,1160) = 1
       ENDIF

       DO ireg=1, 1200
          lat(ireg) = reg(1) - (ireg-1)*delta - delta/2
          lon(ireg) = reglon + (ireg-1)*delta + delta/2
       ENDDO

       latn(:) = lat + delta/2
       lats(:) = lat - delta/2
       lone(:) = lon + delta/2
       lonw(:) = lon - delta/2

       lai(:,:,:) = 0.
       DO imon = 1, 12
          write(cmon, '(i2.2)') imon

          lndname = './LAI_'//trim(iyear)//'/RG_'//TRIM(adjustL(reg1))//'_'//&
                    TRIM(adjustL(reg2))//'_'//TRIM(adjustL(reg3))//'_'//TRIM(adjustL(reg4))//&
                    '.UrbLAI_'//trim(iyear)//'_'//trim(cmon)//'.nc'

          inquire (file=lndname, exist=fileExists)
          IF (fileExists) THEN
             print*, lndname
             CALL nccheck( nf90_open(trim(lndname), nf90_nowrite    , ncid       ) )

             CALL nccheck( nf90_inq_varid(ncid, "LAI" , lai_id       ) )
             CALL nccheck( nf90_get_var  (ncid, lai_id, lai_(:,:,imon)) )

             WHERE (lc_==0) lai_(:,:,imon)=0

             IF (imon == 12) THEN
                ! CALL nccheck( nf90_inq_varid(ncid, "lat" , lat_id) )
                ! CALL nccheck( nf90_get_var  (ncid, lat_id, lat   ) )
                ! CALL nccheck( nf90_inq_varid(ncid, "lon" , lon_id) )
                ! CALL nccheck( nf90_get_var  (ncid, lon_id, lon   ) )

                lai(:,:,1) = (lai_(:,:,1)+lai_(:,:,2))/2
                DO ii = 2, 11
                   lai(:,:,ii) = (lai_(:,:,ii-1)+lai_(:,:,ii)+lai_(:,:,ii+1))/3
                ENDDO
                lai(:,:,12) = (lai_(:,:,11)+lai_(:,:,12))/2
             ENDIF

             CALL nccheck( nf90_close(ncid) )
             ! WHERE (htop>5 .and. htop/=13) lai(:,:,imon)=0
             ! WHERE (htop==0) lai_(:,:,imon)=0
           ENDIF
       ENDDO

       DO ix=1,1200
          DO iy=1,1200
             IF ( maxval(lai(ix,iy,:)) > 0 ) THEN
                saimin1   = saimin*maxval(lai(ix,iy,:))
                saimin1   = saimin1/laimax
                saiini (:)= 0.
                saiini1(:)= saiini

                DO imon = 1, 12
                   saiini1(imon) = saimin
                ENDDO

                laidiff(1) = lai(ix,iy,12)-lai(ix,iy,1)
                DO imon = 1, 11
                   laidiff(imon+1) = lai(ix,iy,imon)-lai(ix,iy,imon+1)
                ENDDO

                WHERE(laidiff<0.) laidiff=0.

                iloop = 1
                DO WHILE (iloop < 13)
                   saires = sairtn*saiini1(mod((iloop+10),12)+1)
                   x1     = saires+laidiff(iloop)*0.5
                   x2     = saimin1
                   saiini(iloop) = max(x1,x2)
                   sai(ix,iy,iloop) = saiini(iloop)

                   iloop = iloop + 1
                   IF (iloop == 13) THEN
                      sum_judg = abs(sum(saiini-saiini1))
                      IF (sum_judg > 1e-6) THEN
                         iloop = 1
                         saiini1(:) = saiini(:)
                      ENDIF
                   ENDIF
                ENDDO
             ELSE
                sai(ix,iy,:) = 0.
             ENDIF
          ENDDO
       ENDDO

       IF (count(sai>3) > 0) THEN
          WHERE(sai>3) sai = 3
       ENDIF

       IF (fileExists) THEN
          lndname = './urban_lai_5x5/RG_'//TRIM(adjustL(reg1))//'_'//&
                    TRIM(adjustL(reg2))//'_'//TRIM(adjustL(reg3))//'_'//TRIM(adjustL(reg4))//'.URBLAI_'//trim(iyear)//'.nc'

          CALL nccheck( nf90_create (trim(lndname)  , NF90_NETCDF4, ncid) )

          CALL nccheck( nf90_def_dim(ncid, "mon"    , 12, mon_dimid   ) )
          CALL nccheck( nf90_def_dim(ncid, "lat"    , ny, lat_dimid   ) )
          CALL nccheck( nf90_def_dim(ncid, "lon"    , nx, lon_dimid   ) )

          CALL nccheck( nf90_def_var(ncid, "mon"    , NF90_INT   , mon_dimid, mon_id , deflate_level=6) )
          CALL nccheck( nf90_def_var(ncid, "lat"    , NF90_DOUBLE, lat_dimid, lat_id , deflate_level=6) )
          CALL nccheck( nf90_def_var(ncid, "lon"    , NF90_DOUBLE, lon_dimid, lon_id , deflate_level=6) )
         !  CALL nccheck( nf90_def_var(ncid, "lat_n"  , NF90_DOUBLE, lat_dimid, latn_id, deflate_level=6) )
         !  CALL nccheck( nf90_def_var(ncid, "lon_w"  , NF90_DOUBLE, lon_dimid, lonw_id, deflate_level=6) )
         !  CALL nccheck( nf90_def_var(ncid, "lat_s"  , NF90_DOUBLE, lat_dimid, lats_id, deflate_level=6) )
         !  CALL nccheck( nf90_def_var(ncid, "lon_e"  , NF90_DOUBLE, lon_dimid, lone_id, deflate_level=6) )

          CALL nccheck( nf90_put_att(ncid, mon_id, "long_name", "Month of year"   ) )
          CALL nccheck( nf90_put_att(ncid, mon_id, "units"    , "month"           ) )
          ! CALL nccheck( nf90_put_att(ncid, lat_id, "long_name", "Latitude"        ) )
          ! CALL nccheck( nf90_put_att(ncid, lat_id, "units"    , "degrees_north"   ) )
          ! CALL nccheck( nf90_put_att(ncid, lon_id, "long_name", "Longitude"       ) )
          ! CALL nccheck( nf90_put_att(ncid, lon_id, "units"    , "degrees_east"    ) )

          CALL nccheck( nf90_put_att(ncid, lat_id , "standard_name", "latitude"     ) )
          CALL nccheck( nf90_put_att(ncid, lat_id , "long_name", "Latitude at grid center"     ) )
          CALL nccheck( nf90_put_att(ncid, lat_id , "units"    , "degrees_north"                                 ) )
         !  CALL nccheck( nf90_put_att(ncid, latn_id, "long_name", "coordinate latitude at the north edge of grid" ) )
         !  CALL nccheck( nf90_put_att(ncid, latn_id, "units"    , "degrees_north"                                 ) )
         !  CALL nccheck( nf90_put_att(ncid, lats_id, "long_name", "coordinate latitude at the sourth edge of grid") )
         !  CALL nccheck( nf90_put_att(ncid, lats_id, "units"    , "degrees_north"                                 ) )
          CALL nccheck( nf90_put_att(ncid, lon_id , "standard_name", "longitude"    ) )
          CALL nccheck( nf90_put_att(ncid, lon_id , "long_name", "Longitude at grid center"    ) )
          CALL nccheck( nf90_put_att(ncid, lon_id , "units"    , "degrees_east"                                  ) )
         !  CALL nccheck( nf90_put_att(ncid, lonw_id, "long_name", "coordinate longitude at the west of grid"      ) )
         !  CALL nccheck( nf90_put_att(ncid, lonw_id, "units"    , "degrees_east"                                  ) )
         !  CALL nccheck( nf90_put_att(ncid, lone_id, "long_name", "coordinate longitude at the east of grid"      ) )
         !  CALL nccheck( nf90_put_att(ncid, lone_id, "units"    , "degrees_east"                                  ) )

          XY3D = (/lon_dimid, lat_dimid, mon_dimid/)

          CALL nccheck( nf90_def_var(ncid, "URBAN_TREE_LAI" , NF90_DOUBLE   , XY3D, lai_id, deflate_level=6) )
          ! CALL nccheck( nf90_def_var(ncid, "URBAN_TREE_LAI" , NF90_INT      , XY3D, lai_id, deflate_level=6) )
          CALL nccheck( nf90_put_att(ncid, lai_id           , "long_name"   , "Urban tree monthly lai"     ) )
          CALL nccheck( nf90_put_att(ncid, lai_id           , "units"       , "m^2/m^2"                    ) )
          CALL nccheck( nf90_put_att(ncid, lai_id           , "_FillValue"  , -999._r8                       ) )
          ! CALL nccheck( nf90_put_att(ncid, lai_id           , "scale_factor", 0.000001                     ) )

          CALL nccheck( nf90_def_var(ncid, "URBAN_TREE_SAI" , NF90_DOUBLE   , XY3D, sai_id, deflate_level=6) )
          ! CALL nccheck( nf90_def_var(ncid, "URBAN_TREE_SAI" , NF90_INT      , XY3D, sai_id, deflate_level=6) )
          CALL nccheck( nf90_put_att(ncid, sai_id           , "long_name"   , "Urban tree monthly sai"     ) )
          CALL nccheck( nf90_put_att(ncid, sai_id           , "units"       , "m^2/m^2"                    ) )
          CALL nccheck( nf90_put_att(ncid, sai_id           , "_FillValue"  , -999._r8                       ) )
          ! CALL nccheck( nf90_put_att(ncid, sai_id           , "scale_factor", 0.000001                     ) )

          CALL nccheck( nf90_inq_varid(ncid, "mon" , mon_id) )
          CALL nccheck( nf90_put_var  (ncid, mon_id, mon   ) )
          CALL nccheck( nf90_inq_varid(ncid, "lat" , lat_id) )
          CALL nccheck( nf90_put_var  (ncid, lat_id, lat   ) )
          CALL nccheck( nf90_inq_varid(ncid, "lon" , lon_id) )
          CALL nccheck( nf90_put_var  (ncid, lon_id, lon   ) )

         !  CALL nccheck( nf90_inq_varid(ncid, "lat_n", latn_id) )
         !  CALL nccheck( nf90_put_var  (ncid, latn_id, latn   ) )
         !  CALL nccheck( nf90_inq_varid(ncid, "lon_w", lonw_id) )
         !  CALL nccheck( nf90_put_var  (ncid, lonw_id, lonw   ) )
         !  CALL nccheck( nf90_inq_varid(ncid, "lat_s", lats_id) )
         !  CALL nccheck( nf90_put_var  (ncid, lats_id, lats   ) )
         !  CALL nccheck( nf90_inq_varid(ncid, "lon_e", lone_id) )
         !  CALL nccheck( nf90_put_var  (ncid, lone_id, lone   ) )

          CALL nccheck( nf90_inq_varid(ncid, "URBAN_TREE_LAI", lai_id) )
          CALL nccheck( nf90_put_var  (ncid, lai_id          , lai   ) )

          CALL nccheck( nf90_inq_varid(ncid, "URBAN_TREE_SAI", sai_id) )
          CALL nccheck( nf90_put_var  (ncid, sai_id          , sai   ) )

          CALL nccheck( nf90_put_att(ncid, NF90_GLOBAL, 'Title'  , 'Urban tree LAI and SAI data') )
          CALL nccheck( nf90_put_att(ncid, NF90_GLOBAL, 'Resolution'  , '15 seconds, 0.0041667 degree, 1200x1200 (lonxlat) &
                regional') )
          CALL nccheck( nf90_put_att(ncid, NF90_GLOBAL, 'Coordinate'  , 'Geographic, degrees longitude and latitude') )
          CALL nccheck( nf90_put_att(ncid, NF90_GLOBAL, 'Authors', 'Yongjiu Dai group at Sun Yat-sen University' ) )
          CALL nccheck( nf90_put_att(ncid, NF90_GLOBAL, 'Address', 'School of Atmospheric Sciences, &
                                     Sun Yat-sen University, Zhuhai, China') )
          CALL nccheck( nf90_put_att(ncid, NF90_GLOBAL, 'Contact', &
          'Wenzong Dong (dongwz@mail2.sysu.edu.cn); Hua Yuan (yuanh25@mail.sysu.edu.cn)') )

          CALL nccheck( nf90_close( ncid) )
       ENDIF
    ENDDO
 ENDDO

CONTAINS
  SUBROUTINE nccheck(status)
      INTEGER, INTENT(IN) :: status

      IF (status /= nf90_noerr) THEN
         print *, trim(nf90_strerror(status))
         stop 2
      END IF
   END SUBROUTINE nccheck
END PROGRAM merge_var
