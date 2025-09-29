import random

if __name__ == "__main__":
    pass # Ваш код здесь

def average_marks(arr):
    avg_mark = []
    for i in arr:
        a = (i[0] + i[1] + i[2] + i[3] + i[4]) / 5
        avg_mark.append(a)
    return avg_mark

students = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
marks = []
for i in range(len(students)):
    marks.append([])
    for j in range(5):
        marks[i].append(random.randint(2,5))

print('Что вы хотите узнать?')
print('Среднюю оценку каждого студента.(1)')
print('Самую высокую и низкую оценку по предмету.(2)')
print('Студента с лучшими и худшими средними баллами.(3)')

request = input('Введите 1/2/3: ')

if request == '1':
    for i in range(len(students)):
        print(students[i], ':', average_marks(marks)[i])

if request == '2':
    mmax = 0
    mmin = 100
    for i in marks:
        for  j in range(5):
            mmax = max(i[j], mmax)
            mmin = min(i[j], mmin)
    print('Самая высокая оценка: ', mmax)
    print('Самая низкая оценка: ', mmin)

if request == '3':
    avg = average_marks(marks)
    m = avg.index(max(avg))
    l = avg.index(min(avg))
    print(f'Студент с самым высоким средним баллом({max(avg)}): {students[m]}')
    print(f'Студент с самым низким средним баллом({min(avg)}): {students[l]}')
