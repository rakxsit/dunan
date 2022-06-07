# data
- words.csv : all the words in the files
- phones.csv : all the phones in the files
- df_full.csv : all the target words looked at, containing geminates and their counterpart singletons
- df_vot.csv : subset of df_full where VOT can be detected by burst detector
- df_closdur.csv : subset of df_full where closure duration can be detected (no preceding silence)
- stop_targets.csv : all the target stops
- stop_duration_nooutliers.csv : all the target stops with outliers removed (where the silence is too long)
- target_phones_all.csv : all the target phones we are looking at
- target_phones.csv : looking at only k and t