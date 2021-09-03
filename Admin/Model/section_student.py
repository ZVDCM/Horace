class SectionStudent:

    def __init__(self, Model):
        self.Model = Model
        self.Section = Model.Section
        self.TableModel = Model.TableModel
        self.Database = Model.Database

    # Section
    def get_all_section(self):
        db = self.Database.connect()
        cursor = db.cursor()

        select_query = "SELECT * FROM Sections ORDER BY ID"
        cursor.execute(select_query)

        sections = cursor.fetchall()

        cursor.close()
        db.close()

        if sections:
            return [self.Model.Section(*section) for section in sections]
        return None
    
    def get_section(self, name):
        db = self.Database.connect()
        cursor = db.cursor()

        select_query = "SELECT * FROM Sections WHERE Name=%s"
        cursor.execute(select_query, (name,))

        section = cursor.fetchone()

        cursor.close()
        db.close()

        if section:
            return self.Model.Section(*section)
        return None

    def create_section(self, name):
        db = self.Database.connect()
        cursor = db.cursor()

        insert_query = "INSERT INTO Sections (Name) VALUES (%s)"
        cursor.execute(insert_query, (name,))
        db.commit()

        cursor.close()
        db.close()

    def edit_section(self, section):
        db = self.Database.connect()
        cursor = db.cursor()

        update_query = "UPDATE Sections SET Name=%s WHERE ID=%s"
        cursor.execute(update_query, (section.Name, section.ID))
        db.commit()

        cursor.close()
        db.close()

    def delete_section(self, section):
        db = self.Database.connect()
        cursor = db.cursor()

        delete_query = "DELETE FROM Sections WHERE ID=%s"
        cursor.execute(delete_query, (section.ID,))
        db.commit()

        cursor.close()
        db.close()