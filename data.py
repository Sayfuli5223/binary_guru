import mysql.connector
from mysql.connector import Error

# ANSI Escape Codes for colors
class Colors:
    RESET = "\033[0m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    WHITE_BG = "\033[48;5;15m"
    GREY_BG = "\033[48;5;235m"
    LIGHT_BLUE = "\033[48;5;33m"

# Function to get employee details from the user
def get_employee_details():
    print(f"\n{Colors.BOLD}{Colors.CYAN}Enter the following details for the new user:{Colors.RESET}")
    username = input(f"{Colors.YELLOW}Enter client username: {Colors.RESET}").strip()
    password = input(f"{Colors.YELLOW}Enter client password: {Colors.RESET}").strip()
    email = input(f"{Colors.YELLOW}Enter client email: {Colors.RESET}").strip()  # New field for email
    return username, password, email

# Function to display all users in a stylish table-like format with colors
def display_users(connection):
    try:
        query = "SELECT id, username, password, email FROM users"  # Now selecting password as well
        cursor = connection.cursor()
        cursor.execute(query)
        users = cursor.fetchall()

        if users:
            print(Colors.CYAN + "=" * 90 + Colors.RESET)  # Increased the width for the new column
            print(Colors.BOLD + Colors.WHITE_BG + "{:<6} {:<25} {:<40} {:<30}".format("ID", "Username", "Email", "Password") + Colors.RESET)
            print(Colors.CYAN + "-" * 90 + Colors.RESET)

            for user in users:
                user_id = str(user[0]) if user[0] is not None else "N/A"
                username = user[1] if user[1] is not None else "N/A"
                email = user[3] if user[3] is not None else "N/A"
                password = user[2] if user[2] is not None else "N/A"  # Show password

                # Print each row of data with a highlighted background for readability
                print(Colors.GREY_BG + "{:<6} {:<25} {:<40} {:<30}".format(user_id, username, email, password) + Colors.RESET)

            print(Colors.CYAN + "=" * 90 + Colors.RESET)
        else:
            print(Colors.RED + "No users found in the database." + Colors.RESET)

        return users  # Return the list of users to let the user choose which one to delete

    except Error as e:
        print(f"Error occurred while fetching users: {e}")
        return []

    finally:
        cursor.close()

# Function to delete multiple users by selecting from the displayed users
def delete_user(connection):
    delete_choice = input(f"\n{Colors.CYAN}Would you like to delete a specific user? (yes/no): {Colors.RESET}").strip().lower()
    
    if delete_choice == "yes":
        users = display_users(connection)

        if users:
            cursor = None  # Initialize cursor here, before we enter try block
            try:
                # Accept a comma-separated list of user IDs
                choices = input(f"\n{Colors.YELLOW}Enter the numbers of the users you want to delete (e.g., 2,3,8): {Colors.RESET}").strip()
                # Convert the input string into a list of integers
                delete_ids = [int(x) for x in choices.split(",")]

                # Loop through the list and delete users
                for choice in delete_ids:
                    if 1 <= choice <= len(users):
                        user_to_delete = users[choice - 1]
                        user_id = user_to_delete[0]  # Get the ID of the user to delete

                        delete_query = "DELETE FROM users WHERE id = %s"
                        cursor = connection.cursor()  # Create cursor inside try block
                        cursor.execute(delete_query, (user_id,))
                        connection.commit()

                        if cursor.rowcount > 0:
                            print(Colors.GREEN + f"User with ID {user_id} (Username: {user_to_delete[1]}) deleted successfully." + Colors.RESET)
                        else:
                            print(Colors.RED + f"Failed to delete user with ID {user_id}." + Colors.RESET)
                    else:
                        print(Colors.RED + f"Invalid user ID: {choice}. No user deleted." + Colors.RESET)

            except ValueError:
                print(Colors.RED + "Invalid input. Please enter a valid comma-separated list of numbers." + Colors.RESET)
            except Error as delete_error:
                print(f"Error occurred while deleting user: {delete_error}")
            finally:
                if cursor:  # Ensure cursor is closed only if it was created
                    cursor.close()

        else:
            print(Colors.RED + "No users available to delete." + Colors.RESET)
    else:
        print(Colors.YELLOW + "No user was deleted." + Colors.RESET)

# Main program function
def main():
    DB_HOST = 'sql12.freesqldatabase.com'  
    DB_USER = 'sql12745269'  
    DB_PASSWORD = 'LwDyBxJhM7'  
    DB_NAME = 'sql12745269'  

    try:
        connection = mysql.connector.connect(
            host=DB_HOST,         
            user=DB_USER,         
            password=DB_PASSWORD, 
            database=DB_NAME      
        )

        if connection.is_connected():
            print(Colors.GREEN + "Connected to the database successfully!" + Colors.RESET)

            while True:
                print(Colors.CYAN + "\nChoose an action:" + Colors.RESET)
                print(Colors.YELLOW + "1. Add User" + Colors.RESET)
                print(Colors.YELLOW + "2. Delete User" + Colors.RESET)
                print(Colors.YELLOW + "3. Exit" + Colors.RESET)
                action = input(f"{Colors.YELLOW}Enter choice (1/2/3): {Colors.RESET}").strip()

                if action == '1':
                    username, password, email = get_employee_details()

                    if username and password and email:
                        try:
                            insert_query = """
                            INSERT INTO users (username, password, email)
                            VALUES (%s, %s, %s)
                            """
                            cursor = connection.cursor()
                            cursor.execute(insert_query, (username, password, email))
                            connection.commit()

                            print(Colors.GREEN + f"Data inserted successfully. Employee ID: {cursor.lastrowid}" + Colors.RESET)
                        except Error as insert_error:
                            print(Colors.RED + f"Error inserting data: {insert_error}" + Colors.RESET)
                        finally:
                            cursor.close()

                elif action == '2':
                    delete_user(connection)

                elif action == '3':
                    print(Colors.YELLOW + "Exiting program..." + Colors.RESET)
                    break

                else:
                    print(Colors.RED + "Invalid option. Please select a valid action." + Colors.RESET)
            
    except Error as e:
        print(f"Error occurred: {e}")

    finally:
        if connection.is_connected():
            connection.close()
            print(Colors.YELLOW + "Connection closed." + Colors.RESET)

if __name__ == "__main__":
    main()
