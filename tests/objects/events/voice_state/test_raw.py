from src.dyscord.objects.events import VoiceState

from . import samples


def test_instance():

    obj = VoiceState()
    assert isinstance(obj, VoiceState)


def test_raw_samples():

    for sample in samples.raw_voice_state_update_samples:
        data = sample['d']
        print(data)
        obj = VoiceState(data)
        for key in data:
            if key == 'hoisted_role':
                continue
            assert hasattr(obj, key)
            assert (getattr(obj, key) is not None) or data[key] is None
