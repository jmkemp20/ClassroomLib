import csv


class BookParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.fields = []
        self.books = []
        with open(file_path) as csv_file:
            self.csv_lib = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in self.csv_lib:
                if line_count == 0:
                    self.fields = row
                    self.fields.append("available")
                else:
                    row.append(row[2])
                    self.books.append(row)
                line_count += 1
        self.fixISBN10()

    def fixISBN10(self):
        for row in range(len(self.books)):
            isbn10 = self.books[row][3]
            # : Trailing 0
            if len(isbn10) == 8:
                self.books[row][3] = "0" + isbn10
            isbn10 = self.books[row][3]
            # : Calculate 10th digit
            if len(isbn10) == 9:
                total = 0
                for i in range(len(isbn10)):
                    num = int(isbn10[i])    # The i'th character in the string converted to integer
                    total += (i+1) * num
                d10 = total % 11
                self.books[row][3] = isbn10 + str(d10)

    def print_rows(self):
        for i in range(len(self.books)):
            print(self.books[i])

    def print_fields(self):
        print(self.fields)

    def valid_isbn(self, isbn):
        for row in range(len(self.books)):
            if self.books[row][3] == isbn:
                return True
        return False

    def get_title(self, isbn):
        for row in range(len(self.books)):
            if self.books[row][3] == isbn:
                return self.books[row][1]
        return ""

    def get_author(self, isbn):
        for row in range(len(self.books)):
            if self.books[row][3] == isbn:
                return self.books[row][0]
        return ""
