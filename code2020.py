"""https://adventofcode.com/2020"""
from argparse import ArgumentParser
from time import time
from re import match
from math import ceil, floor


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
           CHALLENGE 4.2 - 179"""
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


class Day5:
    """https://adventofcode.com/2020/day/5"""
    def __init__(self, filename="input/2020/day_5.txt"):
        self.filename = filename
        self.rows = 127
        self.columns = 7

        res = self.highest_seat()
        print("CHALLENGE 2020.5.1: "+str(res))

        res = self.check_seat()
        print("CHALLENGE 2020.5.2: "+str(res))

    def compute_seat(self, seat):
        row, column = [0, self.rows], [0, self.columns]
        for x in seat:
            if x == "F":
                row[1] -= ceil((row[1] - row[0]) / 2)
            elif x == "B":
                row[0] += ceil((row[1] - row[0]) / 2)
            elif x == "L":
                column[1] -= ceil((column[1] - column[0]) / 2)
            elif x == "R":
                column[0] += ceil((column[1] - column[0]) / 2)
        return row[0] * 8 + column[0]

    def highest_seat(self):
        """CHALLENGE 5.1 - 848"""
        data = [x.replace("\n","") for x in open(self.filename, "r")]
        highest = data[0]
        for seat in data[1:]:
            for pos, label in enumerate(seat):
                if label == highest[pos]:
                    continue
                if label in ("B", "R"):
                    highest = seat
                break
        return self.compute_seat(highest)

    def check_seat(self):
        """CHALLENGE 5.2 - 682"""
        data = [x.replace("\n","") for x in open(self.filename, "r")]
        all_seats = [self.compute_seat(seat) for seat in data]
        all_seats.sort()

        for pos, seat in enumerate(all_seats):
            if seat + 1 != all_seats[pos + 1]:
                return seat + 1


class Day6:
    """https://adventofcode.com/2020/day/6"""
    def __init__(self, filename="input/2020/day_6.txt"):
        self.filename = filename

        res = self.sum_yes_anyone()
        print("CHALLENGE 2020.6.1: "+str(res))

        res = self.sum_yes_everyone()
        print("CHALLENGE 2020.6.2: "+str(res))

    def sum_yes_anyone(self):
        """CHALLENGE 6.1 - 6249"""
        data = [x.replace("\n","") for x in open(self.filename, "r")]
        data.append("")
        result, answers = 0, []
        for user in data:
            if user == "":
                result += len(set(answers))
                answers = []
                continue
            [answers.append(x) for x in user]

        return result

    def sum_yes_everyone(self):
        """CHALLENGE 6.2 - 3103"""
        data = [x.replace("\n","") for x in open(self.filename, "r")]
        data.append("")
        result, answers = 0, None
        for user in data:
            if user == "":
                result += len(set(answers))
                answers = None
                continue

            latest = [x for x in user]
            if answers is None:
                answers = latest
                continue

            updated_answers = []
            for x in answers:
                if x in latest:
                    updated_answers.append(x)
            answers = updated_answers

        return result


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
