from butter_cup.flower import flower
from butter_cup.daisy import daisy


def test_flower():
    assert 'daisy' == daisy()
    assert "       daffodil" == flower(15)
    assert "daffodil" == flower(5)