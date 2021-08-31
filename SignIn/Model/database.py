import mysql.connector as mc


class Database:

    def __init__(self):
        try:
            db = self.connect()
            cursor = db.cursor()

            sql_query = """
                CREATE DATABASE Horace;
                
                CREATE TABLE Horace.Users ( 
                    UserID INT NOT NULL AUTO_INCREMENT, 
                    Username VARCHAR(32) BINARY, 
                    Privilege CHAR(7) NOT NULL, 
                    Salt CHAR(29) NULL, 
                    Hash CHAR(31) NULL, 
                    PRIMARY KEY (UserID),
                    UNIQUE INDEX Username_UNIQUE (Username),
                    KEY Privilege (Privilege)) ENGINE = InnoDB;
                
                CREATE TABLE Horace.Sections ( 
                    ID INT NOT NULL AUTO_INCREMENT, 
                    Section VARCHAR(32) BINARY, 
                    PRIMARY KEY (ID),
                    UNIQUE INDEX Section_UNIQUE (Section),
                    KEY Section (Section)) ENGINE = InnoDB;

                CREATE TABLE Horace.Section_Members ( 
                    ID INT NOT NULL AUTO_INCREMENT, 
                    Section VARCHAR(32) BINARY,
                    Student VARCHAR(32) BINARY,
                    PRIMARY KEY (ID),
                    CONSTRAINT FK_Section FOREIGN KEY (Section) REFERENCES Horace.Sections (Section) ON DELETE CASCADE ON UPDATE CASCADE,
                    CONSTRAINT FK_Section_Student FOREIGN KEY (Student) REFERENCES Horace.Users (Username) ON DELETE CASCADE ON UPDATE CASCADE
                    ) ENGINE = InnoDB;

                CREATE TABLE Horace.Attendances (
                    ID INT NOT NULL AUTO_INCREMENT,
                    Teacher VARCHAR(32) BINARY,
                    File_Name VARCHAR(54) NOT NULL,
                    File LONGBLOB NOT NULL,
                    Date DATETIME NOT NULL,
                    PRIMARY KEY (ID),
                    CONSTRAINT FK_Attendances_Teacher FOREIGN KEY (Teacher) REFERENCES Horace.Users (Username) ON DELETE CASCADE ON UPDATE CASCADE
                    ) ENGINE=InnoDB;

                CREATE TABLE Horace.Classes ( 
                    ID INT NOT NULL AUTO_INCREMENT,
                    Code VARCHAR(32) BINARY,
                    Name VARCHAR(54) NOT NULL,
                    Teacher VARCHAR(32) BINARY,
                    Host_Address int(4) UNSIGNED NULL,
                    Start TIME NOT NULL,
                    End TIME NOT NULL,
                    PRIMARY KEY (ID),
                    CONSTRAINT FK_Classes_Teacher FOREIGN KEY (Teacher) REFERENCES Horace.Users (Username) ON DELETE CASCADE ON UPDATE CASCADE,
                    UNIQUE INDEX Code_UNIQUE (Code)) ENGINE = InnoDB;

                CREATE TABLE Horace.Class_Members ( 
                    ID INT NOT NULL AUTO_INCREMENT,
                    Code VARCHAR(32) BINARY,
                    Section VARCHAR(32) BINARY,
                    PRIMARY KEY (ID),
                    CONSTRAINT FK_Class_Code FOREIGN KEY (Code) REFERENCES Horace.Classes (Code) ON DELETE CASCADE ON UPDATE CASCADE,
                    CONSTRAINT FK_Class_Section FOREIGN KEY (Section) REFERENCES Horace.Sections (Section) ON DELETE CASCADE ON UPDATE CASCADE
                    ) ENGINE = InnoDB;

                CREATE TABLE Horace.Security_Questions (
                    ID INT NOT NULL AUTO_INCREMENT,
                    Admin VARCHAR(32) BINARY,
                    Question VARCHAR(60) NOT NULL, 
                    Salt CHAR(29) NOT NULL, 
                    Hash CHAR(31) NOT NULL, 
                    PRIMARY KEY (ID),
                    CONSTRAINT FK_SQ_Admin FOREIGN KEY (Admin) REFERENCES Horace.Users (Username) ON DELETE CASCADE ON UPDATE CASCADE
                    ) ENGINE=InnoDB;

                CREATE TABLE Horace.URLs(
                    ID INT NOT NULL AUTO_INCREMENT,
                    URL VARCHAR(54) NOT NULL,
                    PRIMARY KEY (ID)
                    ) ENGINE=InnoDB;

                INSERT INTO Horace.Users (Username, Privilege)
                VALUES ('Admin', 'Admin');
            """

            results = cursor.execute(sql_query, multi=True)

            for result in results:
                result.fetchall()

            db.commit()
            cursor.close()
            db.close()

        except mc.Error as e:
            if e.errno == 1007:
                return
            else:
                print(e)

    def connect(self, database=None):
        try:
            return mc.connect(
                user="root",
                password="root123",
                host="127.0.0.1",
                database=database
            )
        except mc.Error as e:
            print(e)
