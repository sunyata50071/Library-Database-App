# Bookstore database app. A clerk can add, remove, update and delete stock.

import sqlite3

# Create the database file.
b_db = sqlite3.connect("ebookstore.db")

# Get cursor.
cursor = b_db.cursor() 

# Create the table and fields.
cursor.execute("""
    CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY, title TEXT, author TEXT,
               qty INTEGER)
""")
b_db.commit()  # Commit transaction.

# Add records. 'or ignore' stops an error when the program runs again. 
cursor.execute("""
    INSERT OR IGNORE INTO book VALUES
        (3001, "A Tale of Two Cities", "Charles Dickens", 30),
        (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
        (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25),
        (3004, "The Lord of the Rings", "J.R.R. Tolkein", 37),
        (3005, "Alice in Wonderland", "Lewis Carroll", 12)  
""")
b_db.commit()

while True:
    clerk_options = input("""\nSelect an option:
        1 - Enter book
        2 - Update book
        3 - Delete book
        4 - Search books
        0 - Exit                  
        """)
    if clerk_options == "1":
        try:
            b_db = sqlite3.connect("ebookstore.db")
            cursor = b_db.cursor()
            book_id = input("Enter a unique ID number for the book: ")
            book_title = input("Enter the books title: ")
            author = input("Enter the books author: ").title()
            qty = int(input("How many copies of this book are there? "))
            cursor.execute("""
            INSERT INTO book(id, title, author, qty)
            VALUES (?, ?, ?, ?)
            """, (book_id, book_title, author, qty))
            b_db.commit()
            b_db.close()
            print("\nThe book has been successfully added!")
        except Exception as e:
            b_db.rollback()  # revert back to the state before the error.
            print("\nThis title could not be added. Check the details are correct!")
    
    elif clerk_options == "2":
        try:
            b_db = sqlite3.connect("ebookstore.db")
            cursor = b_db.cursor()
            cursor.execute("""SELECT * FROM book""")
            records = cursor.fetchall()  # Create variable to print all records.
            b_db.commit()
            print(f"Titles currently in stock: {records}\n")
            title_check = []  # Create a list used for checking titles.
            for rows in records:
                titles = rows[0]  # Get the first field in a variable.
                title_check.append(titles)  # Add IDs to the list.
            title_to_update = int(input("Enter the ID for the title you want to update: "))
            if title_to_update in title_check:
                update_qty = int(input("\nWhat should the quantity be?: "))
                cursor.execute("""
                UPDATE book SET qty = ? WHERE id = ?
                """, (update_qty, title_to_update))
                b_db.commit()
                b_db.close()
                # Only permit qty update.
                # If title or author needs changing user can delete the row and add a new row.
                # This avoids data discrepancies creeping in later.
                print("\nThe quantity of this title has been updated!")
            else:
                print("\nThat's not a valid ID")
        except ValueError as e:
            b_db.rollback()
            print("\nThis title could not be updated!")

    elif clerk_options == "3":
        b_db = sqlite3.connect("ebookstore.db")
        cursor = b_db.cursor()
        cursor.execute("""SELECT * FROM book""")
        stock_list = cursor.fetchall()  # Create a variable for showing stock list.
        b_db.commit()
        print(f"Current Stock List: {stock_list}\n")
        id_check = []  # Create a variable used for checking user input.
        for rows in stock_list:
            id = rows[0]
            id_check.append(id)
        title_to_delete = int(input("Enter the ID for the title you want to delete: "))
        if title_to_delete in id_check:
            cursor.execute("""DELETE FROM book WHERE id = ?""", (title_to_delete,))
            b_db.commit()
            b_db.close()
            print("\nThis book has been successfully deleted!")
        else:
            print("\nThat is not a valid ID!")

    elif clerk_options == "4":
        book_search_method = input("Enter 't' to search by title or 'a' by author: ")
        if book_search_method == "t":
            search_book_title = input("Enter the book title: ")
            b_db = sqlite3.connect("ebookstore.db")
            cursor = b_db.cursor()
            cursor.execute("""
            SELECT * FROM book WHERE title = ?
            """, (search_book_title,))
            title_availability = cursor.fetchall()
            b_db.commit()
            print(f"\nTitles in stock: {title_availability}")
        if book_search_method == "a":
            search_books_by_author = input("Who is the author?: ").title()
            b_db = sqlite3.connect("ebookstore.db")
            cursor = b_db.cursor()
            cursor.execute("""
            SELECT * FROM book WHERE author = ?
            """, (search_books_by_author,))
            author_availability = cursor.fetchall()
            b_db.commit()
            print(f"\nAvailable books by this author: {author_availability}")

    elif clerk_options == "0":
        print("Exiting the app....")
        break
        
    else:
        print("\ninvalid input!")

    b_db.close()  # Close the database connection.
    