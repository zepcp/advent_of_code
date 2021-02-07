"""https://adventofcode.com/2020"""
from argparse import ArgumentParser
from time import time


class Day1:
    """https://adventofcode.com/2020/day/1"""
    def __init__(self, filename="input/2020_1.txt", result=2020):
        self.filename = filename
        self.result = result

        self.time = time()
        res = self.iterate_file(units=2)
        print("CHALLENGE 2020.1.1: "+str(res))

        res = self.iterate_file(units=3)
        print("CHALLENGE 2020.1.2: "+str(res))

        time_taken = time()-self.time
        print("TIME TAKEN %s sec" % time_taken)

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
    def __init__(self, filename="input/2020_2.txt"):
        self.filename = filename

        self.time = time()
        res = self.count_occurrences()
        print("CHALLENGE 2020.2.1: "+str(res))

        res = self.check_one_occurrence()
        print("CHALLENGE 2020.2.2: "+str(res))

        time_taken = time()-self.time
        print("TIME TAKEN %s sec" % time_taken)

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
    def __init__(self, filename="input/2020_3.txt"):
        self.filename = filename

        self.time = time()
        res = self.count_slop(down=1, right=3)
        print("CHALLENGE 2020.3.1: "+str(res))

        res = self.check_slops()
        print("CHALLENGE 2020.3.2: "+str(res))

        time_taken = time()-self.time
        print("TIME TAKEN %s sec" % time_taken)

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


if __name__ == "__main__":
    """python -m code2020 -d 1"""
    parser = ArgumentParser()
    parser.add_argument("--day", "-d", type=int, default=1)
    args = parser.parse_args()

    try:
        eval("Day"+str(args.day))()
    except NameError:
        print("Day Not Implemented")
