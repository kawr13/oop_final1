import csv


class NameDescriptor:
    def __get__(self, instance, owner):
        return instance._name
    

    def __set__(self, instance, value):
        if not value.isalpha():
            raise ValueError("ФИО должно содержать только буквы")
        if not value.istitle():
            raise ValueError("ФИО должно начинаться с заглавной буквы")
        instance._name = value


class SubjectDescriptor:
    def __get__(self, instance, owner):
        return instance._subjects
      

    def __set__(self, instance, value):
        raise AttributeError("Невозможно изменить названия предметов")
        

class Student:
    name = NameDescriptor()
    subjects = SubjectDescriptor()


    def __init__(self, subjects_file):
        self._subjects = self.load_subjects(subjects_file)
        self.marks = {subject: {'grades': [], 'tests': []} for subject in self._subjects}
    

    @property
    def name(self):
        return f'студент: {self._name}'
    

    @name.setter
    def name(self, value):
        self._name = value
    

    @property
    def subjects(self):
        return self._subjects


    def load_subjects(self, file):
        with open(file, 'r', encoding='utf-8', newline='') as csvfile:
            reader = csv.reader(csvfile)
            subjects = next(reader)  # Assuming the first row contains subject names
            return subjects


    def add_grade(self, subject, grade):
        if subject not in self._subjects:
            raise ValueError("Недопустимый предмет")
        if grade < 2 or grade > 5:
            raise ValueError("Недопустимая оценка")
        self.marks[subject]['grades'].append(grade)


    def add_test_result(self, subject, score):
        if subject not in self._subjects:
            raise ValueError("Недопустимый предмет")
        if score < 0 or score > 100:
            raise ValueError("Недопустимый результат теста")
        self.marks[subject]['tests'].append(score)


    def calculate_average_grade(self, subject):
        if subject not in self._subjects:
            raise ValueError("Недопустимый предмет")
        grades = self.marks[subject]['grades']
        if not grades:
            return 0
        av_r = sum(grades) / len(grades)
        return round(av_r, 2)


    def calculate_average_grade_all_subjects(self):
        all_grades = [grade for subject in self._subjects for grade in self.marks[subject]['grades']]
        if not all_grades:
            return 0
        av_r = sum(all_grades) / len(all_grades)
        return round(av_r, 2)
    

    def points(self, names):
        grat = []
        print(f'Все оценки по {names}: ', end='')
        if names in self.marks.keys():
            for i in range(len(self.marks[names]['grades'])):
                grat.append(f"{self.marks[names]['grades'][i]}")
            return grat
    

    def tests_points(self, names):
        grat = []
        print(f'Колличество баллов по {names}: ', end='')
        if names in self.marks.keys():
            for i in range(len(self.marks[names]['tests'])):
                grat.append(f"{self.marks[names]['tests'][i]}")
            return grat



alex = Student("students.csv")
alex.name = "Александр"
print('Предметы студента:', *alex.subjects)
print(alex.name)
alex.add_grade("Математика", 4)
alex.add_grade("Математика", 5)
alex.add_grade("Математика", 2)
alex.add_grade("История", 4)
alex.add_grade("История", 5)
alex.add_grade("История", 2)
alex.add_grade("Наука", 3)
alex.add_grade("Наука", 5)
alex.add_test_result("Математика", 85)
alex.add_test_result("Математика", 92)
alex.add_test_result("Наука", 78)
average_math_grade = alex.calculate_average_grade("Математика")
average_science_grade = alex.calculate_average_grade("Наука")
average_grade_all_subjects = alex.calculate_average_grade_all_subjects()
print(*alex.points("Математика"))
print(*alex.tests_points("Математика"))

print("Средний балл по Математике:", average_math_grade)
print("Средний балл по Науке:", average_science_grade)
print("Средний балл по всем предметам:", average_grade_all_subjects)
print()