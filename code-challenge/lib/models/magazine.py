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