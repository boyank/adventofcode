import pytest
import day11

@pytest.fixture
def input_data():
    data = day11.get_data(day11.FNAME_TEST)
    data = list(data)
    return zip(data[:-1], data[1:])


@pytest.fixture
def input_data2():
    data = day11.get_data(day11.FNAME_TEST.with_name('test_input2.txt'))
    return next(data)
    

@pytest.mark.usefixtures('input_data')
def test_get_data(input_data):
    data, expected = next(input_data)
    expected = ['L.LL.LL.LL', 'LLLLLLL.LL', 'L.L.L..L..',
                'LLLL.LL.LL', 'L.LL.LL.LL', 'L.LLLLL.LL',
                '..L.L.....', 'LLLLLLLLLL', 'L.LLLLLL.L',
                'L.LLLLL.LL']
    assert data == expected


@pytest.mark.usefixtures('input_data')
def test_do_round(input_data):
    for plan, expected in input_data:
        plan = [list(row) for row in plan]
        assert day11.do_round(plan) == expected


@pytest.mark.usefixtures('input_data')
def test_count(input_data):
    data = day11.get_data(day11.FNAME_TEST)
    plan = next(data)
    assert day11.process(plan) == 37


@pytest.mark.usefixtures('input_data2')
def test_check_cols_l1(input_data2):
    assert day11.check_col(input_data2, 1, 2, len(input_data2), len(input_data2[0]), level=1) == 0


@pytest.mark.usefixtures('input_data2')
def test_check_rows_l1(input_data2):
    assert day11.check_row(input_data2, 1, 2, len(input_data2), len(input_data2[0]), level=1) == 1


@pytest.mark.usefixtures('input_data2')
def test_check_diagonals_l1(input_data2):
    assert day11.check_diagonals(input_data2, 1, 2, len(input_data2), len(input_data2[0]), level=1) == 1


@pytest.mark.usefixtures('input_data2')
def test_check_cols(input_data2):
    assert day11.check_col(input_data2, 4, 3, len(input_data2), len(input_data2[0]), level=0) == 2


@pytest.mark.usefixtures('input_data2')
def test_check_rows(input_data2):
    assert day11.check_row(input_data2, 4, 3, len(input_data2), len(input_data2[0]), level=0) == 2


@pytest.mark.usefixtures('input_data2')
def test_check_diagonals(input_data2):
    assert day11.check_diagonals(input_data2, 4, 3, len(input_data2), len(input_data2[0]), level=0) == 4


def test_check_cols3():
    data = day11.get_data(day11.FNAME_TEST)
    next(data)
    plan = next(data)
    assert day11.check_col(plan, 0, 6, len(plan), len(plan), level=0) == 1


def test_check_rows3():
    data = day11.get_data(day11.FNAME_TEST)
    next(data)
    plan = next(data)
    assert day11.check_row(plan, 0, 0, len(plan), len(plan), level=0) == 1


def test_check_diagonals3():
    data = day11.get_data(day11.FNAME_TEST)
    next(data)
    plan = next(data)
    assert day11.check_diagonals(plan, 0, 0, len(plan), len(plan), level=0) == 1


@pytest.mark.usefixtures('input_data2')
def test_check_occupied(input_data2):
    assert day11.check_occupied(input_data2, 4, 3, level=0) == 8


def test_do_round_level0():
    data = day11.get_data(day11.FNAME_TEST)
    plan = next(data)
    assert day11.process(plan, crowd=4, level=0) == 26