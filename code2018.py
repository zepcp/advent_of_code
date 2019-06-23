"""https://adventofcode.com/2018"""
from time import time
from numpy import matrix

def find_n(string, n_times):
    """Check if exists N occurrences of a char within a string"""
    for char in string:
        if string.count(char) == n_times:
            return 1
    return 0

class Day1:
    """https://adventofcode.com/2018/day/1"""
    def __init__(self, filename="2018_1.txt", starting_point=0, run=False):
        self.filename = filename
        self.starting_point = starting_point

        if run:
            self.time = time()
            res = self.find_final_state()
            print("CHALLENGE 2018.1.1: "+str(res))

            res = self.find_repeated_state()
            print("CHALLENGE 2018.1.2: "+str(res))

            time_taken = time()-self.time
            print("TIME TAKEN %s sec" % time_taken)

    def find_final_state(self):
        """CHALLENGE 1.1 - 430"""
        data = open(self.filename, "r")
        result = self.starting_point

        for line in data:
            result = result + int(line)

        return result

    def find_repeated_state(self):
        """CHALLENGE 1.2 - 462"""
        result = self.starting_point
        state = [result]

        while True:
            data = open(self.filename, "r")
            for line in data:
                result = result + int(line)
                if result in state:
                    return result
                state.append(result)

class Day2:
    """https://adventofcode.com/2018/day/2"""
    def __init__(self, filename="2018_2.txt", run=False):
        self.filename = filename

        if run:
            self.time = time()
            res = self.find_checksum()
            print("CHALLENGE 2018.2.1: "+str(res))

            res = self.find_similars()
            print("CHALLENGE 2018.2.2: "+str(res))

            time_taken = time()-self.time
            print("TIME TAKEN %s sec" % time_taken)

    def find_checksum(self):
        """CHALLENGE 2.1 - 8398"""
        data = open(self.filename, "r")
        twice = 0
        three_times = 0

        for line in data:
            twice += find_n(line, 2)
            three_times += find_n(line, 3)

        return twice * three_times

    def find_similars(self):
        """CHALLENGE 2.2 - hhvsdkatysmiqjxunezgwcdpr"""
        data = open(self.filename, "r")

        for line in data:
            for pos in range(len(line)):
                sub_line = line[:pos]+line[pos+1:]
                data2 = open(self.filename, "r")
                for test_line in data2:
                    if line == test_line:
                        continue
                    elif sub_line == test_line[:pos]+test_line[pos+1:]:
                        return sub_line.strip()
        return None

class Day3:
    """https://adventofcode.com/2018/day/3"""
    def __init__(self, filename="2018_3.txt", size=1000, run=False):
        self.filename = filename
        self.square = matrix([[0]*size]*size)

        if run:
            self.time = time()
            res = self.find_repeated_squares()
            print("CHALLENGE 2018.3.1: "+str(res))
            res = self.find_no_overlap()
            print("CHALLENGE 2018.3.2: "+str(res))

            time_taken = time()-self.time
            print("TIME TAKEN %s sec" % time_taken)

    @staticmethod
    def parse_elf_line(line):
        """Auxiliar function to parse input file lines"""
        claim, _, start, size = line.split(" ")
        start = start.replace(":", "").split(",")
        size = size.replace("\n", "").split("x")
        claim = int(claim.replace("#", ""))
        x_start = int(start[0])
        y_start = int(start[1])
        x_size = int(size[0])
        y_size = int(size[1])

        return claim, x_start, y_start, x_size, y_size

    def find_repeated_squares(self):
        """CHALLENGE 3.1 - 105047"""
        data = open(self.filename, "r")

        for line in data:
            _, x_start, y_start, x_size, y_size = self.parse_elf_line(line)

            for i in range(x_size):
                for j in range(y_size):
                    self.square[x_start+i, y_start+j] += 1

        return (self.square > 1).sum()

    def find_no_overlap(self):
        """CHALLENGE 3.2 - 658"""
        data = open(self.filename, "r")

        for line in data:
            claim, x_start, y_start, x_size, y_size = self.parse_elf_line(line)

            overlap = False
            for i in range(x_size):
                for j in range(y_size):
                    if self.square[x_start+i, y_start+j] > 1:
                        overlap = True
                        break
                if overlap:
                    break

            if not overlap:
                return claim
        return None

class Day4:
    """https://adventofcode.com/2018/day/4"""
    def __init__(self, filename="2018_4.txt", run=False):
        self.filename = filename

        if run:
            self.time = time()
            res = self.find_guard_opening()
            print("CHALLENGE 2018.4.1: "+str(res))
            res = self.find_minute_opening()
            print("CHALLENGE 2018.4.2: "+str(res))

            time_taken = time()-self.time
            print("TIME TAKEN %s sec" % time_taken)

    @staticmethod
    def parse_action(action):
        """Auxiliar function to parse the guard action"""
        if 'falls asleep' in action:
            return 1
        if 'wakes up' in action:
            return 0
        if 'begins shift' in action:
            return int(action.split(' ')[1].strip('#'))
        return None

    def parse_schedule(self, data):
        """Auxiliar function to parse the schedule of guard actions"""
        schedule = {}

        for line in data:
            month = line[6:8]
            day = line[9:11]
            hour = line[12:14]
            minute = int(line[15:17])+1
            action = self.parse_action(line[19:])

            day = day if hour == '00' else str(int(day)+1)
            day = day if len(day) == 2 else '0'+day

            try:
                schedule[day+"-"+month]
            except KeyError:
                schedule[day+"-"+month] = [0]*61

            if action > 1:
                schedule[day+"-"+month][0] = action
            elif action in (0, 1):
                while minute < len(schedule[day+"-"+month]):
                    schedule[day+"-"+month][minute] = action
                    minute += 1

        return schedule

    def find_guard_opening(self):
        """CHALLENGE 4.1 - 95199"""
        schedule = self.parse_schedule(sorted(open(self.filename, "r")))

        sleepy_guard = -1
        slept_time = 0
        guards = {}
        for date in schedule:
            guard_id = schedule[date][0]
            slept = sum(schedule[date][1:])
            try:
                guards[guard_id] += slept
            except KeyError:
                guards[guard_id] = slept
            if guards[guard_id] > slept_time:
                sleepy_guard = guard_id
                slept_time = guards[guard_id]

        sleepy_time = -1
        slept_time = 0
        times = [0]*60
        for date in schedule:
            if schedule[date][0] != sleepy_guard:
                continue
            for minute in range(1, len(schedule[date])):
                times[minute-1] += schedule[date][minute]
                if times[minute-1] > slept_time:
                    sleepy_time = minute-1
                    slept_time = times[minute-1]

        return sleepy_guard * sleepy_time

    def find_minute_opening(self):
        """CHALLENGE 4.2 - 7887"""
        schedule = self.parse_schedule(sorted(open(self.filename, "r")))

        sleepy_minute = -1
        sleepy_guard = -1
        slept_time = 0
        result = 0
        times = {}
        for date in schedule:
            guard_id = schedule[date][0]
            for minute in range(1, len(schedule[date][1:])):
                try:
                    times[guard_id][minute] += schedule[date][minute+1]
                except KeyError:
                    times[guard_id] = [0]*60
                    times[guard_id][minute] = schedule[date][minute+1]
                if times[guard_id][minute] > slept_time:
                    sleepy_minute = minute
                    sleepy_guard = guard_id
                    slept_time = times[guard_id][minute]
                    result = sleepy_minute*sleepy_guard
                elif times[guard_id][minute] == slept_time:
                    if guard_id * minute < result:
                        sleepy_minute = minute
                        sleepy_guard = guard_id
                        result = sleepy_minute*sleepy_guard

        return result

class Day5:
    """https://adventofcode.com/2018/day/5"""
    def __init__(self, filename="2018_5.txt", run=False):
        self.filename = filename

        if run:
            self.time = time()
            res = self.react_polymer()
            print("CHALLENGE 2018.5.1: "+str(res))

            res = self.shortest_polymer()
            print("CHALLENGE 2018.5.2: "+str(res))

            time_taken = time()-self.time
            print("TIME TAKEN %s sec" % time_taken)

    @staticmethod
    def remove_pairs(polymer):
        """Auxiliar function to remove pairs from polymer"""
        i = 0
        res = []
        while i < len(polymer):
            try:
                if polymer[i].lower() == polymer[i+1].lower() \
                    and polymer[i] != polymer[i+1]:
                    i += 2
                    continue
            except IndexError:
                res.append(polymer[i])
                break
            res.append(polymer[i])
            i += 1
        return ''.join(res)

    def react_polymer(self):
        """CHALLENGE 5.1 - 11118"""
        data = open(self.filename, "r")
        for line in data:
            polymer = line

        while True:
            new = self.remove_pairs(polymer)
            if len(polymer) == len(new):
                break
            polymer = new

        return len(new)

    def shortest_polymer(self):
        """CHALLENGE 5.2 - 6948"""
        data = open(self.filename, "r")
        for line in data:
            polymer = line

        length = len(polymer)
        for char in set(polymer.upper()):
            short_poly = polymer.replace(char, "").replace(char.lower(), "")
            while True:
                new = self.remove_pairs(short_poly)
                if len(short_poly) == len(new):
                    break
                short_poly = new
            if len(new) < length:
                length = len(new)

        return length

class Day6:
    """https://adventofcode.com/2018/day/6"""
    def __init__(self, filename="2018_6.txt", distance=10000, run=False):
        self.filename = filename

        if run:
            self.time = time()
            res = self.safest_area()
            print("CHALLENGE 2018.6.1: "+str(res))

            res = self.closest_area(distance)
            print("CHALLENGE 2018.6.2: "+str(res))

            time_taken = time()-self.time
            print("TIME TAKEN %s sec" % time_taken)

    @staticmethod
    def parse_data(filename):
        """Auxiliar function to parse data file into a matrix"""
        locations = []
        min_x = 1000
        max_x = 0
        min_y = 1000
        max_y = 0
        data = open(filename, "r")
        for line in data:
            pos_x = int(line.split(",")[0].strip())
            pos_y = int(line.split(",")[1].strip())
            locations.append([pos_x, pos_y])
            min_x = pos_x if pos_x < min_x else min_x
            max_x = pos_x+1 if pos_x > max_x else max_x
            min_y = pos_y if pos_y < min_y else min_y
            max_y = pos_y+1 if pos_y > max_y else max_y
        area = matrix([[0]*(max_x-min_x)]*(max_y-min_y))

        i = 0
        for sight in locations:
            i += 1
            sight[0] = sight[0]-min_x
            sight[1] = sight[1]-min_y
            area[sight[1], sight[0]] = i

        return locations, area

    @staticmethod
    def closest(locations, pos_x, pos_y):
        """Fill matrix with closest sight"""
        distance = 1000
        value = 0
        i = 0
        for sight in locations:
            i += 1
            dist = abs(pos_x-sight[0])+abs(pos_y-sight[1])
            if dist < distance:
                distance = dist
                value = i
            elif dist == distance:
                value = 0
        return value

    @staticmethod
    def total(locations, pos_x, pos_y):
        """Fill matrix with total distance to all sights"""
        total = 0
        for sight in locations:
            total += abs(pos_x-sight[0])+abs(pos_y-sight[1])
        return total

    def safest_area(self):
        """CHALLENGE 6.1 - 3401"""
        locations, area = self.parse_data(self.filename)

        for pos_y in range(len(area)):
            for pos_x in range(int(area.size/len(area))):
                if area[pos_y, pos_x] == 0:
                    area[pos_y, pos_x] = self.closest(locations, pos_x, pos_y)

        count = 0
        for loc in range(len(locations)):
            loc += 1
            if loc in area[0, :] or loc in area[:, 0] \
                or loc in area[len(area)-1, :] \
                or loc in area[:, int(area.size/len(area))-1]:
                continue
            occurrences = (area == loc).sum()
            count = occurrences if occurrences > count else count
        return count

    def closest_area(self, distance):
        """CHALLENGE 6.2 - 49327"""
        locations, area = self.parse_data(self.filename)

        for pos_y in range(len(area)):
            for pos_x in range(int(area.size/len(area))):
                if area[pos_y, pos_x] == 0:
                    area[pos_y, pos_x] = self.total(locations, pos_x, pos_y)

        count = (area < distance).sum()
        for sight in locations:
            dist = self.total(locations, sight[0], sight[1])
            if dist > distance:
                count -= 1

        return count

class Day7:
    """https://adventofcode.com/2018/day/7"""
    def __init__(self, filename="2018_7.txt", run=False, team=5, task_time=60):
        self.filename = filename

        if run:
            self.time = time()
            res = self.steps_ordered()
            print("CHALLENGE 2018.7.1: "+str(res))

            res = self.steps_time(team, task_time)
            print("CHALLENGE 2018.7.2: "+str(res))

            time_taken = time()-self.time
            print("TIME TAKEN %s sec" % time_taken)

    @staticmethod
    def parse_data(filename):
        """Auxiliar function to parse data file into dict and array"""
        steps = {}
        options = []
        data = sorted(open(filename, "r"))
        for line in data:
            before = line.split()[1]
            after = line.split()[7]
            try:
                steps[before].append(after)
            except KeyError:
                steps[before] = []
                steps[before].append(after)
            if before not in options:
                options.append(before)
            if after not in options:
                options.append(after)

        return steps, options

    @staticmethod
    def available_options(options, steps, multiple=False):
        """Auxiliar function to find available options"""
        valid_options = []
        for opt in sorted(options):
            valid = True
            for step in steps:
                if opt in steps[step]:
                    valid = False
                    break
            if valid:
                if not multiple:
                    return opt
                valid_options.append(opt)

        return valid_options

    def steps_ordered(self):
        """CHALLENGE 7.1 - FMOXCDGJRAUIHKNYZTESWLPBQV"""
        steps, options = self.parse_data(self.filename)

        sequence = []
        while options != []:
            opt = self.available_options(options, steps)
            sequence.append(opt)
            options.remove(opt)
            steps[opt] = []

        return ''.join(sequence)

    def steps_time(self, team=5, task_time=60):
        """CHALLENGE 7.2 - 1053"""
        steps, options = self.parse_data(self.filename)

        workers = [0]*team
        jobs = ['']*team
        time_taken = -1

        while options != [] or workers != [0]*team:
            time_taken += 1

            for worker, time_left in enumerate(workers):
                if time_left > 0:
                    workers[worker] -= 1
                    if workers[worker] == 0:
                        steps[jobs[worker]] = []
                        jobs[worker] = ''

            if 0 not in workers:
                continue

            valid = self.available_options(options, steps, multiple=True)
            if valid:
                for worker, time_left in enumerate(workers):
                    if time_left == 0 and valid:
                        workers[worker] = task_time+ord(valid[0])-64
                        jobs[worker] = valid[0]
                        options.remove(valid[0])
                        valid.remove(valid[0])

        return time_taken

if __name__ == "__main__":
    Day1(run=False)
    Day2(run=False)
    Day3(run=False)
    Day4(run=False)
    Day5(run=False)
    Day6(run=False)
    Day7(run=False)
