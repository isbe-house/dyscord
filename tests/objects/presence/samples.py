import json
import pathlib

simple_presence = {
    'user': {
        'id': '80351110224678912'
    },
    'guild_id': '804392362054910047',
    'status': 'online',
    'activities': [],
    'client_status': {
        'desktop': 'Windows'
    }
}


target = pathlib.Path(pathlib.Path(__file__).parent, 'raw_PRESENSE_UPDATE_samples.json')
with open(target) as fp:
    raw_presense_update_samples = json.load(fp)
