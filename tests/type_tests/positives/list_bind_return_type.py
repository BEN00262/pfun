from zen import List


def test() -> List[int]:
    return List(i for i in (1, 2, 3)).and_then(lambda x: List([x**2]))