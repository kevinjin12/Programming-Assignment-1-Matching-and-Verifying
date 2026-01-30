from collections import deque

def read_input(filename):
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file]

    if not lines:
        raise ValueError("Empty input file")
    
    n = int(lines[0])

    if len(lines) != 2 * n + 1:
        raise ValueError(f"Expected {2*n + 1} lines, got {len(lines)}")
    
    hospital_prefs = []
    for i in range(1, n + 1):
        hospital_prefs.append([int(x) for x in lines[i].split()])

    student_prefs = []
    for i in range(n + 1, 2 * n + 1):
        student_prefs.append([int(x) for x in lines[i].split()])

    if len(hospital_prefs) != n or len(student_prefs) != n:
        raise ValueError("Number of hospitals and students must be equal")

    return n, hospital_prefs, student_prefs


def matching_engine(n, hospital_prefs, student_prefs):
    # change perference list input from 1-indexed to 0-indexed
    hospital_prefs = [[x - 1 for x in row] for row in hospital_prefs]
    student_prefs = [[x - 1 for x in row] for row in student_prefs]

    # pairs from the perspective of the hospitals
    hospital_pairs = [-1] * n

    # pairs from the perspective of the students
    student_pairs = [-1] * n

    # keeps track of next student each hospital wants to match with
    next_student = [0] * n

    # create 2d matrix for easy lookup of rankings
    student_ranks = [[0] * n for i in range(n)]
    for student in range(n):
        for rank, hospital in enumerate(student_prefs[student]):
            student_ranks[student][hospital] = rank

    unmatched_hospitals = deque(range(n))

    while unmatched_hospitals:
        h = unmatched_hospitals.popleft()

        # top student on h's list whom h has not been matched
        s = hospital_prefs[h][next_student[h]]

        # student is free
        if student_pairs[s] == -1:
            hospital_pairs[h] = s
            student_pairs[s] = h    

        # student prefers hospital h to current assignment
        elif student_ranks[s][h] < student_ranks[s][student_pairs[s]]:
            old_h = student_pairs[s]
            hospital_pairs[h] = s
            student_pairs[s] = h
            # unmatch old hospital
            hospital_pairs[old_h] = -1
            unmatched_hospitals.append(old_h)

        # student rejects hospital h
        else:
            unmatched_hospitals.append(h)

        # hospital h did not match with student s so move on to next preference
        next_student[h] += 1

    res = []
    for hospital, student in enumerate(hospital_pairs):
        res.append([hospital + 1, student + 1])

    return res

def main():
    n, hospital_prefs, student_prefs = read_input("tests/test1.in")

    hospital_pairs = matching_engine(n, hospital_prefs, student_prefs)

    print(hospital_pairs)



if __name__ == "__main__":
    main()