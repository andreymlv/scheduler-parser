from subject import Subject
import json

class Group(object):
        def __init__(self, group_name):
            self.subjects = {}
            self.name = group_name
        
        def add_subject(self, subject_name , start_time , is_even , day):
            subs = self.subjects.get(day)
            s = Subject(subject_name, start_time, is_even)
            if(subs == None):
                self.subjects.update({day:[s]})
            else:
                subs.append(s)

        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
