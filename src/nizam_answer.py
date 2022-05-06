# This https://github.com/AudioCommons/timbral_models package predicts eight timbral characteristics: hardness, depth, brightness, roughness, warmth, sharpness, booming, and reverberation.

# I sorted by each one of them.

from timbral_models import timbral_extractor
from pathlib import Path
from operator import itemgetter

path = Path("sort-sounds-by-similarity-from-sound-file/assets/transients_1/")
timbres = [
    {"file": file, "timbre": timbral_extractor(str(file))} for file in path.glob("*wav")
]

itemgetters = {key: itemgetter(key) for key in timbres[0]["timbre"]}

for timbre, get_timbre in itemgetters.items():
    print(f"Sorting by {timbre}")
    for item in sorted(timbres, key=lambda d: get_timbre(d["timbre"])):
        print(item["file"].name)
    print()
