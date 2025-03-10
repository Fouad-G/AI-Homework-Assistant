from datetime import date 
class Lesson():
    def __init__(self,lesson_id,lesson_date:date,topic, feedback,teacher_id) -> None:
        self.lesson_id=lesson_id
        self.lesson_date = lesson_date
        self.topic = topic
        self.feedback = feedback
        self.teacher_id = teacher_id
        
    def add_feedback(self,feedback):
        self.feedback=feedback