# Functionality

Takes a sound file, splits that sound file by transients (sound change), sorts those transients by timbre and outputs a midi file with multiple tracks that match the start time, end time, and sorting of the transients


# Instructions

To create a virtual environment and install dependencies

```
./setup.sh
source .env/bin/activate
```

Run the program by executing

`python src/main.py`

### ARGUMENTS

```
-i --input      required    Path to the input soundfile
-o --outfile                Name of the output midi file
-s --sr                     Sample rate of the soundfile if known
-m --midi                   Path to a .mid file that corresponds to the soundfile, if one exists
-h                          Help
```


# Limitations

- the sorting is currently not very good
- the transient separation is currently not very good. It's suggested to use a transient separated midi file, which you can get from Ableton buy right clicking on an audio track and selecting "Slice To New MIDI Track", and then right clicking on the midi track and selecting "Export MIDI Clip..."