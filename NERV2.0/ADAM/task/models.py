######################################
# Time:2020/02/11
# alter: ZWQ
######################################

from common import db


class ToDoList(db.Model):
    __tablename__ = 'todolist'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120) ,nullable=False)
    taskname = db.Column(db.String(120),nullable=False)
    accomplish = db.Column(db.Boolean,nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_task_by_username(cls, username):
        result = cls.query.filter_by(username=username)
        task_list = list()
        for i in result:
            task_list.append(i)
        return task_list

    @classmethod
    def update_task(cls,id,new_task_name,accomplish):
        result = cls.query.filter(cls.id==id).first()
        result.taskname = new_task_name
        result.accomplish = accomplish
        db.session.commit()

    @classmethod
    def del_task(cls,id):
        result = cls.query.filter_by(id=id).first()
        db.session.delete(result)
        db.session.commit()