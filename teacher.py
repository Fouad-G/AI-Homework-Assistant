from lesson import Lesson
from datetime import date 

class Teacher():
    def __init__(self, teacher_id,name, subject):
        self.teacher_id = teacher_id
        self.name = name
        self.subject = subject

    def create_Lesson(self,topic):
        return Lesson(None,date.today(),topic,"",self.teacher_id)
    
    def review_homework(self, homework, feedback: str):
        # Hier könnte man Status ändern, Punkte vergeben usw.
        homework.status = "reviewed"
        print(f"Teacher {self.name} reviewed homework {homework.homework_id} with feedback: {feedback}")
