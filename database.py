import sqlite3
import pandas as pd

# Database file name
DB_FILE = "hr_chatbot.db"

def create_database():
    """Creates a database and a table for storing FAQs if not exists."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faq (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT UNIQUE,
            answer TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("[INFO] Database and table created successfully.")

def load_faq_data(csv_file):
    """Loads FAQ data from a CSV file into the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Read CSV file
    faq_data = pd.read_csv(csv_file)

    # Insert each question-answer pair into the table
    for index, row in faq_data.iterrows():
        try:
            cursor.execute("INSERT INTO faq (question, answer) VALUES (?, ?)", (row['Question'], row['Answer']))
        except sqlite3.IntegrityError:
            pass  # Skip duplicates
    
    conn.commit()
    conn.close()
    print("[INFO] FAQ data loaded successfully.")

def fetch_answer(question):
    """Fetches an answer from the database based on a user's question."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT answer FROM faq WHERE question LIKE ?", ('%' + question + '%',))
    result = cursor.fetchone()

    conn.close()
    
    if result:
        return result[0]
    else:
        return "Sorry, I don't have an answer to that question."

# Run this file to create the database and load data
if __name__ == "__main__":
    create_database()
    load_faq_data("data/faq_data.csv")

