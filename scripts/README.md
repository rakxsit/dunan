# scripts

## praat scripts
- save_intervals_to_wav_sound_files.praat : cut up long sound file into chunks, based on labeled intervals
- TextGridMaker.praat : creates TextGrids for all .wav files in a folder

## shell scripts
- extractchannel.sh : extract left (1) or right (channel) from stereo sound file
- runmfa.sh : run the Montreal Forced Aligner on all folders in a folder

## Jupyter notebooks
- geminates.ipynb : wrangles the geminates and their counterpart singletons
- geminate_silencecheck.ipynb : checks whether silences are actual silences or part of the stop
- burst.ipynb : detects and labels bursts