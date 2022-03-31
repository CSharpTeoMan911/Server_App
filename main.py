import atexit
import operator
import select
import socket
import sys
import threading
import Server_Functions

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def Connection_Management():
    try:
        try:
            connection, port = server_socket.accept()
            received_data = connection.recv(1000).decode("utf-8", "strict")

            option = ""
            subject = ""
            week = ""
            id = ""
            password = ""
            filename = ""

            if len(received_data) > 0:

                for index in range(0, len(received_data)):
                    if index == 0:
                        if str(received_data[index]) != "0":
                            option += str(received_data[index])

                    elif index == 1:
                        option += str(received_data[index])

                    elif index == 2:
                        subject += str(received_data[index])

                    elif index == 3:
                        if str(received_data[index]) != "0":
                            week += str(received_data[index])

                    elif index == 4:
                        week += str(received_data[index])

                    elif (index > 5) and (index < operator.indexOf(str(received_data), "]")):
                        id += str(received_data[index])

                    elif (index > operator.indexOf(str(received_data), "]") + 1) and (
                            index < len(str(received_data)) - 1 - operator.indexOf(reversed(str(received_data)), "]")):
                        password += str(received_data[index])

                    elif index > len(str(received_data)) - 1 - operator.indexOf(reversed(str(received_data)), "]"):
                        filename += str(received_data[index])

                match option:

                    case "1":
                        credential_function = Server_Functions.Credential_Functions(id, password)
                        retrieved_value = credential_function.Log_In()
                        connection.send(str.encode(retrieved_value))

                    case "2":
                        credential_function = Server_Functions.Credential_Functions(id, password)
                        retrieved_value = credential_function.Register()
                        connection.send(str.encode(retrieved_value))

                    case "3":

                        credential_function = Server_Functions.Credential_Functions(id, password)
                        retrieved_value = credential_function.Log_Out()
                        connection.send(str.encode(retrieved_value))

                    case "4":
                        profile_function = Server_Functions.Profile_Functions(id, password)
                        retrieved_value = profile_function.Download_Profile_Picture()
                        connection.send(retrieved_value)

                    case "5":
                        contacts_function = Server_Functions.Contact_Functions(id, password, filename)
                        retrieved_value = contacts_function.Load_Contacts()
                        connection.send(retrieved_value)

                    case "6":
                        contacts_function = Server_Functions.Contact_Functions(id, password, filename)
                        retrieved_value = contacts_function.Download_Contact_Picture()
                        connection.send(retrieved_value)

                    case "7":
                        grades_function = Server_Functions.Grades_Functions(id, password, subject)
                        retrieved_value = grades_function.Load_Grades()
                        connection.send(retrieved_value)

                    case "8":
                        materials_function = Server_Functions.Material_Functions(id, password, subject, "", "")
                        retrieved_value = materials_function.Load_Materials()
                        connection.send(retrieved_value)

                    case "9":
                        materials_function = Server_Functions.Material_Functions(id, password, subject, filename, week)
                        retrieved_value = materials_function.Download_Material()
                        connection.send(retrieved_value)



        except:
            pass

    except KeyboardInterrupt:
        threading.current_thread().join()
        server_socket.close()
        sys.exit(0)





def Server_Operation():
    server_socket.listen(1000)

    while True:
        try:
            try:
                connection_management_thread = threading.Thread(target=Connection_Management())
                connection_management_thread.start()

            except:
                atexit.register(sys.exit(0))
        except KeyboardInterrupt:
            threading.current_thread().join()
            server_socket.close()
            sys.exit(0)
            break


if __name__ == "__main__":

    try:
        try:
            print("##################################")
            print("#                                #")
            print("#  SERVER OPENED AND LISTENING   #")
            print("#                                #")
            print("##################################")

            server_socket.bind(("0.0.0.0", 22))

            print("ADDRESS: " + str(socket.gethostbyname(socket.gethostname())))
            print("PORT: " + str(server_socket.getsockname()[1]))

            thread = threading.Thread(target=Server_Operation())
            thread.start()

        except:
            atexit.register(sys.exit(0))

    except KeyboardInterrupt:
        sys.exit(0)
