from range import Range
from cover import Cover

range1 = Range(4, 5)
range2 = Range(10, 3)
range3 = Range(1, 4)
range4 = Range(6, 2)
range5 = Range(7, 10)


def run_tests():
    assert not Range(0, 0)
    assert Range(0, 0) == Range.empty_set
    assert Range(4, 0) == Range.empty_set
    assert Range(2, 3) == Range(2, 3)
    assert range1.cover(range1) == Cover(Range.empty_set, range1, Range.empty_set), range1.cover(range1)
    assert range1.cover(range2) == Cover(range1, Range(0, 0), range2)
    assert range2.cover(range1) == Cover(range1, Range(0, 0), range2)
    assert range2.cover(range5) == Cover(Range(7, 3), Range(10, 3), Range(13, 4))
    assert range5.cover(range2) == Cover(Range(7, 3), Range(10, 3), Range(13, 4))
    assert range1.cover(range3) == Cover(Range(1, 3), Range(4, 1), Range(5, 4)), range1.cover(range3)
    assert range3.cover(range1) == Cover(Range(1, 3), Range(4, 1), Range(5, 4)), range1.cover(range3)




if __name__ == '__main__':
    run_tests()