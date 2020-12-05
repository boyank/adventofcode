'''https://adventofcode.com/2020/day/4'''

import string

def passports(fname):
    passport = {}
    with open(fname) as f:
        for line in f:
            line = line.strip()
            if line:
                for field in line.split(' '):
                    key, value = field.split(':')
                    passport[key] = value
            else:
                yield passport
                passport = {}


def check_byr(passport):
    try:
        if 1920 <= int(passport['byr']) <= 2002:
            return True
    except ValueError:
        return False
    return False

def check_iyr(passport):
    try:
        if 2010 <= int(passport['iyr']) <= 2020:
            return True
    except ValueError:
        return False
    return False

def check_eyr(passport):
    try:
        if 2020 <= int(passport['eyr']) <= 2030:
            return True
    except ValueError:
        return False
    return False


def check_hgt(passport):
    if passport['hgt'].endswith(('in', 'cm')):
        try:
            height = int(passport['hgt'][:-2])
        except ValueError:
            return False
        else:
            units = passport['hgt'][-2:]
            if units == 'cm' and (150 <= height <= 193):
                    return True
            if units == 'in' and (59 <= height <= 76):
                    return True
    return False

def check_hcl(passport):
    if len(passport['hcl']) == 7 and passport['hcl'].startswith('#'):
        if all((char in string.ascii_lowercase or char in '0123456789') for char in passport['hcl'][1:]):
            return True
    return False

def check_ecl(passport):
    return passport['ecl'] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}

def check_pid(passport):
    return len(passport['pid']) == 9 and all(char in '0123456789' for char in passport['pid'])


required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'} # 'cid' filed is optional
checks = {'byr':check_byr, 'iyr':check_iyr, 'eyr':check_eyr, 'hgt':check_hgt, 'hcl':check_hcl, 'ecl':check_ecl, 'pid':check_pid}

part1_valid_passports = 0
part2_valid_passports = 0
for passport in passports('./advent2020/day04/passports.txt'):
    if all(field in passport.keys() for field in required_fields):
        part1_valid_passports += 1
        if all(check(passport) for check in checks.values()):
            part2_valid_passports += 1

# part1
print(f'Part 1 answer: {part1_valid_passports}') # correct answer 200

# part2
print(f'Part 2 answer: {part2_valid_passports}') # correct answer 116
