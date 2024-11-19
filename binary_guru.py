import sys
import time
import datetime
import pytz
import requests
import mysql.connector
from colorama import Fore, Style, init
import msvcrt  # Windows-specific module to handle password input

# Initialize colorama for colored output
init(autoreset=True)

# ANSI escape codes for blue text
BLUE = '\033[1;34m'  # Bold Blue
RESET = '\033[0m'    # Reset to normal color

# MySQL Database Configuration
DB_HOST = 'sql12.freesqldatabase.com'  # Replace with your MySQL server host
DB_USER = 'sql12745269'  # Replace with your MySQL username
DB_PASSWORD = 'LwDyBxJhM7'  # Replace with your MySQL password
DB_NAME = 'sql12745269'  # Replace with your database name

# Function to handle user login with MySQL
def login():

    
    attempts = 3
    while attempts > 0:
        username = input(f"{BLUE}Username: {RESET}").strip().upper()
        password = get_password(f"{BLUE}Password: {RESET}")
        
        if authenticate_user(username, password):
            print(f"{Fore.GREEN}Login successful!")
            return True
        else:
            attempts -= 1
            print(f"{Fore.RED}Invalid Password. {attempts} attempts remaining.")
    
    print(f"{Fore.RED}Too many failed attempts. Exiting.")
    return False

# Custom function to handle password input with masking
def get_password(prompt="Password: "):
    # Print the prompt
    print(prompt, end='', flush=True)
    password = []
    
    while True:
        # Get a character from user input (without pressing Enter)
        ch = msvcrt.getch()
        
        # Check if the user pressed Enter (carriage return)
        if ch == b'\r':  # Enter key
            break
        elif ch == b'\x08':  # Backspace key (delete last character)
            if password:
                password.pop()
                sys.stdout.write('\b \b')  # Move the cursor back and overwrite the last character
                sys.stdout.flush()
        else:
            password.append(ch.decode('utf-8'))  # Decode the byte and append to password list
            sys.stdout.write('*')  # Display asterisk for each character typed
            sys.stdout.flush()
    
    print()  # To move to a new line after password input
    return ''.join(password)  # Return the password as a string

# Function to authenticate user with MySQL database
def authenticate_user(username, password):
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        # Query to fetch user data
        query = "SELECT password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        
        if result and result[0] == password:  # Check if password matches
            return True
        else:
            return False
    
    except mysql.connector.Error as err:
        print(f"{Fore.RED}Error connecting to MySQL: {err}")
        return False
    finally:
        if conn:
            conn.close()

# Function to display banner with current time
def generate_banner(selected_timezone):
    timezone = pytz.timezone(selected_timezone)
    current_time = datetime.datetime.now(timezone)
    formatted_time = current_time.strftime('%d-%m-%y, Time-%H:%M')

    banner = f"""
\033[92m

██████╗ ██╗███╗   ██╗ █████╗ ██████╗ ██╗   ██╗     ██████╗ ██╗   ██╗██████╗ ██╗   ██╗
██╔══██╗██║████╗  ██║██╔══██╗██╔══██╗╚██╗ ██╔╝    ██╔════╝ ██║   ██║██╔══██╗██║   ██║
██████╔╝██║██╔██╗ ██║███████║██████╔╝ ╚████╔╝     ██║  ███╗██║   ██║██████╔╝██║   ██║
██╔══██╗██║██║╚██╗██║██╔══██║██╔══██╗  ╚██╔╝      ██║   ██║██║   ██║██╔══██╗██║   ██║
██████╔╝██║██║ ╚████║██║  ██║██║  ██║   ██║       ╚██████╔╝╚██████╔╝██║  ██║╚██████╔╝
╚═════╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝        ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ 
                                                                                     

                Current Time: {formatted_time}
                     TELEGRAM - @ewr_sayful
======================== OCTOBITS SIGNALS ============================== 

\033[92m
"""
    print(banner)

# Loading Animation
def loading_animation(text, duration=50, interval=0.2):
    colors = [Fore.YELLOW] * 6
    end_time = time.time() + duration

    while time.time() < end_time:
        for suffix in [' ', '.', '..', '...']:
            color = colors[len(suffix) % len(colors)]
            sys.stdout.write(f'\r{color}{text} {suffix}')
            sys.stdout.flush()
            time.sleep(interval)
    
    print(f'\r{Fore.GREEN}{text} complete!')

def trend_animation(text, duration=50, interval=0.2):
    colors = [Fore.YELLOW] * 6
    end_time = time.time() + duration

    while time.time() < end_time:
        for suffix in [' ', '.', '..', '...']:
            color = colors[len(suffix) % len(colors)]
            sys.stdout.write(f'\r{color}{text} {suffix}')
            sys.stdout.flush()
            time.sleep(interval)
    
    print(f'\r{Fore.GREEN}{text} complete!')

def spinner_animation(duration=20):
    colors = ['\033[93m'] * 7
    spinner = ['-', '\\', '|', '/']
    end_time = time.time() + duration

    while time.time() < end_time:
        for frame in spinner:
            color = colors[spinner.index(frame) % len(colors)]
            sys.stdout.write(f'\r{color}SIGNAL GENERATING... {frame}\033[0m')
            sys.stdout.flush()
            time.sleep(0.2)
            
    print('\r\033[92mSIGNAL GENERATE SUCCESSFUL!\033[0m')

# Gathering Parameters from User
def gather_params():
    pairs = input(f"{Fore.RED}[*]Enter currency pairs (comma-separated, e.g., BRLUSD_otc,USDPKR_otc): {Style.RESET_ALL}").strip() 
    martingale_levels = input(f"{Fore.RED}[*]How many martingale levels do you want (1 or 2)? {Style.RESET_ALL}").strip() 
    start_time = input(f"{Fore.RED}[*]Enter start time (e.g., 09:00): {Style.RESET_ALL}").strip() or "09:00"
    end_time = input(f"{Fore.RED}[*]Enter end time (e.g., 18:00): {Style.RESET_ALL}").strip() or "18:00"
    
    while True:
        try:
            days = int(input(f"{Fore.RED}[*]Enter number of days (e.g., 5): {Style.RESET_ALL}").strip())
            if days <= 0:
                print(f"{Fore.RED}Please enter a positive number for days.{Style.RESET_ALL}")
                continue
            break
        except ValueError:
            print(f"{Fore.RED}Invalid input, please enter a number for days.{Style.RESET_ALL}")
    mode = input(f"{Fore.RED}[*]Enter mode (e.g., blackout or normal): {Style.RESET_ALL}").strip() or "normal"
    min_percentage = input(f"{Fore.RED}[*]Enter minimum percentage (e.g., 50 or 50+): {Style.RESET_ALL}").strip() or "50"
    filter_value = input(f"{Fore.RED}[*]Enter filter value (e.g., 1 or 2): {Style.RESET_ALL}").strip() or "1"
    separate = input(f"{Fore.RED}[*]Enter separate (e.g., 1): {Style.RESET_ALL}").strip() or "1"

    params = {
        'start_time': start_time,
        'end_time': end_time,
        'days': days,
        'pairs': pairs,
        'mode': mode,
        'min_percentage': min_percentage,
        'filter': filter_value,
        'separate': separate
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    return params, headers

# Processing Response Data based on mode
def process_response(response_text, mode):
    """
    Processes the response text and returns a formatted output with color based on the mode ('normal'/'blackout').

    Args:
    - response_text: The raw text data from the response.
    - mode: Mode can be either 'blackout' or 'normal'.

    Returns:
    - A list of formatted strings based on the mode, with color.
    """
    # Split the response text into individual lines
    lines = response_text.strip().split('\n')
    result = []

    # Signal Template (Banner) with gaps above and below
    signal_template = (
        f"\n\n"  # Adds two new lines before the banner for a gap
        f"{Fore.GREEN}{Style.BRIGHT}╔══════════════✰══════════════╗\n"
        f"  Use proper money management\n"
        f"  Use proper Trading Rule\n"
        f"  1STEP MTG\n"
        f"  BANGLADESH TIME (UTC+06:00)\n"
        f"╚══════════════✰══════════════╝\n"
        f"\n"  # Adds one new line after the banner for a gap
        f"1 Minute Expire Signal\n\n{Style.RESET_ALL}"
    )
    result.append(signal_template)  # Add the banner template above the results

    for line in lines:
        if any(line.startswith(meta) for meta in ["Execution Time", "Timezone", "Date", "Signals:"]):
            continue
        if not line.strip():  # Skip empty lines
            continue
        
        try:
            line_parts = line.split('～')

            if len(line_parts) >= 3:
                currency_pair = line_parts[1].replace('_', '-').upper()
                time = line_parts[2].strip()

                # Add signal to result based on mode
                if mode == "blackout":
                    result.append(f"{Fore.YELLOW}{Style.BRIGHT}`{time};{currency_pair}`{Style.RESET_ALL}")
                elif mode == "normal":
                    try:
                        signal_type = line_parts[3].strip().upper()
                        if signal_type == "CALL":
                            result.append(f"{Fore.YELLOW}{Style.BRIGHT}`{time};{currency_pair};{signal_type}`{Style.RESET_ALL}")
                        elif signal_type == "PUT":
                            result.append(f"{Fore.YELLOW}{Style.BRIGHT}`{time};{currency_pair};{signal_type}`{Style.RESET_ALL}")
                        else:
                            result.append(f"{Fore.YELLOW}{Style.BRIGHT}`{time};{currency_pair}; UNKNOWN`{Style.RESET_ALL}")
                    except IndexError:
                        result.append(f"{Fore.CYAN}{Style.BRIGHT}`{time};{currency_pair};UNKNOWN`{Style.RESET_ALL}")
            else:
                result.append(f"{Fore.MAGENTA}Invalid line format: {line}")
        except Exception as e:
            result.append(f"{Fore.RED}Error processing line: {line}. Error: {str(e)}")

    return result
def send_request():
    url = "https://alltradingapi.com/signal_list_gen/qx_signal.js"
    
    params, headers = gather_params()
    
    try:
        # Send the HTTP request
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Will raise HTTPError for bad responses (4xx, 5xx)
        
        try:
            response_text = response.text
            # Process the response text based on mode
            result = process_response(response_text, params['mode'])

            # Display results with the banner and animations
            loading_animation("Capturing News...", duration=10)
            trend_animation("Trend Filtering...", duration=10)
            spinner_animation(duration=20)

        
            
            # Print the formatted result
            for line in result:
                print(line)
            
        except ValueError:
            print("Response is not in expected format:")
            print(response.text)
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    finally:
        leave_choice = input("DO YOU WANT TO LEAVE? (Y/N): ").strip().upper()
        if leave_choice == 'Y':
            print("Exiting the program.")    
if __name__ == "__main__":
    generate_banner('Asia/Dhaka')  # Print banner first
    if login():  # Login system after banner
        send_request()  # Continue with request if login is successful
