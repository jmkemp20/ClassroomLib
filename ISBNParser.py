import requests


def get_info(isbn):
    info_list = []

    url = "https://openlibrary.org/isbn/" + isbn + ".json"
    print(url)
    r = requests.get(url)

    book_json = r.json()
    try:
        book_title = str(book_json["title"])
    except KeyError:
        book_title = ""
    try:
        book_isbn10 = str(book_json["isbn_10"][0])
    except KeyError:
        book_isbn10 = ""
    try:
        book_isbn13 = str(book_json["isbn_13"][0])
    except KeyError:
        book_isbn13 = ""
    try:
        author_key = book_json["authors"][0]["key"]
        url = "https://openlibrary.org" + author_key + ".json"
        r = requests.get(url)

        author_json = r.json()

        temp_author = str(author_json["name"]).split()
        book_author = temp_author[len(temp_author) - 1]
    except KeyError:
        book_author = ""

    info_list.append(book_author)
    info_list.append(book_title)
    info_list.append(book_isbn10)
    info_list.append(book_isbn13)

    return info_list


def to_isbn13(isbn10):
    if valid_isbn10(isbn10):
        total = 0
        isbn13 = "978" + str(isbn10[:len(isbn10) - 1])
        for i in range(len(isbn13)):
            digit = int(isbn13[i])
            total += digit * (3 if is_odd(i) else 1)
        checkdigit = (10 - total % 10) % 10
        isbn13 += str(checkdigit)
        if valid_isbn13(isbn13):
            return isbn13
    return -1


# : Meant to convert valid ISBN10 IFF (ISBN13 is valid AND ISBN10 does not exist)
def to_isbn10(isbn13):
    if valid_isbn13(isbn13):
        # Need to remove first three digits and calc 10th digit
        isbn10 = isbn13[3:len(isbn13) - 1]
        total = 0
        for i in range(len(isbn10)):
            digit = int(isbn10[i])
            total += (i + 1) * digit
        d10 = total % 11
        if d10 == 10:
            d10 = 'X'
        isbn10 += str(d10)
        if valid_isbn10(isbn10):
            return isbn10
    return -1


def valid_isbn10(isbn10):
    if len(isbn10) == 10:
        total = 0
        for i in range(len(isbn10) - 1):
            digit = int(isbn10[i])
            total += (10 - i) * digit
        if isbn10[9] == 'X' or isbn10[9] == 'x':
            total += 10
        else:
            total += int(isbn10[9])
        return total % 11 == 0
    return False


def valid_isbn13(isbn13):
    if len(isbn13) == 13:
        if isbn13[:3] == '978':
            total = 0
            for i in range(len(isbn13)):
                digit = int(isbn13[i])
                total += digit * (3 if is_odd(i) else 1)
            remainder = (10 - total % 10) % 10
            if remainder == 0:
                return True
    return False


def fix_isbn10(isbn10):
    temp_isbn = isbn10
    if len(temp_isbn) == 8:  # Missing proceed 0?
        temp_isbn = "0" + str(temp_isbn)
    if len(temp_isbn) == 9:  # Missing proceeding 0
        temp_isbn = "0" + temp_isbn
        if valid_isbn10(temp_isbn):
            return temp_isbn
    elif len(temp_isbn) == 10:  # Need to verify isbn10
        if valid_isbn10(temp_isbn):
            return temp_isbn
        # DO NOT want to recalc 10th here -- must use isbn13
    return -1


def is_odd(num):
    return num % 2 != 0
