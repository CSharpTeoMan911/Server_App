import sys
import threading
import mysql.connector


class Credential_Functions:
    student_id = ""
    password = ""

    def __init__(self, id, password):
        self.student_id = str(id)
        self.password = str(password)

    def Log_In(self):
        try:
            try:
                connector = mysql.connector.connect(user="student", password="User_Log_In", host="localhost",
                                                    database="universityrecords")
                cursor = connector.cursor()
                query = "SELECT student_Id, student_password FROM student_credentials WHERE student_Id = '" + str(
                    self.student_id) + "';"
                cursor.execute(query)

                for element in cursor:

                    if element[0] == self.student_id:
                        if element[1] == self.password:
                            connector.close()
                            cursor.close()

                            log_in_connector = mysql.connector.connect(user="student", password="User_Log_In",
                                                                       host="localhost", database="universityrecords")
                            log_in_cursor = log_in_connector.cursor()
                            log_in_query = "UPDATE student_credentials SET user_logged_in = %s WHERE student_Id = %s"
                            log_in_query_parameters = ("True", self.student_id)
                            log_in_cursor.execute(log_in_query, log_in_query_parameters)
                            log_in_connector.commit()
                            log_in_connector.close()
                            log_in_cursor.close()

                            return "[ Log In Succeeded ]"

                        else:
                            connector.close()
                            cursor.close()
                            return "[ Log in failed ]"

                return "[ Log in failed ]"

            except:
                return "[ Log in failed ]"

        except KeyboardInterrupt:
            threading.current_thread().join()
            sys.exit(0)

    def Register(self):
        try:
            try:
                connector = mysql.connector.connect(user="student", password="User_Log_In", host="localhost",
                                                    database="universityrecords")
                cursor = connector.cursor()
                query = "SELECT student_Id, student_password FROM student_credentials WHERE student_Id = '" + str(
                    self.student_id) + "';"
                cursor.execute(query)

                for element in cursor:

                    if element[0] == self.student_id:
                        if element[1] == self.password:
                            connector.close()
                            cursor.close()
                            return "[ Registration failed ]"

                        else:
                            connector.close()
                            cursor.close()
                            return "[ Registration failed ]"

                register_connector = mysql.connector.connect(user="student", password="User_Log_In",
                                                             host="localhost", database="universityrecords")
                register_cursor = register_connector.cursor()
                registration_query = "INSERT student_credentials(student_Id, student_password) VALUES(%s, %s);"
                registration_query_parameters = (self.student_id, self.password)
                register_cursor.execute(registration_query, registration_query_parameters)
                register_connector.commit()
                register_connector.close()
                register_cursor.close()

                register_log_in_connector = mysql.connector.connect(user="student", password="User_Log_In",
                                                                    host="localhost", database="universityrecords")
                register_log_in_cursor = register_log_in_connector.cursor()
                log_in_registered_account = "UPDATE student_credentials SET user_logged_in = 'True' WHERE student_Id = '" + self.student_id + "';"
                register_log_in_cursor.execute(log_in_registered_account)
                register_log_in_connector.commit()
                register_log_in_connector.close()
                register_log_in_cursor.close()

                return "[ Registration Succeeded ]"

            except:
                return "[ Registration failed ]"

        except KeyboardInterrupt:
            threading.current_thread().join()
            sys.exit(0)

    def Log_Out(self):
        try:
            try:
                connector = mysql.connector.connect(user="student", password="User_Log_In", host="localhost",
                                                    database="universityrecords")
                cursor = connector.cursor()
                query = "UPDATE student_credentials SET user_logged_in = NULL WHERE student_Id = '" + str(
                    self.student_id) + "';"
                cursor.execute(query)
                connector.commit()
                connector.close()
                cursor.close()

                return "[ Log Out Succeeded ]"

            except:
                return "[ Log Out failed ]"

        except KeyboardInterrupt:
            sys.exit(0)

    def Verify_If_Logged_In(self):
        try:
            try:
                connector = mysql.connector.connect(user="student", password="User_Log_In",
                                                    host="localhost", database="universityrecords")
                cursor = connector.cursor()
                query = "SELECT user_logged_in FROM student_credentials WHERE student_Id = '" + self.student_id + "';"
                cursor.execute(query)

                for element in cursor:
                    if element[0] == "True":
                        return "[User Logged In]"
                    else:
                        return "[User not Logged In]"

                    connector.close()
                    cursor.close()

            except:
                return "[User not Logged In]"

        except KeyboardInterrupt:
            sys.exit(0)


class Profile_Functions:
    student_id = ""
    student_password = ""

    def __init__(self, ID, PASSWORD):
        self.student_id = str(ID)
        self.student_password = str(PASSWORD)

    def Download_Profile_Picture(self):

        try:
            try:
                verify = Credential_Functions(self.student_id, self.student_password)
                result = verify.Log_In()

                match result:
                    case "[ Log In Succeeded ]":
                        verification_result = verify.Verify_If_Logged_In()

                        match verification_result:
                            case "[User Logged In]":
                                con = mysql.connector.connect(user='student', password='User_Log_In',
                                                              database='universityrecords', host='localhost')

                                cursor = con.cursor()
                                query = ("SELECT student_profile_picture "
                                         "FROM "
                                         "student_credentials "
                                         "WHERE "
                                         "student_Id ='" + self.student_id + "';")

                                cursor.execute(query)

                                profile_picture = cursor.fetchall()

                                return profile_picture[0][0]

                            case "[User not Logged In]":
                                return bytes(0)

                    case "[ Log In failed ]":
                        return bytes(0)

            except:
                return bytes(0)
        except KeyboardInterrupt:
            sys.exit(0)


class Material_Functions:
    student_id = ""
    student_password = ""
    subject = ""
    file_name = ""
    week = ""

    def __init__(self, ID, PASSWORD, SUBJECT, FILE_NAME, WEEK):
        self.student_id = str(ID)
        self.student_password = str(PASSWORD)
        self.file_name = str(FILE_NAME)
        self.week = str(WEEK)

        match SUBJECT:

            case "0":
                self.subject = "computer_systems_materials_foundation_year"

            case "1":
                self.subject = "databases_materials_year_1"

            case "2":
                self.subject = "foundation_project_materials_foundation_year"

            case "3":
                self.subject = "fundamentals_of_programming_materials_foundation_year"

            case "4":
                self.subject = "fundamentals_of_software_engineering_materials_year_1"

            case "5":
                self.subject = "logical_analysis_materials_foundation_year"

    def Load_Materials(self):
        try:
            try:
                verify = Credential_Functions(self.student_id, self.student_password)
                result = verify.Log_In()

                match result:
                    case "[ Log In Succeeded ]":
                        verification_result = verify.Verify_If_Logged_In()

                        match verification_result:
                            case "[User Logged In]":

                                try:
                                    materials_download_connection = mysql.connector.connect(user='student',
                                                                                            password='User_Log_In',
                                                                                            database='universityrecords',
                                                                                            host='localhost')

                                    materials_download_cursor = materials_download_connection.cursor()
                                    materials_download_query = "SELECT material_name, " \
                                                               "Week_Value" \
                                                               " FROM " \
                                                               + self.subject + ";"

                                    materials_download_cursor.execute(materials_download_query)
                                    materials_retrieved_data = materials_download_cursor.fetchall()

                                    processed_data = ""

                                    for item in materials_retrieved_data:
                                        processed_data += item[0] + "|" + str(item[1]) + "|"

                                    materials_download_cursor.close()
                                    materials_download_connection.close()

                                    return processed_data.encode()

                                except:
                                    return "[Material Loading Procedure Failed]".encode("utf-8")

                            case "[User not Logged In]":
                                return "[Material Loading Procedure Failed]".encode("utf-8")

                    case "[ Log In failed ]":
                        return "[Material Loading Procedure Failed]".encode("utf-8")

            except:
                return "[Material Loading Procedure Failed]".encode("utf-8")
        except KeyboardInterrupt:
            sys.exit(0)




    def Download_Material(self):
        try:
            try:
                verify = Credential_Functions(self.student_id, self.student_password)
                result = verify.Log_In()

                match result:
                    case "[ Log In Succeeded ]":
                        verification_result = verify.Verify_If_Logged_In()

                        match verification_result:
                            case "[User Logged In]":

                                try:
                                    materials_download_connection = mysql.connector.connect(user='student',
                                                                                            password='User_Log_In',
                                                                                            database='universityrecords',
                                                                                            host='localhost')

                                    materials_download_cursor = materials_download_connection.cursor()
                                    materials_download_query = "SELECT material_file " \
                                                               "FROM " \
                                                               + self.subject +\
                                                               " WHERE material_name = '" + self.file_name + "' "\
                                                               "AND " \
                                                               "Week_Value ='" + self.week + "';"

                                    materials_download_cursor.execute(materials_download_query)
                                    materials_retrieved_data = materials_download_cursor.fetchall()

                                    processed_data = materials_retrieved_data[0][0]

                                    materials_download_cursor.close()
                                    materials_download_connection.close()

                                    return processed_data

                                except:
                                    return "[Material Downloading Procedure Failed]".encode("utf-8")

                            case "[User not Logged In]":
                                return "[Material Downloading Procedure Failed]".encode("utf-8")

                    case "[ Log In failed ]":
                        return "[Material Downloading Procedure Failed]".encode("utf-8")

            except:
                return "[Material Downloading Procedure Failed]".encode("utf-8")
        except KeyboardInterrupt:
            sys.exit(0)


class Grades_Functions:
    user_id = ""
    password = ""
    grades_table_name = ""
    final_grades_table_name = ""

    def __init__(self, id, password, subject):
        self.user_id = str(id)
        self.password = str(password)

        match str(subject):

            case "0":
                self.final_grades_table_name = "computer_systems_final_grade_foundation_year"
                self.grades_table_name = "computer_systems_grades_foundation_year"

            case "1":
                self.final_grades_table_name = "databases_final_grade_year_1"
                self.grades_table_name = "databases_grades_year_1"

            case "2":
                self.final_grades_table_name = "foundation_project_final_grade_foundation_year"
                self.grades_table_name = "foundation_project_grades_foundation_year"

            case "3":
                self.final_grades_table_name = "fundamentals_of_programming_final_grade_foundation_year"
                self.grades_table_name = "fundamentals_of_programming_grades_foundation_year"

            case "4":
                self.final_grades_table_name = "fundamentals_of_software_engineering_final_grade_year_1"
                self.grades_table_name = "fundamentals_of_software_engineering_grades_year_1"

            case "5":
                self.final_grades_table_name = "logical_analysis_final_grade_foundation_year"
                self.grades_table_name = "logical_analysis_grades_foundation_year"

    def Load_Grades(self):

        try:
            try:
                verify = Credential_Functions(self.user_id, self.password)
                result = verify.Log_In()

                match result:
                    case "[ Log In Succeeded ]":
                        verification_result = verify.Verify_If_Logged_In()

                        match verification_result:
                            case "[User Logged In]":

                                try:
                                    grades_download_connection = mysql.connector.connect(user='student',
                                                                                         password='User_Log_In',
                                                                                         database='universityrecords',
                                                                                         host='localhost')

                                    grades_download_cursor = grades_download_connection.cursor()
                                    grades_download_query = "SELECT Grade1, Grade2, Grade3 FROM " \
                                                            + str(self.grades_table_name) + \
                                                            " WHERE student_Id = '" + str(self.user_id) + "';"

                                    grades_download_cursor.execute(grades_download_query)
                                    grades_retrieved_data = grades_download_cursor.fetchall()

                                    processed_data = ""

                                    processed_data += str(grades_retrieved_data[0][0]) + "|" + str(
                                        grades_retrieved_data[0][1]) + "|" + str(grades_retrieved_data[0][2])
                                    grades_download_cursor.close()
                                    grades_download_connection.close()

                                    final_grade_download_connection = mysql.connector.connect(user='student',
                                                                                              password='User_Log_In',
                                                                                              database='universityrecords',
                                                                                              host='localhost')

                                    final_grade_download_cursor = final_grade_download_connection.cursor()
                                    final_grade_download_query = "SELECT FinalGrade FROM " \
                                                                 + str(self.final_grades_table_name) + \
                                                                 " WHERE student_Id = '" + str(self.user_id) + "';"

                                    final_grade_download_cursor.execute(final_grade_download_query)
                                    final_grade_retrieved_data = final_grade_download_cursor.fetchall()

                                    processed_data += "|" + str(final_grade_retrieved_data[0][0]) + "|"

                                    final_grade_download_cursor.close()
                                    final_grade_download_connection.close()

                                    return processed_data.encode()

                                except:
                                    return "[Grade Loading Procedure Failed]".encode("utf-8")

                            case "[User not Logged In]":
                                return "[Grade Loading Procedure Failed]".encode("utf-8")

                    case "[ Log In failed ]":
                        return "[Grade Loading Procedure Failed]".encode("utf-8")

            except:
                return "[Grade Loading Procedure Failed]".encode("utf-8")
        except KeyboardInterrupt:
            sys.exit(0)


class Contact_Functions:
    student_id = ""
    student_password = ""
    institution_name = ""

    def __init__(self, ID, PASSWORD, INSTITUTION_NAME):
        self.student_id = ID
        self.student_password = PASSWORD
        self.institution_name = INSTITUTION_NAME

    def Load_Contacts(self):

        try:
            try:
                verify = Credential_Functions(self.student_id, self.student_password)
                result = verify.Log_In()

                match result:
                    case "[ Log In Succeeded ]":
                        verification_result = verify.Verify_If_Logged_In()

                        match verification_result:
                            case "[User Logged In]":
                                connector = mysql.connector.connect(user="student", password="User_Log_In",
                                                                    host="localhost", database="universityrecords")
                                cursor = connector.cursor()
                                query = "SELECT academic_institution, institution_landline_number, institution_email " \
                                        "FROM university_contacts"
                                cursor.execute(query)

                                retrieved_data = cursor.fetchall()

                                processed_data = ""

                                for data in retrieved_data:
                                    processed_data += "[" + data[0] + "|" + data[1] + "|" + data[2] + "]"

                                return processed_data.encode()

                            case "[User not Logged In]":
                                return "[ Error Loading Contacts ]".encode()

                    case "[ Log In failed ]":
                        return "[ Error Loading Contacts ]".encode()

            except:
                return "[ Error Loading Contacts ]".encode()

        except KeyboardInterrupt:
            sys.exit(0)

    def Download_Contact_Picture(self):
        try:
            try:
                verify = Credential_Functions(self.student_id, self.student_password)
                result = verify.Log_In()

                match result:
                    case "[ Log In Succeeded ]":
                        verification_result = verify.Verify_If_Logged_In()

                        match verification_result:
                            case "[User Logged In]":

                                con = mysql.connector.connect(user='student', password='User_Log_In',
                                                              database='universityrecords', host='localhost')

                                cursor = con.cursor()
                                query = ("SELECT institution_picture "
                                         "FROM "
                                         "university_contacts "
                                         "WHERE "
                                         "academic_institution ='" + self.institution_name + "';")

                                cursor.execute(query)

                                profile_picture = cursor.fetchall()

                                return profile_picture[0][0]

                            case "[User not Logged In]":
                                return bytes(0)

                    case "[ Log In failed ]":
                        return bytes(0)

            except:
                return bytes(0)

        except KeyboardInterrupt:
            sys.exit(0)
