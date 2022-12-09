from collections import Counter
import pytest

def max_calories(data, n=1):
    return sorted(list(map(sum, data)), reverse=True)[:n]

def read_input(fname):
    with open(fname) as f:
        return [map(int, item.splitlines()) for item in f.read().split('\n\n')]


@pytest.fixture()
def sample_input1():
    data = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""
    return [map(int, item.splitlines()) for item in data.split('\n\n')]


def test_day01_1(sample_input1):
    print(sample_input1)
    assert  max_calories(sample_input1) == [24000]

data1 = read_input('./day01/input.txt')
print(max_calories(data1))
data1 = read_input('./day01/input.txt')
print(sum(max_calories(data1, 3)))
