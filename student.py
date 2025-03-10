class Student():
    def __init__(self,student_id, name,age,interests) -> None:
        self.student_id= student_id
        self.name= name
        self.age= age
        self.interests=interests if interests else[] 
        self.feedback_log=[]

    def get_profile(self):
        return f"Name:{self.name}, Age:{self.age}, Interests:{','.join(self.interests)}"
    
    def add_feedback(self,feedback):
        self.feedback_log.append(feedback)
