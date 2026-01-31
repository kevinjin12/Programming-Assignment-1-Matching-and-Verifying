from collections import deque
from pathlib import Path
import random
import time

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

def read_pair_input(n, filename):
    hospital_pairs = []
    with open(filename, "r") as file:
        for _ in range(n):
            current_line = file.readline().split()
            hospital_pairs.append((int(current_line[0]), int(current_line[1])))
    return hospital_pairs

def write_matching_output(filename, final_pairs):
    with open(filename, "w") as file:
        for hospital_idx, student_idx in final_pairs:
            file.write(str(hospital_idx) + " " + str(student_idx) + "\n")

    return

def write_verifier_output(filename, message):
    with open(filename, "w") as file:
        file.write(message)

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

def verifier(n, final_pairs, hospital_preferences, student_preferences):
    
    # Used to check if each student and hospital is uniquely represented in the final pairs
    unique_students = set()
    unique_hospitals = set()

    # Stores the pairs as lookups to quickly find what applicant/hospital is a given index matched to
    hospital_to_student = {}
    student_to_hospital = {}

    # Stores the ranks of each pair of hospital/applicant
    hospital_ranks = [[n for _ in range(n)] for _ in range(n)]
    student_ranks = [[n for _ in range(n)] for _ in range(n)]

    # Checks Validity
    for hospital, student in final_pairs:
        unique_hospitals.add(hospital)
        unique_students.add(student)

        hospital_to_student[hospital] = student
        student_to_hospital[student] = hospital
    
    # Make sure we only have n pairs and each hospital/applicant is used once
    if len(final_pairs) != n:
        return "INVALID there are not n pairs"

    if len(unique_hospitals) != n or len(unique_students) != n:
        return "INVALID every hospital and student is not uniquely used"

    # Format the data into easy lookups to check the rank of a given hospital and student
    for i, (hospitals, students) in enumerate(zip(hospital_preferences, student_preferences)):
        for rank, (s_j, h_j) in enumerate(zip(hospitals, students)):
            hospital_ranks[i][s_j - 1] = rank
            student_ranks[i][h_j - 1] = rank

    # Checks Stability
    for hospital_idx in range(1, n+1):
        for student_idx in range(1, n+1):

            # If already matched we ignore
            if hospital_to_student[hospital_idx] == student_idx:
                continue
            
            # Get the ranks of what the hospital ranked this specific student and vice versa
            hospital_rank_of_student = hospital_ranks[hospital_idx - 1][student_idx - 1]
            student_rank_of_hospital = student_ranks[student_idx -1][hospital_idx - 1]

            # Get the ranks of what G-S came up with
            hospitals_match_rank = hospital_ranks[hospital_idx - 1][hospital_to_student[hospital_idx] - 1]
            student_match_rank = student_ranks[student_idx - 1][student_to_hospital[student_idx] - 1]

            # If they ranked each other higher than what they are currently matched with, we have an unstable solution
            if hospital_rank_of_student < hospitals_match_rank and student_rank_of_hospital < student_match_rank:
                return "UNSTABLE blocking pair: (" + str(hospital_idx) + ", " + str(student_idx) + ")"
    
    return "VALID STABLE"

def generate_preference_lists(n):
    hospital_preferences = []
    student_preferences = []
    for idx in range(2*n):
        pref_list = list(range(1, n + 1))
        random.shuffle(pref_list)

        if idx < n:
            hospital_preferences.append(pref_list)
        else:
            student_preferences.append(pref_list)
    
    return hospital_preferences, student_preferences

def run_trial(n):

    # Conducting 10 experiments per n to reduce any noise we get from randomly generating the input
    avg_time = 0
    for _ in range(10):
        
        # First generate input
        hospital_prefs, student_prefs = generate_preference_lists(n)

        start_time = time.perf_counter()
        hospital_pairs = matching_engine(n, hospital_prefs, student_prefs)
        end_time = time.perf_counter()

        avg_time += (end_time - start_time)

    return avg_time / 10.0

def run_verifier_trial(n):

    avg_time = 0
    for _ in range(10):

        # Generate input
        hospital_prefs, student_prefs = generate_preference_lists(n)
        hospital_pairs = matching_engine(n, hospital_prefs, student_prefs)

        start_time = time.perf_counter()
        verifier(n, hospital_pairs, hospital_prefs, student_prefs)
        end_time = time.perf_counter()

        avg_time += (end_time - start_time)
    
    return avg_time / 10.0

def measure_runtime(output_file, is_verifier):

    with open(output_file, "w") as file:
        file.write("N   Average Time\n")

        n = 1
        while n <= 512:

            if not is_verifier:
                avg_time = run_trial(n)
            else:
                avg_time = run_verifier_trial(n)

            file.write(str(n) + "   " + str(avg_time) + "\n")
            n *= 2

def main():

    base_dir = Path(__file__).resolve().parent.parent
    input_file_path = base_dir / "data/input.in"
    output_file_path = base_dir / "data/output.out"
    verifier_file_path = base_dir / "data/verifier.out"

    # measure_runtime(base_dir/"data/Measuring Runtime/verifier_times.out", True)
    # measure_runtime(base_dir/"data/Measuring Runtime/matching_engine_times.out", False)
    
    print("Welcome to the Matching Engine and Verifier!\n")
    user_choice = input("Which mode would you like to run? [matcher/verifier] ")

    if user_choice.lower() == "matcher":
        n, hospital_prefs, student_prefs = read_input(input_file_path)
        hospital_pairs = matching_engine(n, hospital_prefs, student_prefs)
        write_matching_output(output_file_path, hospital_pairs)
    elif user_choice.lower() == "verifier":
        n, hospital_prefs, student_prefs = read_input(input_file_path)
        hospital_pairs = read_pair_input(n, output_file_path)
        verifier_message = verifier(n, hospital_pairs, hospital_prefs, student_prefs)
        write_verifier_output(verifier_file_path, verifier_message)

if __name__ == "__main__":
    main()