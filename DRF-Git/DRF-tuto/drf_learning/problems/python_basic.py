# 1. Defines a dictionary representing a book with: id, title, author, price 
# 2. Creates a function that takes book data and returns a formatted string 
# 3. Creates a list of 3 books 
# 4. Prints information about each book

book1 = { "id": 1, "title": "python", "author": "abc", "price": 100}
book2 = { "id": 2, "title": "java", "author": "xyz", "price": 200}
book3 = { "id": 3, "title": ".Net", "author": "pqr", "price": 300}

def bookDetails(book):
    return f" {book['title']} : author - {book['author']}, price - {book['price']}"

Books = [book1, book2, book3]

for B in Books:
    print(bookDetails(B))