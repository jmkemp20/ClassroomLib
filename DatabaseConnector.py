from bson import ObjectId
from pymongo import MongoClient
import json


class DatabaseConnector:
    def __init__(self, url):
        self.client = MongoClient(url)
        self.db = self.client.ClassroomLibDB

    def upload_students(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as read_file:
            data = json.load(read_file)

        count = 0
        for student in data['students']:
            self.db.ClassroomStudents.insert_one(student)
            print('Pushed {0} of {1} with title: {2}'.format(count, len(data['students']), student['name']))
            count += 1

    def upload_books(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as read_file:
            data = json.load(read_file)
        count = 0
        for book in data:
            self.db.ClassroomBooks.insert_one(book)
            print('Pushed {0} of {1} with title: {2}'.format(count, len(data), book['title']))
            count += 1

    def get_students(self):
        students = []
        for student in self.db.ClassroomStudents.find():
            students.append(student)
        return students

    def get_student_book_list(self, uid):
        query = {
            '_id': ObjectId(uid)
        }
        student = self.db.ClassroomStudents.find_one(query)
        return student['book_list']

    def isbn_in_lib(self, isbn):
        for book in self.db.ClassroomBooks.find():
            if str(book['isbn10']) == isbn or str(book['isbn13']) == isbn:
                return True
        return False

    def id_in_lib(self, uid):
        query = {
            '_id': ObjectId(uid)
        }
        book = self.db.ClassroomBooks.find_one(query)
        if book is not None:
            return True
        return False

    def get_id_from_isbn(self, isbn):
        for book in self.db.ClassroomBooks.find():
            if str(book['isbn10']) == isbn or str(book['isbn13']) == isbn:
                return book['_id']
        return -1

    def get_info_from_id(self, uid):
        query = {
            '_id': ObjectId(uid)
        }
        temp_dict = {
            "_id": '',
            "authors": '',
            "title": '',
            "description": '',
            "publisher": '',
            "publish_date": '',
            "pages": '',
            "isbn10": '',
            "isbn13": ''
        }
        book = self.db.ClassroomBooks.find_one(query)
        if book is not None:
            temp_dict['_id'] = str(book['_id'])
            temp_dict['authors'] = str(book['authors'])
            temp_dict['title'] = str(book['title'])
            temp_dict['description'] = str(book['description'])
            temp_dict['publisher'] = str(book['publisher'])
            temp_dict['publish_date'] = str(book['publish_date'])
            temp_dict['pages'] = str(book['pages'])
            temp_dict['isbn10'] = str(book['isbn10'])
            temp_dict['isbn13'] = str(book['isbn13'])
            return temp_dict
        return None


dc = DatabaseConnector(
    "mongodb+srv://jmkemp20:jajabinks@classroomlibdb.rpwpl.mongodb.net/ClassroomLibDB?retryWrites=true&w=majority")

students = dc.get_students()
print(students)

print(dc.isbn_in_lib("9780142426425"))

dc.get_student_book_list('6116bfa4c27f2dd4b26ec72a')

print(dc.get_info_from_id(dc.get_id_from_isbn('9781250091666')))
