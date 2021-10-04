import mysql.connector as mc
from SignIn.Misc.Functions.read_db_config import read_db_config

class Database:

    def init_db(self):
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
                    Name VARCHAR(32) BINARY, 
                    PRIMARY KEY (ID),
                    UNIQUE INDEX Section_UNIQUE (Name),
                    KEY Section (Name)) ENGINE = InnoDB;

                CREATE TABLE Horace.Section_Students ( 
                    ID INT NOT NULL AUTO_INCREMENT, 
                    Section VARCHAR(32) BINARY,
                    Student VARCHAR(32) BINARY,
                    PRIMARY KEY (ID),
                    CONSTRAINT FK_Section FOREIGN KEY (Section) REFERENCES Horace.Sections (Name) ON DELETE CASCADE ON UPDATE CASCADE,
                    CONSTRAINT FK_Section_Student FOREIGN KEY (Student) REFERENCES Horace.Users (Username) ON DELETE CASCADE ON UPDATE CASCADE,
                    UNIQUE INDEX Student_UNIQUE (Student)
                    ) ENGINE = InnoDB;

                CREATE TABLE Horace.Attendances (
                    ID INT NOT NULL AUTO_INCREMENT,
                    Teacher VARCHAR(32) BINARY,
                    Name VARCHAR(54) NOT NULL,
                    File LONGBLOB NOT NULL,
                    Date DATETIME NOT NULL,
                    PRIMARY KEY (ID),
                    CONSTRAINT FK_Attendances_Teacher FOREIGN KEY (Teacher) REFERENCES Horace.Users (Username) ON DELETE CASCADE ON UPDATE CASCADE
                    ) ENGINE=InnoDB;

                CREATE TABLE Horace.Classes ( 
                    ID INT NOT NULL AUTO_INCREMENT,
                    Code VARCHAR(32) BINARY,
                    Name VARCHAR(54) NOT NULL,
                    Start TIME NOT NULL,
                    End TIME NOT NULL,
                    PRIMARY KEY (ID),
                    KEY Code (Code)) ENGINE = InnoDB;

                CREATE TABLE Horace.Class_Teachers ( 
                    ID INT NOT NULL AUTO_INCREMENT,
                    Code VARCHAR(32) BINARY,
                    Teacher VARCHAR(32) BINARY,
                    Start TIME NOT NULL,
                    End TIME NOT NULL,
                    Host_Address int(4) UNSIGNED NULL,
                    PRIMARY KEY (ID),
                    CONSTRAINT FK_Class_Teachers_Code FOREIGN KEY (Code) REFERENCES Horace.Classes (Code) ON DELETE CASCADE ON UPDATE CASCADE,
                    CONSTRAINT FK_Class_Teacher FOREIGN KEY (Teacher) REFERENCES Horace.Users (Username) ON DELETE CASCADE ON UPDATE CASCADE
                    ) ENGINE = InnoDB;

                CREATE TABLE Horace.Class_Sections ( 
                    ID INT NOT NULL AUTO_INCREMENT,
                    Code VARCHAR(32) BINARY,
                    Teacher VARCHAR(32) BINARY,
                    Section VARCHAR(32) BINARY,
                    Start TIME NOT NULL,
                    End TIME NOT NULL,
                    PRIMARY KEY (ID),
                    CONSTRAINT FK_Class_Section_Code FOREIGN KEY (Code) REFERENCES Horace.Classes (Code) ON DELETE CASCADE ON UPDATE CASCADE,
                    CONSTRAINT FK_Class_Section_Teacher FOREIGN KEY (Teacher) REFERENCES Horace.Users (Username) ON DELETE CASCADE ON UPDATE CASCADE,
                    CONSTRAINT FK_Class_Section FOREIGN KEY (Section) REFERENCES Horace.Sections (Name) ON DELETE CASCADE ON UPDATE CASCADE
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
                    Domain VARCHAR(54) NOT NULL,
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

            return True

        except mc.Error as e:
            if e.errno == 1007:
                return True
            else:
                return False
        except AttributeError:
            return False

    def connect(self, database=None):
        try:
            config = read_db_config()
            config['database'] = database
            return mc.connect(**config)
        except mc.Error as e:
            return
