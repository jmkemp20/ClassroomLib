import csv


class BookParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.fields = []
        self.books = []

        # : These must be changed depending on books.csv
        self.author_row = 0
        self.title_row = 1
        self.isbn10_row = 3
        self.isbn13_row = 4

        with open(file_path) as csv_file:
            self.csv_lib = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in self.csv_lib:
                if line_count == 0:
                    self.fields = row
                    #self.fields.append("available")
                else:
                    #row.append(row[2])
                    self.books.append(row)
                line_count += 1

        # TODO In the future, verify each ISBN 10 and 13 and use the other to calculate itself if invalid
        self.fixISBN10()
        self.fixISBN13()

    def fixISBN10(self):
        for row in range(len(self.books)):
            isbn10 = self.books[row][self.isbn10_row]
            # : Trailing 0
            if len(isbn10) == 8:
                self.books[row][self.isbn10_row] = "0" + isbn10
            isbn10 = self.books[row][self.isbn10_row]
            # : Calculate 10th digit
            if len(isbn10) == 9:
                total = 0
                for i in range(len(isbn10)):
                    num = int(isbn10[i])    # The i'th character in the string converted to integer
                    total += (i+1) * num
                d10 = total % 11
                self.books[row][self.isbn10_row] = isbn10 + str(d10)

    def fixISBN13(self):
        for row in range(len(self.books)):
            if len(self.books[row][self.isbn13_row]) != 13:
                isbn10 = self.books[row][self.isbn10_row]
                isbn10 = isbn10[:len(isbn10) - 1]   # Removes check digit
                isbn13 = "978" + isbn10

                sum = 0
                for i in range(len(isbn13)):
                    digit = int(isbn13[i])
                    sum += digit * (3 if self.is_odd(i) else 1)
                checkdigit = (10 - sum % 10) % 10
                self.books[row][self.isbn13_row] = isbn13 + str(checkdigit)

    def is_odd(self, num):
        return num % 2 != 0

    def print_rows(self):
        for i in range(len(self.books)):
            print(self.books[i])

    def print_fields(self):
        print(self.fields)

    def valid_isbn(self, isbn):
        for row in range(len(self.books)):
            if self.books[row][self.isbn10_row] == isbn or self.books[row][self.isbn13_row] == isbn:
                return True
        return False

    def get_title(self, isbn):
        for row in range(len(self.books)):
            if self.books[row][self.isbn10_row] == isbn or self.books[row][self.isbn13_row] == isbn:
                return self.books[row][self.title_row]
        return ""

    def get_author(self, isbn):
        for row in range(len(self.books)):
            if self.books[row][self.isbn10_row] == isbn or self.books[row][self.isbn13_row] == isbn:
                return self.books[row][self.author_row]
        return ""
