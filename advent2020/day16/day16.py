'''https://adventofcode.com/2020/day/16'''

import pytest
from pathlib import Path
from collections import namedtuple, defaultdict
from itertools import product
from operator import mul
from functools import reduce

FNAME_RULES = Path(__file__).with_name('rules.txt')
FNAME_TICKETS = Path(__file__).with_name('tickets.txt')

Rule = namedtuple('Rule', ['name', 'start', 'fend', 'sstart', 'end'])


def read_file(fname):
    with fname.open() as f:
        return f.read().splitlines()


def get_rules(content):
    rules = []
    for line in content:
        name, limits = line.split(': ')
        limits = [int(n) for item in limits.split(' or ') for n in item.split('-')]
        rules.append(Rule(name, *limits))
    return rules


def get_tickets(content):
    tickets =[tuple(int(field) for field in ticket.split(',')) for ticket in content ]
    return tickets


def is_valid(field, rules):
    for rule in rules:
        if (rule.start <= field <= rule.end) and not (rule.fend < field < rule.sstart):
            return True
    return False


def valid_tickets(tickets, rules):
    return [ticket for ticket in tickets if all(is_valid(field, rules) for field in ticket)]


def part1(tickets, rules):
    return sum(field for ticket in tickets 
                for field in ticket if not is_valid(field, rules))

def part2(ticket, tickets, rules):
    return reduce(mul, (ticket[field_id] for field_id, field_name
                                in field_order(tickets, rules).items()
                                if field_name.startswith('departure')), 1)


def field_order(tickets, rules):
    order = defaultdict(list)
    tickets = valid_tickets(tickets, rules)
    for field_id, values in enumerate(zip(*tickets)):
        for rule in rules:
            if all(is_valid(value, [rule,]) for value in values):
                order[field_id].append(rule.name)
    order = dict(sorted(order.items(), key=lambda x: len(x[1]), reverse=True))
    fields = {}
    for (key, value), value2 in zip(list(order.items())[:-1], list(order.values())[1:]):
        fields[key] = list(set(value) - set(value2))[0]
    return fields
                

@pytest.fixture
def test_rules():
    return """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50""".splitlines()


@pytest.mark.usefixture('test_rules')
def test_get_rules(test_rules):
    rules = get_rules(test_rules)
    assert rules == [Rule('class', 1, 3, 5, 7), Rule('row', 6, 11, 33, 44), Rule('seat', 13, 40, 45, 50)]


@pytest.fixture
def test_tickets():
    return """7,3,47
40,4,50
55,2,20
38,6,12""".splitlines()


@pytest.mark.usefixture('test_tickets')
def test_get_tickets(test_tickets):
    tickets = get_tickets(test_tickets)
    assert tickets == [(7, 3, 47), (40, 4, 50), (55, 2, 20), (38, 6, 12)]


@pytest.fixture
def test_fields():
    return {4:False, 55:False, 12:False, 7:True, 38:True}


@pytest.mark.usefixtures('test_fields', 'test_rules')
def test_isvalid(test_fields, test_rules):
    rules = get_rules(test_rules)
    for field, expected in test_fields.items():
        assert is_valid(field, rules) == expected


@pytest.mark.usefixtures('test_tickets', 'test_rules')
def test_part1(test_tickets, test_rules):
    tickets = get_tickets(test_tickets)
    rules = get_rules(test_rules)
    assert part1(tickets, rules) == 71

if __name__ == '__main__':
    rules = read_file(FNAME_RULES)
    rules = get_rules(rules)
    tickets = read_file(FNAME_TICKETS)
    tickets = get_tickets(tickets)
    my_ticket, *tickets = tickets
    print(f'Part1: {part1(tickets, rules)}')
    print(f'Part2: {part2(my_ticket, tickets, rules)}')