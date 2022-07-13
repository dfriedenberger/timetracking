


def test_split_dataset():
    from .calculate import split_dataset
    data = []
    base , spents = split_dataset(data)
    assert base != None
    assert len(spents) == 0