import sqlite3
from datetime import date
from typing import List,Optional
from teacher import Teacher
from student import Student
from lesson import Lesson
class DatabaseManager():

    def __init__(self,db_path=":memory:") -> None:
        self.db_path= db_path
        self.connection=None
        
    def connect(self):
        self.connection= sqlite3.connect(self.db_path)
        self.connection.execute("PRAGMA foreign_keys=ON;") # Aktiviert die fremde schlüssel Referenz

    def create_tables(self):
        with self.connection:
            self.connection.execute(        #Student Tabelle
                """
            CREATE TABLE IF NOT EXISTS student(
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            interests TEXT
            );
                """
            )
            self.connection.execute(        #Lehrer Tabelle

            """
            CREATE TABLE IF NOT EXISTS teacher(
                teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject TEXT

            );

            """
            )
            self.connection.execute(    #lesson Tabelle
                """
                CREATE TABLE IF NOT EXISTS lesson
                (
                    lesson_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lesson_date TEXT,
                    topic TEXT,
                    feedback TEXT,
                    teacher_id INTEGER,
                    FOREIGN KEY(teacher_id) REFERENCES teacher(teacher_id) ON DELETE CASCADE
                );

                """

            )
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS homework(
                
                homework_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                lesson_id INTEGER,
                tasks TEXT,
                status TEXT,
                FOREIGN KEY(student_id) REFERENCES student(student_id) ON DELETE CASCADE,
                FOREIGN KEY(lesson_id) REFERENCES lesson(lesson_id) ON DELETE CASCADE

                

                );

                """
            )

    def add_student(self, student):
        #diese methode fügt neue schülere deren alter und interessen werden durch komma getrennt
        interests_str=",".join(student.interests) if student.interests else""
        with self.connection:
            cursor= self.connection.execute(
                """
                INSERT INTO student(name,age,interests) VALUES (?,?,?);  
                """ , (student.name,student.age,interests_str)) #TODO was macht VALUES(???)
            return cursor.lastrowid  #TODO was beudetet das ?
            

    def get_student(self, student_id)->Optional[dict]:
        #diese methode gibt der Schüler Informationen und seine Interessen , falls die existieren
        cursor= self.connection.cursor()
        cursor.execute("SELECT student_id, name, age, interests FROM student WHERE student_id=?;",(student_id,)) #TODO wieso ist student_id =?;
        row= cursor.fetchone() #TODO was bedeutet das
        if not row:
            return None
            # SQLite gibt Strings zurück, daher müssen wir die Liste rekonstruieren
        interests_list = row[3].split(",") if row[3] else []
        return Student(student_id=row[0], name=row[1], age=row[2], interests=interests_list)
    
    def add_lesson(self,lesson):
        #diese Methode fügt eine neue Unterrichtstunde hinzu mit der eigenschaften datum,thema,feedback,teacher_id

        with self.connection:
            cursor= self.connection.execute(
                """
                INSERT INTO lesson(lesson_date,topic,feedback,teacher_id) VALUES(?,?,?,?);

                """, (lesson.lesson_date.isoformat(), lesson.topic,lesson.feedback,lesson.teacher_id)

            )
            return cursor.lastrowid
        
    def add_homework(self, homework) -> int:
    # Prüfe, ob der Student existiert
        cursor = self.connection.cursor()
        cursor.execute("SELECT student_id FROM student WHERE student_id=?;", (homework.student_id,))
        student_exists = cursor.fetchone()
        
        if not student_exists:
            raise ValueError(f"Fehler: Student mit ID {homework.student_id} existiert nicht!")

        # Prüfe, ob die Lesson existiert
        cursor.execute("SELECT lesson_id FROM lesson WHERE lesson_id=?;", (homework.lesson_id,))
        lesson_exists = cursor.fetchone()

        if not lesson_exists:
            raise ValueError(f"Fehler: Lesson mit ID {homework.lesson_id} existiert nicht!")

        # Falls beide existieren, füge die Hausaufgabe ein
        with self.connection:
            cursor = self.connection.execute(
                """
                INSERT INTO homework (student_id, lesson_id, tasks, status) VALUES (?, ?, ?, ?);
                """,
                (homework.student_id, homework.lesson_id, homework.tasks, homework.status)
            )
        return cursor.lastrowid

        
    def add_teacher(self, teacher: Teacher) -> int:
        with self.connection:
            cursor = self.connection.execute("""
                INSERT INTO teacher (name, subject) VALUES (?, ?);
            """, (teacher.name, teacher.subject))
            teacher_id = cursor.lastrowid
            teacher.teacher_id = teacher_id
        return teacher_id
        
    def mark_homework_done(self,homework_id):
        with self.connection:
            self.connection.execute(
                """
                UPDATE homework SET status = 'done' WHERE homework_id=?;

                """,(homework_id,)
            )

    def delete_student(self, student_id):
        #das löscht ein schüler aus der Datenbank und seinen Hausaufgaben
        
        with self.connection:
            self.connection.execute("DELETE FROM student WHERE student_id=?;",(student_id))

    def delete_lesson(self,lesson_id):

        with self.connection:
            self.connection.execute("DELETE FROM lesson WHERE lesson_id=?;",(lesson_id))

    def get_all_students(self):
        cursor= self.connection.cursor()
        cursor.execute("SELECT homework_id,student_id,lesson_id,tasks,status")
        rows=cursor.fetchall()
        return [{"student_id": row[0], "name": row[1], "age": row[2], "interests": row[3].split(",")} for row in rows]
    def close_connection(self):
        """Schließt die Verbindung zur Datenbank."""
        if self.connection:
            self.connection.close()
    def get_students(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT student_id, name, age, interests FROM student;")  # 🔹 Richtig: SELECT-Abfrage ausführen
        rows = cursor.fetchall()  # 🔹 Alle Ergebnisse abrufen
        return rows
    
    def get_lessons(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT lesson_id, topic FROM lesson;")  # 🔹 Richtig: SELECT-Abfrage ausführen
        rows = cursor.fetchall()  # 🔹 Alle Ergebnisse abrufen
        return rows
    def get_lesson(self, lesson_id):
        """Retrieve a specific lesson by lesson_id."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT lesson_id,lesson_date,topic,feedback, teacher_id FROM lesson WHERE lesson_id = ?;", (lesson_id,))
        row = cursor.fetchone()  # 🔹 Get one lesson

        if row is None:
            return None  # If no lesson is found, return None

        return Lesson(row[0], row[1], row[2], row[3],row[4])  # Create a Lesson object
    def get_homeworks(self):
        cursor = self.connection.cursor()
        cursor.execute("""SELECT s.student_id,s.name,h.homework_id, h.student_id, h.lesson_id, h.tasks,l.topic
                          FROM homework h
                          JOIN student s,lesson l ON h.student_id= s.student_id;""")  # 🔹 Richtig: SELECT-Abfrage ausführen
        rows = cursor.fetchall()  # 🔹 Alle Ergebnisse abrufen
        return rows
