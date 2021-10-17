from src.dyscord.objects import User, Snowflake


def test_user():

    x = User()

    print(x)

    x.from_dict(
        {'avatar': 'b437e9bd4b0e487a097c4538c6cdce3f',
         'discriminator': '2585',
         'id': str(Snowflake()),
         'username': 'TestUser',
         })

    assert x.username == 'TestUser'

    assert type(x.id) is Snowflake
