class author:
    def __init__(self, id, name:):
        self.id = id
        self.name = name


    def save(self):
        if self.name is None or len(self.name.strip()) == 0:
            raise ValueError("Author name cannot be empty")

        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
        conn.commit()
        conn.close()


    def delete(self):
         if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM authors WHERE id = ?", (self.id,))
            conn.commit()
            conn.close()

    
@classmethod
def get_by_id(cls, id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return cls(id=row[0], name=row[1])
    else:
        return None



    def get_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        rows = cursor.fetchone()
        conn.close()
        if rows is None
            return None
        else:
            return cls(id=row[i'd'], name=row['name'])








        
