from src.dyscord.objects import ChannelImporter, Channel, TextChannel
from src.dyscord.utilities import Cache

from tests.objects.channel import samples


class TestImporter:

    def setup_method(self, test_method):
        cache = Cache()
        cache.clear()

    def teardown_method(self, test_method):
        pass

    def test_all_samples(self):

        for sample in samples.all:

            obj = ChannelImporter().ingest_raw_dict(sample)
            print(type(obj))
            assert isinstance(obj, Channel)

    def test_text_channel(self):

        input_data = samples.dev_guild_text

        channel = ChannelImporter().ingest_raw_dict(input_data)

        assert isinstance(channel, Channel)
        assert isinstance(channel, TextChannel)
        assert channel.name == 'general'
        assert channel.position == 6
