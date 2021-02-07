"""https://adventofcode.com/2020"""
from argparse import ArgumentParser
from time import time
from re import match


class Day1:
    """https://adventofcode.com/2020/day/1"""
    def __init__(self, filename="input/2020/day_1.txt", result=2020):
        self.filename = filename
        self.result = result

        res = self.iterate_file(units=2)
        print("CHALLENGE 2020.1.1: "+str(res))

        res = self.iterate_file(units=3)
        print("CHALLENGE 2020.1.2: "+str(res))

    def find_added(self, data, partial_sum, partial_prod, units):
        counter = 0
        for x in data:
            if units > 1:
                match = self.find_added(data[counter:], partial_sum + x, partial_prod * x, units - 1)
                if match:
                    return match
            if self.result == partial_sum + x:
                return partial_prod * x
            counter += 1
        return

    def iterate_file(self, units):
        """CHALLENGE 1.1 - 1016131
           CHALLENGE 1.2 - 276432018"""
        data = [int(x.replace("\n","")) for x in open(self.filename, "r")]
        return self.find_added(data, 0, 1, units)


class Day2:
    """https://adventofcode.com/2020/day/2"""
    def __init__(self, filename="input/2020/day_2.txt"):
        self.filename = filename

        res = self.count_occurrences()
        print("CHALLENGE 2020.2.1: "+str(res))

        res = self.check_one_occurrence()
        print("CHALLENGE 2020.2.2: "+str(res))

    @staticmethod
    def clean_line(line):
        occurrences, character, password = line.split(" ")
        minimum, maximum = occurrences.split("-")
        return int(minimum), int(maximum), character.replace(":", "").strip(), password.strip()

    def count_occurrences(self):
        """CHALLENGE 2.1 - 414"""
        data = [x.replace("\n","") for x in open(self.filename, "r")]
        valid = 0
        for line in data:
            minimum, maximum, character, password = self.clean_line(line)
            if maximum >= password.count(character) >= minimum:
                valid += 1
        return valid

    def check_one_occurrence(self):
        """CHALLENGE 2.2 - 413"""
        data = [x.replace("\n","") for x in open(self.filename, "r")]
        valid = 0
        for line in data:
            first, second, character, password = self.clean_line(line)
            if password[first - 1] == character and password[second - 1] != character:
                valid += 1
            if password[first - 1] != character and password[second - 1] == character:
                valid += 1
        return valid


class Day3:
    """https://adventofcode.com/2020/day/3"""
    def __init__(self, filename="input/2020/day_3.txt"):
        self.filename = filename

        res = self.count_slop(down=1, right=3)
        print("CHALLENGE 2020.3.1: "+str(res))

        res = self.check_slops()
        print("CHALLENGE 2020.3.2: "+str(res))

    def count_slop(self, down, right):
        """CHALLENGE 3.1 - 200"""
        data = [x.replace("\n","") for x in open(self.filename, "r")]
        position, trees, jump = right, 0, down
        count_line = 1
        for line in data[1:]:
            if jump > 1:
                jump -= 1
                count_line += 1
                continue
            count_line += 1
            if position >= len(line):
                position -= len(line)
            if line[position] == "#":
                trees += 1
            position += right
            jump = down
        return trees

    def check_slops(self):
        """CHALLENGE 3.2 - 3737923200"""
        result = self.count_slop(down=1, right=1)
        result *= self.count_slop(down=1, right=3)
        result *= self.count_slop(down=1, right=5)
        result *= self.count_slop(down=1, right=7)
        result *= self.count_slop(down=2, right=1)
        return result


class Day4:
    """https://adventofcode.com/2020/day/4"""
    def __init__(self, filename="input/2020/day_4.txt"):
        self.filename = filename
        self.required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
        self.optional_fields = ["cid"]

        res = self.valid_passports()
        print("CHALLENGE 2020.4.1: "+str(res))

        res = self.valid_passports(check_content=True)
        print("CHALLENGE 2020.4.2: "+str(res))

    @staticmethod
    def clean_data(line):
        data = {}
        for pair in line.split(" "):
            key, value = pair.split(":")
            data[key] = value
        return data

    @staticmethod
    def validate_key(key, value):
        if key == "cid":
            return True
        elif key == "byr":
            if 2002 >= int(value) >= 1920:
                return True
        elif key == "iyr":
            if 2020 >= int(value) >= 2010:
                return True
        elif key == "eyr":
            if 2030 >= int(value) >= 2020:
                return True
        elif key == "hgt":
            if "cm" in value:
                if 193 >= int(value.replace("cm", "")) >= 150:
                    return True
            if "in" in value:
                if 76 >= int(value.replace("in", "")) >= 59:
                    return True
        elif key == "hcl":
            return True if match(r"#[0-9a-f]{6}", value) else None
        elif key == "ecl":
            if value.strip() in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"):
                return True
        elif key == "pid":
            if len(value.strip()) == 9 and int(value.strip()):
                return True

    def valid_passports(self, check_content=False):
        """CHALLENGE 4.1 - 204
           CHALLENGE 4.2 - between 179"""
        data = [x.replace("\n","") for x in open(self.filename, "r")]
        data.append("")
        missing_fields = self.required_fields.copy()
        valid = 0
        for x in data:
            if x == "":
                if not missing_fields:
                    valid += 1
                missing_fields = self.required_fields.copy()
                continue
            key_pairs = self.clean_data(x)
            for key in key_pairs.keys():
                if check_content and not self.validate_key(key, key_pairs[key]):
                    continue
                try:
                    missing_fields.remove(key)
                except ValueError:
                    pass
        return valid


if __name__ == "__main__":
    """python -m code2020 -d 1"""
    parser = ArgumentParser()
    parser.add_argument("--day", "-d", type=int, default=1)
    args = parser.parse_args()
    start_time = time()

    try:
        eval("Day"+str(args.day))()
    except NameError:
        print("Day Not Implemented")

    time_taken = time() - start_time
    print("TIME TAKEN %s sec" % time_taken)
