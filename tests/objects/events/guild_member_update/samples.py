import pathlib
import json

target = pathlib.Path(pathlib.Path(__file__).parent, 'raw_GUILD_MEMBER_UPDATE_samples.json')
with open(target) as fp:
    raw_guild_member_update_samples = json.load(fp)
