safe_reports = 0

with open("input") as fp:
    for line in fp:
        levels = [int(x) for x in line.strip().split()]
        consistent_delta_sign = True
        safe_distance = True
        increasing = levels[0] < levels[1]
        i = 0

        while i < len(levels) - 1:
            if (levels[i] < levels[i+1]) != increasing:
                consistent_delta_sign = False
                break
            elif not (1 <= abs(levels[i+1] - levels[i]) <= 3):
                safe_distance = False
                break
            i += 1
        
        if consistent_delta_sign and safe_distance:
            safe_reports += 1

print(safe_reports)