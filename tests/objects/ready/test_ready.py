from src.dyscord.objects import Ready
from tests.objects.ready import samples


def test_simple():
    data = samples.example_connect

    obj = Ready()
    obj.from_dict(data)
