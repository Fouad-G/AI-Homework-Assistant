class Homework():
    def __init__(self, homework_id, student_id, lesson_id, tasks):
        self.homework_id = homework_id
        self.student_id = student_id
        self.lesson_id = lesson_id
        self.tasks = tasks
        self.status = "open"

    def mark_done(self):
        self.status = "done"