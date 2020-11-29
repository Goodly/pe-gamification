from sqlalchemy import create_engine
from event_model.task_run import TaskRun
from event_model.project import Project
from event_model.user import User
from event_model.task import Task
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
import csv

engine = create_engine("postgresql://pe_dashboard:test-only-yVu8W5azUtZ8RPSWX42o@localhost:5432/pe_dashboard", echo=True)
Session = sessionmaker(bind = engine)
session = Session()

#so i don't go crazy reading the traceback in terminal
for i in range(1000):
    print(" ")

"""
code to print out tables
m = MetaData()
m.reflect(engine)
for table in m.tables.values():
    print(table.name)
    #for column in table.c:
      #  print(column.name)
"""

with open('event_model/tr_with_proj.csv', newline='') as pscfile:
    reader = csv.DictReader(pscfile)
    for row in reader:
        #run query on user table, if empty, then add new user (result == None)
        in_user = session.query(User).filter(User.id == row['user_id']).first()
        if in_user == None:
            u = User(id = row['user_id'], name = 'test' + row['user_id'], email_addr = row['user_id'] + '@gmail.com')
            session.add(u)
            session.commit()
        #if project not in project table, then ->
        in_proj = session.query(Project).filter(Project.id == row['project_id']).first()
        if in_proj == None:
            p = Project(id = row['project_id']) #right now this is just a filler value of 4
            session.add(p)
            session.commit()
        #if task not in task table, then ->
        in_task = session.query(Task).filter(Task.id == row['task_id']).first()
        if in_task == None:
            t = Task(id = row['task_id'], project_id = row['project_id'])
            session.add(t)
            session.commit()
        #finally, create task run 
        tr = TaskRun(created = row['created'], project_id = row['project_id'], task_id = row['task_id'],
             user_id = row['user_id'], finish_time = row['finish_time'],
             task_type = row['task_type'])
        session.add(tr)
    session.commit()

#print out to see our baby :')
result = engine.execute('SELECT * FROM '
                            '"taskrun"')
for r in result:
    print(r)