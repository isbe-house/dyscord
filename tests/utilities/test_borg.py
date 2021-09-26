from src.simple_discord.utilities import Borg


class foo(Borg):
    def __init__(self, value):
        super().__init__()
        self.value = value


def test_simple_borg():

    x = foo(1)
    y = foo(2)

    assert y.value == 2
    assert x.value == 2
    assert x is not y

    x.value = 5

    assert x.value == 5
    assert y.value == 5
    assert x is not y
