import re
from Admin.Misc.Functions.hash import *


class ClassMember:

    def __init__(self, Model):
        self.Model = Model
        self.Class = Model.Class
        self.ClassTeacher = Model.ClassTeacher
        self.Teacher = Model.Teacher
        self.ClassSection = Model.ClassSection
        self.Section = Model.Section
        self.TableModel = Model.TableModel
        self.ListModel = Model.ListModel
        self.Database = Model.Database

    def get_all_class(self):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Classes ORDER BY ID"
        cursor.execute(select_query)

        classes = cursor.fetchall()

        cursor.close()
        db.close()

        if classes:
            return [self.Class(*_class) for _class in classes]
        return []

    def create_class(self, code, name, start, end):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Classes WHERE Code=%s"
        cursor.execute(select_query, (code,))

        class_exist = cursor.fetchone()
        res = "exists"

        if not class_exist:
            insert_query = "INSERT INTO Classes (Code, Name, Start, End) VALUES (%s,%s,%s,%s)"
            cursor.execute(
                insert_query, (code, name, start, end))
            db.commit()

            res = "successful"

        cursor.close()
        db.close()

        return res

    def edit_class(self, id, code, name, start, end):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Classes WHERE Code=%s"
        cursor.execute(select_query, (code,))

        class_exist = cursor.fetchone()
        res = "exists"

        if not class_exist:
            update_query = "UPDATE Classes SET Code=%s, Name=%s, Start=%s, End=%s WHERE ID=%s"
            cursor.execute(update_query, (code, name, start, end, id))
            db.commit()

            res = "successful"

        cursor.close()
        db.close()

        return res

    def delete_class(self, Class):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        delete_query = "DELETE FROM Classes WHERE ID=%s AND Code=%s"
        cursor.execute(delete_query, (Class.ID, Class.Code))
        db.commit()

        cursor.close()
        db.close()

        return 'successful'

    # *Class Teacher
    def get_target_class_teacher(self, Class):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT ID, Code, Teacher FROM Class_Teachers WHERE Code=%s ORDER BY ID"
        cursor.execute(select_query, (Class.Code,))

        class_teachers = cursor.fetchall()

        cursor.close()
        db.close()

        if class_teachers:
            return [self.ClassTeacher(*class_teacher) for class_teacher in class_teachers]
        return []
    
    def get_teacher_not_in_class(self, Class):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = """
            SELECT UserID, Username, Salt, Hash FROM Users WHERE Privilege=%s
            AND Username NOT IN (SELECT Teacher FROM Class_Teachers WHERE Code=%s);
        """
        cursor.execute(select_query, ('Teacher', Class.Code))

        teachers_not_in_class = cursor.fetchall()

        cursor.close()
        db.close()

        if teachers_not_in_class:
            return [self.Teacher(*teacher_not_in_class) for teacher_not_in_class in teachers_not_in_class]
        return []

    def register_teacher_class(self, Class, Teacher):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        insert_query = "INSERT INTO Class_Teachers (Code, Teacher) VALUES (%s,%s)"
        cursor.execute(
            insert_query, (Class.Code, Teacher.Username))
        db.commit()

        cursor.close()
        db.close()

        return 'successful'

    def delete_class_teacher(self, ClassTeacher):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        delete_query = "DELETE FROM Class_Teachers WHERE Teacher=%s"
        cursor.execute(delete_query, (ClassTeacher.Teacher,))
        db.commit()

        cursor.close()
        db.close()

        return 'successful'

    # *Class Section
    def get_target_class_section(self, Class, ClassTeacher):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Class_Sections WHERE Code=%s AND Teacher=%s ORDER BY ID"
        cursor.execute(select_query, (Class.Code, ClassTeacher.Teacher))

        class_sections = cursor.fetchall()
        
        cursor.close()
        db.close()

        if class_sections:
            return [self.ClassSection(*class_section) for class_section in class_sections]
        return []

    def get_section_not_in_class(self, Class, ClassTeacher):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = """
            SELECT * FROM Sections WHERE Name NOT IN (
	            SELECT Section FROM Class_Sections WHERE Code=%s AND Teacher=%s);
        """
        cursor.execute(select_query, (Class.Code, ClassTeacher.Teacher))

        sections_not_in_class = cursor.fetchall()

        cursor.close()
        db.close()

        if sections_not_in_class:
            return [self.Section(*section_not_in_class) for section_not_in_class in sections_not_in_class]
        return []

    def register_section_class(self, Class, ClassTeacher, Section):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        insert_query = "INSERT INTO Class_Sections (Code, Teacher, Section) VALUES (%s,%s,%s)"
        cursor.execute(
            insert_query, (Class.Code, ClassTeacher.Teacher, Section.Name))
        db.commit()

        cursor.close()
        db.close()

        return 'successful'

    def delete_class_section(self, ClassSection):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        delete_query = "DELETE FROM Class_Sections WHERE Code=%s AND Teacher=%s AND Section=%s"
        cursor.execute(delete_query, (ClassSection.Code, ClassSection.Teacher, ClassSection.Section))
        db.commit()

        cursor.close()
        db.close()

        return 'successful'