# data
- df_full.csv : contains all target segments for Dunan (geminates and singleton counterparts) 
- df_vot.csv : subset of df_full.csv that contains only segments with measureable VOT
- df_closdur.csv : subset of df_full.csv that contains only segments with a reliable closure duration (no silence beforehand)
- closure-vot-totalc.csv : inntersection of df_vot.csv and df_closdur.csv
- AMP_Dunan.csv : contains measures of f0 and intensity from MATLAB
- vot.csv : reshaping of AMP_Dunan.csv with VOT information
- f0-int.csv : reshaping of AMP_Dunan.csv with f0 and intensity