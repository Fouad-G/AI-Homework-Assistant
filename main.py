from database_manager import DatabaseManager
from student import Student
from homework_generator import HomeworkGenerator
from teacher import Teacher
from lesson import Lesson
from homework import Homework
from datetime import date
from pdf import Pdf

class App:
    def __init__(self, db_path=":memory:"):
        self.db_manager = DatabaseManager(db_path=db_path)
        self.hw_generator = HomeworkGenerator()
        self.pdf_generator=Pdf()
        self.current_teacher = None  # Könnte man setzen, wenn man sich "einloggt"
    
    def setup_db(self):
        """Erstellt DB-Verbindung und Tabellen."""
        self.db_manager.connect()
        self.db_manager.create_tables()
    
    def run(self):
        """Einfacher CLI-Loop, nur zur Demo."""
        self.setup_db()
        
        # Beispiel: Lehrer anlegen
        teacher = Teacher(teacher_id=None, name="Herr Müller", subject="Mathematik")
        self.db_manager.add_teacher(teacher)
        self.current_teacher = teacher

        while True:
            print("\n==== Hauptmenü ====")
            print("1) Neuen Schüler anlegen")
            print("2) Neue Stunde (Lesson) erstellen")
            print("3) Hausaufgabe für ein Schüler generieren")
            print("4) Hausaufgaben für alle Schüler generieren")

            print("5) Alle Schüler anzeigen")  # 🔹 Neue Option
            print("6) Alle Themen anzeigen")  # 🔹 Neue Option
            print("7) Hausaufgaben anzeigen")  # 🔹 Neue Option

            print("8) Beenden")

            choice = input("Auswahl: ")

            if choice == "1":
                self.handle_new_student()
            elif choice == "2":
                self.handle_new_lesson()
            elif choice == "3":
                self.generate_homework()

            elif choice =="4":
                self.generate_homeworks_for_all()
            elif choice == "5":
                self.print_all_students()  # 🔹 Hier wird die neue Funktion aufgerufen
            elif choice == "6":
                self.print_all_lessons()
            elif choice=="7":
                self.print_all_homeworks()    

            elif choice=="8":
                print("programm beendet")
            else:
                print("Ungültige Auswahl. Bitte erneut versuchen.")

    
    def handle_new_student(self):
        name = input("Name des Schülers: ")
        age = int(input("Alter: "))
        interests = input("Interessen (Komma-separiert): ").split(",")
        new_student = Student(None, name, age, interests)
        student_id = self.db_manager.add_student(new_student)
        print(f"Neuer Schüler angelegt mit ID {student_id}")

    def handle_new_lesson(self):
        topic = input("Thema der Stunde: ")
        lesson = self.current_teacher.create_Lesson(topic=topic)
        lesson_id = self.db_manager.add_lesson(lesson)
        print(f"Neue Lesson angelegt mit ID {lesson_id}")

    def generate_homework(self):
        student_id = int(input("Für welchen Student (ID)? "))
        student = self.db_manager.get_student(student_id)
        if not student:
            print("Student nicht gefunden.")
            return
        
        lesson_id = int(input("Für welche Lesson (ID)? "))
        # Hier könntest du lesson laden, für Demo erstellen wir eine Dummy-Lesson
        lesson = Lesson(lesson_id, date.today(), "", "", self.current_teacher.teacher_id)
        
        # KI/Algorithmus generieren die Hausaufgaben
        homework = self.hw_generator.generate_homework(student, lesson)
        
        # In der Datenbank speichern
        hw_id = self.db_manager.add_homework(homework)
        self.pdf_generator.generate_homework_pdf(student.name, lesson.topic, date.today(), homework.tasks)
        print(f"Hausaufgabe (ID: {hw_id}) für {student.name} erstellt.")

    def generate_homeworks_for_all(self):

        students = self.db_manager.get_students()  # Get all students
        if not students:
            print("Keine Schüler gefunden.")
            return

        # 🔹 Display available lessons before asking for ID
        lessons = self.db_manager.get_lessons()
        print("\nVerfügbare Lektionen:")
        for lesson in lessons:
            print(f"ID: {lesson[0]}, Thema: {lesson[1]}")

        lesson_id = int(input("\nFür welche Lesson (ID)? "))  # Ask for lesson once

        # 🔹 Fetch the specific lesson
        lesson = self.db_manager.get_lesson(lesson_id)
        
        if not lesson:
            print("Lesson nicht gefunden.")
            return
        for student in students:  # Iterate over students
            student_id, student_name, student_age, student_interests = student  # Unpack student tuple
            
            student_obj = self.db_manager.get_student(student_id)
            if not student_obj:
                print(f"Student mit ID {student_id} nicht gefunden, übersprungen.")
                continue  # Skip to next student

            # Generate homework
            homework = self.hw_generator.generate_homework(student_obj, lesson)

            # Save to database
            hw_id = self.db_manager.add_homework(homework)

            # Convert tasks to string (if needed)
            tasks_str = "\n".join(homework.tasks) if isinstance(homework.tasks, list) else str(homework.tasks)

            # Generate PDF
            self.pdf_generator.generate_homework_pdf(student_obj.name, lesson.topic, date.today(), tasks_str)

            print(f"✅ Hausaufgabe (ID: {hw_id}) für {student_obj.name} erstellt.")

    def print_all_students(self):
        students = self.db_manager.get_students()
        if not students:
            print("Keine Schüler gefunden.")
            return

        print("\n===== Schülerliste =====")
        for student in students:
            student_id, name, age, interests = student
            print(f"ID: {student_id}, Name: {name}, Alter: {age}, Interessen: {interests}")
        
    def print_all_lessons(self):
        lessons=self.db_manager.get_lessons()
        if not lessons:
            print("Keine Thema gefunden.")
            return
        print("\n===== Themenliste =====")
        for lesson in lessons:
            lesson_id,topic=lesson
            print(f"ID{lesson_id},Thema{topic}")

    def print_all_homeworks(self):
        homeworks = self.db_manager.get_homeworks()  # Holt alle Hausaufgaben aus der Datenbank

        if not homeworks:
            print("Keine Hausaufgaben gefunden.")
            return

        self.print_all_students()  # Liste aller Schüler anzeigen

        try:
            choice = int(input("Welche Schüler-Hausaufgaben willst du sehen? Gib bitte seine Student_ID ein: "))
        except ValueError:
            print("Ungültige Eingabe! Bitte eine gültige Student_ID eingeben.")
            return

        student_homeworks = [hw for hw in homeworks if hw[0] == choice]  # hw[0] = student_id

        if not student_homeworks:
            print(f"Keine Hausaufgaben für den Schüler mit ID {choice} gefunden.")
            return

        student_name = student_homeworks[0][1]  # hw[1] = name des Schülers
        print(f"\n===== Hausaufgabenliste von {student_name} (ID: {choice}) =====")

        for homework in student_homeworks:
            topic=homework[6]
            homework_id = homework[2]  # homework_id
            lesson_id = homework[4]  # lesson_id
            tasks = homework[5]  # tasks

            print(f"📝 Homework ID: {homework_id}, Lesson ID: {lesson_id}")
            print(f"📝📌 ======Das Thema: {topic}=======📝📌")

            print(f"📌 Aufgaben: {tasks}\n")


if __name__ == "__main__":
    app = App(db_path="schulapp.db")  # Oder ":memory:" für In-Memory
    app.run()