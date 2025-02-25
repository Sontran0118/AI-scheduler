import sqlite3

def create_database():
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS Courses (
                        course_id TEXT PRIMARY KEY,
                        course_name TEXT,
                        credits INTEGER
                      )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Requirements (
                        requirement_id TEXT PRIMARY KEY,
                        requirement_type TEXT,
                        description TEXT
                      )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Specializations (
                        specialization_id TEXT PRIMARY KEY,
                        specialization_name TEXT,
                        description TEXT
                      )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Course_Requirements (
                        course_id TEXT,
                        requirement_id TEXT,
                        FOREIGN KEY (course_id) REFERENCES Courses(course_id),
                        FOREIGN KEY (requirement_id) REFERENCES Requirements(requirement_id)
                      )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Specialization_Courses (
                        specialization_id TEXT,
                        course_id TEXT,
                        FOREIGN KEY (specialization_id) REFERENCES Specializations(specialization_id),
                        FOREIGN KEY (course_id) REFERENCES Courses(course_id)
                      )''')
    
    conn.commit()
    conn.close()

def parse_and_store_data(filename):
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()
    
    with open(filename, "r") as file:
        section = None
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                section = line.lstrip("# ") if line.startswith("#") else section
                continue
            
            data = line.split("|")
            
            if section == "COURSES":
                cursor.execute("INSERT OR IGNORE INTO Courses VALUES (?, ?, ?)", (data[0], data[1], int(data[2])))
                
            elif section == "REQUIREMENTS":
                cursor.execute("INSERT OR IGNORE INTO Requirements VALUES (?, ?, ?)", (data[0], data[1], data[2]))
                
            elif section == "SPECIALIZATIONS":
                cursor.execute("INSERT OR IGNORE INTO Specializations VALUES (?, ?, ?)", (data[0], data[1], data[2]))
                
            elif section == "COURSE_REQUIREMENTS":
                cursor.execute("INSERT OR IGNORE INTO Course_Requirements VALUES (?, ?)", (data[0], data[1]))
                
            elif section == "SPECIALIZATION_COURSES":
                cursor.execute("INSERT OR IGNORE INTO Specialization_Courses VALUES (?, ?)", (data[0], data[1]))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    parse_and_store_data("course_requirements.txt")
    print("Data successfully stored in database.")
