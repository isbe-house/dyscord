from src.dyscord.objects import Presence

from . import samples


def test_basic_sample():
    for sample in samples.raw_presense_update_samples:
        data = sample['d']
        print(data)
        obj = Presence(data)

        assert isinstance(obj, Presence)
        assert obj.user.id == data['user']['id']
