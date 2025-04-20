import json
import os

data_file = "library.txt"

def load_library():
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            return json.load(file)
    return []

def save_library(library):
    with open(data_file, "w") as file:
        json.dump(library, file)

def add_book(library):
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    year = input("Enter publication year: ")
    genre = input("Enter book genre: ")
    read = input("Have you read this book? (yes/no): ").lower() == "yes"

    new_book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read
    }
    library.append(new_book)
    save_library(library)
    print(f"Book '{title}' added to your library.")

def remove_book(library):
    title = input("Enter the title of the book to remove: ")
    for book in library:
        if book["title"].lower() == title.lower():
            library.remove(book)
            save_library(library)
            print(f"Book '{title}' removed from your library.")
            return
    print(f"Book '{title}' not found in your library.")

def search_book(library):
    search_term = input("Enter a title, author, or genre to search: ").lower()
    results = [book for book in library if (search_term in book["title"].lower() or
                                             search_term in book["author"].lower() or
                                             search_term in book["genre"].lower())]
    if results:
        print("Search results:")
        for book in results:
            read_status = "Read" if book["read"] else "Not Read"
            print(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} [{read_status}]")
    else:
        print("No books found!")
def display_books(library):
    if library:
        print("Your library:")
        for book in library:
            read_status = "Read" if book["read"] else "Not Read"
            print(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} [{read_status}]")
    else:
        print("Your library is empty.")

def display_statistics(library):
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    percentage_read_books = (read_books / total_books * 100) if total_books > 0 else 0
    print(f"Total books: {total_books}")
    print(f"percentage of read books: {percentage_read_books:.2f}%")

def main():
    library = load_library()
    while True:
        print("\n Welcome to your Personal Library Manager!")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Search Book")
        print("4. Display Books")
        print("5. Display Statistics")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")
        if choice == "1":
            add_book(library)
        elif choice == "2":
            remove_book(library)
        elif choice == "3":
            search_book(library)
        elif choice == "4":
            display_books(library)
        elif choice == "5":
            display_statistics(library)
        elif choice == "6":
            print("Library saved to file. Goodbye!")
            save_library(library)
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


