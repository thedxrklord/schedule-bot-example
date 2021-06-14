import json
import urllib.request


class Schedule:
    base_url = 'https://schedule.dxrk.dev/api/'
    university_id = None
    faculty_id = None
    department_id = None

    def __init__(self, university_id=None, faculty_id=None, department_id=None):
        if university_id:
            self.university_id = university_id
        if faculty_id:
            self.faculty_id = faculty_id
        if department_id:
            self.department_id = department_id
        pass

    def universities(self):
        with urllib.request.urlopen(self.base_url + 'universities') as url:
            data = json.loads(url.read().decode())
            return data

    def name_by_id(self, _id):
        universities = self.universities()
        for university in universities:
            if int(university['id']) == int(_id):
                return university['short_name']
        return None

    def get_university_faculties(self):
        with urllib.request.urlopen(self.base_url + 'university/' + self.university_id + '/faculties') as url:
            data = json.loads(url.read().decode())
            return data

    def get_faculty_departments(self):
        with urllib.request.urlopen(self.base_url + 'faculty/' + self.faculty_id + '/departments') as url:
            data = json.loads(url.read().decode())
            return data

    def get_department_teachers(self):
        with urllib.request.urlopen(self.base_url + 'department/' + self.department_id + '/teachers') as url:
            data = json.loads(url.read().decode())
            return data

    def get_department_groups(self):
        with urllib.request.urlopen(self.base_url + 'department/' + self.department_id + '/groups') as url:
            data = json.loads(url.read().decode())
            return data

    def get_group_schedule(self, group_id, date):
        with urllib.request.urlopen(self.base_url + 'group/' + group_id + '/lessons-normal-short-names?dateFrom=' + date + '&dateTo=' + date) as url:
            data = json.loads(url.read().decode())
            return data

    def get_university_groups(self):
        with urllib.request.urlopen(self.base_url + 'university/' + self.university_id + '/groups') as url:
            data = json.loads(url.read().decode())
            return data

    def get_teacher_schedule(self, teacher_id, date):
        with urllib.request.urlopen(self.base_url + 'teacher/' + teacher_id + '/lessons-normal-short-names?dateFrom=' + date + '&dateTo=' + date) as url:
            data = json.loads(url.read().decode())
            return data
