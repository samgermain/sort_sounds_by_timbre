# This https://github.com/AudioCommons/timbral_models package predicts eight timbral characteristics:
#   hardness, depth, brightness, roughness, warmth, sharpness, booming, and reverberation.

# I sorted by each one of them.

from operator import itemgetter
from pathlib import Path

from timbral_models import timbral_extractor

path = Path(
    "/Users/sam/Documents/dev/sort_sounds_by_timbre/assets/transients_1/")
timbres = [
    {"file": file, "timbre": timbral_extractor(str(file))} for file in path.glob("*wav")
]
itemgetters = {key: itemgetter(key) for key in timbres[0]["timbre"]}

for timbre, get_timbre in itemgetters.items():
    print(f"Sorting by {timbre}")
    for item in sorted(timbres, key=lambda d: get_timbre(d["timbre"])):
        print(item["file"].name)
    print()
