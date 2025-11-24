# Create a Python dictionary with book data
# Convert it to JSON string
# Convert JSON string back to dictionary
# Print the result
import json

Book = { "id": 1, "title": "python", "author": "abc", "price": 100, "published": True }

bookDetails = json.dumps(Book)
print("json formate: ", bookDetails)

bookDict = json.loads(bookDetails)
print("dict: ", bookDict)