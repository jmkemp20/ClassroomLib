import json
import ISBNParser as ip


class BookParserJSON:
    def __init__(self, file_path):
        self.file_path = file_path

        with open(file_path, 'r', encoding='utf-8') as read_file:
            self.data = json.load(read_file)
        print("validating library json data...")

        if self.validate_json():
            print("validation complete")
        else:
            print("Invalid JSON Data")

    def validate_json(self):
        for book in self.data:
            if not ip.valid_isbn13(str(book['isbn13'])) and not ip.valid_isbn10(str(book['isbn10'])):
                print(book['title'] + " " + str(book['isbn10']) + " " + str(book['isbn13']))
                return False
        return True

    def get_title(self, isbn):
        for book in self.data:
            if str(book['isbn13']) == isbn or str(book['isbn10']) == isbn:
                return book['title']
        return ""

    def get_author(self, isbn):
        for book in self.data:
            if str(book['isbn13']) == isbn or str(book['isbn10']) == isbn:
                return book['authors']
        return ""

    def get_publisher(self, isbn):
        for book in self.data:
            if str(book['isbn13']) == isbn or str(book['isbn10']) == isbn:
                return book['publisher']
        return ""

    def get_publish_date(self, isbn):
        for book in self.data:
            if str(book['isbn13']) == isbn or str(book['isbn10']) == isbn:
                return book['publish_date']
        return ""

    def get_pages(self, isbn):
        for book in self.data:
            if str(book['isbn13']) == isbn or str(book['isbn10']) == isbn:
                return book['pages']
        return ""

    def get_description(self, isbn):
        for book in self.data:
            if str(book['isbn13']) == isbn or str(book['isbn10']) == isbn:
                return book['description']
        return ""

    def isbn_in_library(self, isbn):
        for book in self.data:
            if str(book['isbn13']) == isbn or str(book['isbn10']) == isbn:
                return True
        return False
