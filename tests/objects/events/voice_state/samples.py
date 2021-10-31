import pathlib
import json

target = pathlib.Path(pathlib.Path(__file__).parent, 'raw_VOICE_STATE_UPDATE_samples.json')
with open(target) as fp:
    raw_voice_state_update_samples = json.load(fp)
