class Magazine():
      def __init__(self, id, name, category):
            self.id = id
            self.name = name
            self.category = category

   def save(self):
    if self.nem is None or len(self.name.strip()) == 0:
        raise ValueError("Magazine name cannot be empty")
    if self.category is None or len(self.category.strip()) == 0:
        raise ValueError("Magazine category cannot be empty")

    conn = get_connection()
    cursor = conn.cursor() 
    if self.id is None:
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
        self.id = cursor.lastrowid
    else:
        cursor.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", (self.name, self.category, self.id))
    conn.commit()
    conn.close()

    
    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return None
        return cls(id=row['id'], name=row['name'], category=row['category'])
    

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return None
        return cls(id=row['id'], name=row['name'], category=row['category'])


     @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row['id'], name=row['name'], category=row['category']) for row in rows]


    