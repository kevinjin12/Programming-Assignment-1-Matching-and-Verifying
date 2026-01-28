def matching_engine(n, hospital_preferences, student_preferences):
    hospital_preferences = [[x - 1 for x in row] for row in hospital_preferences]
    student_preferences = [[x - 1 for x in row] for row in student_preferences]

    # pairs from the perspective of the hospitals
    hospital_pairs = [-1] * n

    # pairs from the perspective of the students
    student_pairs = [-1] * n

    next_proposal = [0] * n

    student_rank = [[0]*n for _ in range(n)]
    for student in range(n):
        for rank, hospital in enumerate(student_preferences[student]):
            student_rank[student][hospital] = rank

    while True:
        progress = False

        for hospital in range(n):
            if hospital_pairs[hospital] == -1 and next_proposal[hospital] < n:
                student = hospital_preferences[hospital][next_proposal[hospital]]
                next_proposal[hospital] += 1
                progress = True

                if student_pairs[student] == -1:
                    hospital_pairs[hospital] = student
                    student_pairs[student] = hospital
                else:
                    current_hospital = student_pairs[student]
                    if student_rank[student][hospital] < student_rank[student][current_hospital]:
                        student_pairs[student] = hospital
                        hospital_pairs[current_hospital] = -1
                        hospital_pairs[hospital] = student

        if not progress:
            break
    
    res = []
    for hospital, student in enumerate(hospital_pairs):
        res.append((hospital + 1, student + 1))
    return res

def main():
    hospital_preferences = [[1, 2, 3], [2, 3, 1], [2, 1, 3]]
    student_preferences = [[2, 1, 3], [1, 2, 3], [1, 2, 3]]
    n = len(hospital_preferences)

    hospital_pairs = matching_engine(n, hospital_preferences, student_preferences)

    print("Hospital pairs:", hospital_pairs)

if __name__ == "__main__":
    main()