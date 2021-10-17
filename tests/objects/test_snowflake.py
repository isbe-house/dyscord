import datetime

from src.dyscord.objects import Snowflake


def test_create_snowflake():

    s = Snowflake()

    print(s)


def test_sample_snowflakes():

    samples = [
        888187109867921429,
        888985357171961896,
        '888985357171961896',
        Snowflake(888187109867921429),
    ]

    for sample in samples:

        s = Snowflake(sample)
        print(s)

        print(f'Timestamp: {datetime.datetime.fromtimestamp(s.timestamp)}')
        print(s.timestamp)
        print(s.worker_id)
        print(s.process_id)
        print(s.increment)

        assert type(s) is Snowflake


def test_equality():

    obj = Snowflake(888187109867921429)
    assert obj == 888187109867921429
    assert obj == '888187109867921429'
    assert obj == obj
