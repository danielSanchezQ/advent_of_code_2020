from itertools import chain


def validate_byr(byr):
    byr = int(byr)
    return 1920 <= byr <= 2002


def validate_iyr(iyr):
    iyr = int(iyr)
    return 2010 <= iyr <= 2020


def validate_eyr(eyr):
    eyr = int(eyr)
    return 2020 <= eyr <= 2030


def validate_hgt(hgt):
    if hgt.endswith("in"):
        hgt = int(hgt.replace("in", ""))
        return 59 <= hgt <= 76
    return 150 <= int(hgt.replace("cm", "")) <= 193


def validate_hcl(hcl):
    valid_chars = {
        "a", "b", "c", "d", "e", "f",
        *(str(c) for c in range(10))
    }
    return hcl[0] == "#" and set(hcl[1:]).issubset(valid_chars)


def validate_ecl(ecl):
    valid_ecl = {
        "amb", "blu", "brn", "gry", "grn", "hzl", "oth"
    }
    return ecl in valid_ecl


def validate_pid(pid):
    return len(pid) == 9 and pid.isdigit()


def validate_cid(cid):
    return True


fields = {
    "byr": validate_byr,
    "iyr": validate_iyr,
    "eyr": validate_eyr,
    "hgt": validate_hgt,
    "hcl": validate_hcl,
    "ecl": validate_ecl,
    "pid": validate_pid,
    "cid": validate_cid,
}


def parse_passports(f):
    passports_data = f.read().split("\n\n")
    passports_data = map(lambda x: x.replace("\n", " ").split(), passports_data)
    passports_data = (
        {k:v for k, v in map(lambda x: x.split(":"), passport)} for passport in passports_data
    )
    return passports_data


def validate_fields(mandatory, data_dict: dict):
    return set(data_dict.keys()).issuperset(mandatory)


def validate_value(key, value):
    return fields[key](value)


def validate_part_1(data_dict):
    mandatory = set(list(fields.keys())[:-1])
    return validate_fields(mandatory, data_dict)


def validate_part_2(data_dict):
    fields_validation = validate_part_1(data_dict)
    values_validation = all(validate_value(k, v) for k, v in data_dict.items())
    return fields_validation and values_validation


def count_valid(check_f, passports):
    return sum(1 for p in passports if check_f(p))


if __name__ == "__main__":
    with open("./input/advent4.txt") as f:
        passports = list(parse_passports(f))
        print(count_valid(validate_part_1, passports))
        print(count_valid(validate_part_2, passports))