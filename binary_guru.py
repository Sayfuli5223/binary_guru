import sys
import smtplib
import random
import string
import time
import datetime
import pytz
import requests
import mysql.connector
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from colorama import Fore, Style, init

from getpass import getpass

# Initialize colorama for colored output
init(autoreset=True)

# ANSI escape codes for blue text
BLUE = '\033[1;34m'  # Bold Blue
RESET = '\033[0m'    # Reset to normal color

# MySQL Database Configuration
DB_HOST = 'sql12.freesqldatabase.com'
DB_USER = 'sql12745269'
DB_PASSWORD = 'LwDyBxJhM7'
DB_NAME = 'sql12745269'

# Email Configuration
SENDER_EMAIL = "binary.guru.socket@gmail.com"
SENDER_PASSWORD = "uhci lywd nloe epfd"  # App password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# OTP Expiry Time (in seconds)
OTP_EXPIRY_TIME = 600  # 10 minutes

# Function to send OTP to the user's email
def send_otp_email(recipient_email, otp):
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["From"] = SENDER_EMAIL
        message["To"] = recipient_email
        message["Subject"] = "BINARY GURU SOCKET LOGIN OTP CODE"

        # Modern minimalistic design with subtle gradient and clean layout
        html = f"""
        <html>
          <head>
            <style>
              body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f3f4f6;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
              }}
              .email-container {{
                width: 100%;
                max-width: 600px;
                background-color: #ffffff;
                border-radius: 10px;
                padding: 40px;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
                text-align: center;
              }}
              .header {{
                background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                font-size: 28px;
                font-weight: bold;
              }}
              .otp-code {{
                font-size: 48px;
                font-weight: bold;
                color: #6a11cb;
                margin: 30px 0;
                background-color: #f1f5fe;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
              }}
              .message {{
                font-size: 16px;
                color: #555;
              }}
              .expire-info {{
                font-weight: bold;
                color: #e74c3c;
              }}
              .footer {{
                margin-top: 30px;
                font-size: 14px;
                color: #aaa;
              }}
              .footer a {{
                color: #2575fc;
                text-decoration: none;
              }}
            </style>
          </head>
          <body>
            <div class="email-container">
              <div class="header">
                Binary Guru Socket
              </div>
              <div class="message">
                <p>Your One-Time Password (OTP) for logging in is:</p>
              </div>
              <div class="otp-code">
                {otp}
              </div>
              <div class="message">
                <p>This OTP will expire in <span class="expire-info">10 minutes</span>.</p>
                <p>Please do not share this code with anyone.</p>
              </div>
              <div class="footer">
                <p>&copy; 2024 Binary Guru. All rights reserved.</p>
                <p><a href="#">Unsubscribe</a> | <a href="#">Privacy Policy</a></p>
              </div>
            </div>
          </body>
        </html>
        """

        # Attach both plain text and HTML versions to the email
        plain_text = f"Your One-Time Password (OTP) is: {otp}\nThis code will expire in 10 minutes."
        message.attach(MIMEText(plain_text, "plain"))
        message.attach(MIMEText(html, "html"))

        # Send the email via SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Encrypt the connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())

        # Success message
        print(f"{Fore.GREEN}OTP has been sent to your E-MAIL.{Fore.RESET}")

    except Exception as e:
        # Error handling
        print(f"{Fore.RED}Error sending OTP email: {e}{Fore.RESET}")

# Function to handle user login with MySQL and email verification
# Function to handle user login with MySQL and email verification
def login():
    attempts = 3
    while attempts > 0:
        username = input(f"{Fore.BLUE}Username: {Fore.RESET}").strip().upper()
        
        # Use getpass for secure password input (cross-platform)
        password = getpass(f"{Fore.BLUE}Password: {Fore.RESET}")
        
        if authenticate_user(username, password):
            print(f"{Fore.YELLOW}Authenticating...{Fore.RESET}")
            email = get_user_email(username)  # Retrieve user's email from the database
            if email:
                otp, timestamp = generate_otp()  # Generate OTP with timestamp
                send_otp_email(email, otp)  # Send OTP to the user's email
                
                otp_attempts = 3  # Counter for OTP attempts
                while otp_attempts > 0:
                    user_otp = input(f"{Fore.BLUE}Enter the OTP sent to your email: {Fore.RESET}")
                    
                    # Show the "Verifying OTP..." loader for 5 seconds before verification
                    print(f"{Fore.YELLOW}Verifying OTP...", end='', flush=True)
                    time.sleep(5)  # Simulate the verification delay
                    
                    if verify_otp(otp, timestamp, user_otp):
                        print(f"\r{Fore.GREEN}Email Verified! Login successful!{Fore.RESET}")  # Update message to "Email Verified!"
                        # Wait for 2 seconds before proceeding to login success
                        time.sleep(2)
                        return True
                    else:
                        otp_attempts -= 1
                        print(f"\r{Fore.RED}Wrong OTP. {otp_attempts} attempt(s) remaining.{Fore.RESET}")
                
                print(f"{Fore.RED}Too many invalid OTP attempts. Exiting.{Fore.RESET}")
                return False  # Exit after 3 failed OTP attempts
            else:
                print(f"{Fore.RED}User does not have an email registered. Exiting.{Fore.RESET}")
                return False
        else:
            attempts -= 1
            print(f"{Fore.RED}Invalid credentials. {attempts} attempts remaining.{Fore.RESET}")
    
    print(f"{Fore.RED}Too many failed login attempts. Exiting.{Fore.RESET}")
    return False

# Function to authenticate user with MySQL database
def authenticate_user(username, password):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        query = "SELECT password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        
        if result and result[0] == password:
            return True  # User authenticated
        return False
    except mysql.connector.Error as err:
        print(f"{Fore.RED}Error connecting to MySQL: {err}{Fore.RESET}")
        return False
    finally:
        if conn:
            conn.close()

# Function to retrieve user's email from the database
def get_user_email(username):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        query = "SELECT email FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        
        if result:
            return result[0]  # Return the email address
        return None
    except mysql.connector.Error as err:
        print(f"{Fore.RED}Error fetching user email: {err}{Fore.RESET}")
        return None
    finally:
        if conn:
            conn.close()

# Function to generate a random OTP with a timestamp
def generate_otp():
    otp = ''.join(random.choices(string.digits, k=6))  # Generate a 6-digit OTP
    timestamp = time.time()  # Get the current time in seconds
    return otp, timestamp

# Function to verify the entered OTP and check expiry
def verify_otp(generated_otp, generated_timestamp, entered_otp):
    # Check if the OTP has expired
    if time.time() - generated_timestamp > OTP_EXPIRY_TIME:
        return False  # OTP has expired
    
    # Check if the entered OTP matches the generated OTP
    if generated_otp == entered_otp:
        return True  # OTP is valid
    return False  # OTP is invalid

# Custom function to handle password input with masking using msvcrt
def get_password(prompt="Password: "):
    print(prompt, end='', flush=True)
    password = []

    while True:
        ch = get_password()  # Get character input

        if ch == b'\r':  # Enter key
            break
        elif ch == b'\x08':  # Backspace key (delete last character)
            if password:
                password.pop()  # Remove last character
                sys.stdout.write('\b \b')  # Move cursor back
                sys.stdout.flush()
        else:
            password.append(ch.decode('utf-8'))  # Add character to password list
            sys.stdout.write('*')  # Mask input with asterisks
            sys.stdout.flush()
    
    print()  # Newline after password input
    return ''.join(password)

# Function to display banner with current time
def generate_banner(selected_timezone):
    timezone = pytz.timezone(selected_timezone)
    current_time = datetime.datetime.now(timezone)
    formatted_time = current_time.strftime('%d-%m-%y, Time-%H:%M')

    banner = f"""
\033[92m

======================== WELCOME BINARY_GURU ========================================

██████╗ ██╗███╗   ██╗ █████╗ ██████╗ ██╗   ██╗     ██████╗ ██╗   ██╗██████╗ ██╗   ██╗
██╔══██╗██║████╗  ██║██╔══██╗██╔══██╗╚██╗ ██╔╝    ██╔════╝ ██║   ██║██╔══██╗██║   ██║
██████╔╝██║██╔██╗ ██║███████║██████╔╝ ╚████╔╝     ██║  ███╗██║   ██║██████╔╝██║   ██║
██╔══██╗██║██║╚██╗██║██╔══██║██╔══██╗  ╚██╔╝      ██║   ██║██║   ██║██╔══██╗██║   ██║
██████╔╝██║██║ ╚████║██║  ██║██║  ██║   ██║       ╚██████╔╝╚██████╔╝██║  ██║╚██████╔╝
╚═════╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝        ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ 
                                                                                     

                Current Time: {formatted_time}
                     TELEGRAM - @ewr_sayful
======================== OCTOBITS SIGNALS =========================================== 

\033[92m
"""
    print(banner)

# Loading Animation
def loading_animation(text, duration=50, interval=0.2):
    colors = [Fore.YELLOW] * 6
    end_time = time.time() + duration

    while time.time() < end_time:
        for suffix in ['.','..','...']:
            color = colors[len(suffix) % len(colors)]
            sys.stdout.write(f'\r{color}{text} {suffix}')
            sys.stdout.flush()
            time.sleep(interval)
    
    print(f'\r{Fore.GREEN}{text} complete!')

def trend_animation(text, duration=50, interval=0.2):
    colors = [Fore.YELLOW] * 6
    end_time = time.time() + duration

    while time.time() < end_time:
        for suffix in ['.', '..', '...']:
            color = colors[len(suffix) % len(colors)]
            sys.stdout.write(f'\r{color}{text} {suffix}')
            sys.stdout.flush()
            time.sleep(interval)
    
    print(f'\r{Fore.GREEN}{text} complete!')

def spinner_animation(duration=20):
    colors = ['\033[93m'] * 7
    spinner = ['-','\\','|','/']
    end_time = time.time() + duration

    while time.time() < end_time:
        for frame in spinner:
            color = colors[spinner.index(frame) % len(colors)]
            sys.stdout.write(f'\r{color}SIGNAL GENERATING...{frame}\033[0m')
            sys.stdout.flush()
            time.sleep(0.2)
            
    print('\r\033[92mSIGNAL GENERATE SUCCESSFUL!\033[0m')

# Gathering Parameters from User
def gather_params():
    # Gather user inputs
    pairs = input(f"{Fore.BLUE}[*]Enter currency pairs (formate - XXXXXX-OTC): {Style.RESET_ALL}").strip()

    # Process the pairs by replacing hyphens with underscores
    pairs = pairs.replace("-OTC", "_otc")

    martingale_levels = input(f"{Fore.BLUE}[*]How many martingale levels do you want (1 or 2)? {Style.RESET_ALL}").strip()
    start_time = input(f"{Fore.BLUE}[*]Enter start time (e.g., 09:00): {Style.RESET_ALL}").strip() or "09:00"
    end_time = input(f"{Fore.BLUE}[*]Enter end time (e.g., 18:00): {Style.RESET_ALL}").strip() or "18:00"
    
    while True:
        try:
            days = int(input(f"{Fore.BLUE}[*]Enter number of days (e.g., 5): {Style.RESET_ALL}").strip())
            if days <= 0:
                print(f"{Fore.RED}Please enter a positive number for days.{Style.RESET_ALL}")
                continue
            break
        except ValueError:
            print(f"{Fore.RED}Invalid input, please enter a number for days.{Style.RESET_ALL}")
    
    while True:
        mode = input(f"{Fore.BLUE}[*]Enter mode (NORMAL or BLACKOUT): {Style.RESET_ALL}").strip().lower()
        if mode in ['normal', 'blackout']:
            break
        else:
            print(f"{Fore.RED}Invalid input! Please enter either 'normal' or 'blackout'.{Style.RESET_ALL}")
    
    # Ensure valid input for min_percentage and max_percentage
    while True:
        try:
            min_percentage = float(input(f"{Fore.BLUE}[*]Enter minimum percentage (e.g., 50): {Style.RESET_ALL}").strip() or "50")
            if min_percentage < 0 or min_percentage > 100:
                print(f"{Fore.RED}Please enter a valid percentage between 0 and 100.{Style.RESET_ALL}")
                continue
            break
        except ValueError:
            print(f"{Fore.RED}Invalid input, please enter a valid number for minimum percentage.{Style.RESET_ALL}")

    while True:
        try:
            max_percentage = float(input(f"{Fore.BLUE}[*]Enter maximum percentage (e.g., 50): {Style.RESET_ALL}").strip() or "50")
            if max_percentage < 0 or max_percentage > 100:
                print(f"{Fore.RED}Please enter a valid percentage between 0 and 100.{Style.RESET_ALL}")
                continue
            # Ensure max_percentage is greater than or equal to min_percentage
            if max_percentage < min_percentage:
                print(f"{Fore.RED}Maximum percentage must be greater than or equal to minimum percentage.{Style.RESET_ALL}")
                continue
            break
        except ValueError:
            print(f"{Fore.RED}Invalid input, please enter a valid number for maximum percentage.{Style.RESET_ALL}")
    
    filter_value = input(f"{Fore.BLUE}[*]Enter filter value (1 or 2): {Style.RESET_ALL}").strip() or "1"
    separate = input(f"{Fore.BLUE}[*]Enter separate (1): {Style.RESET_ALL}").strip() or "1"

    # Compile parameters into a dictionary
    params = {
        'start_time': start_time,
        'end_time': end_time,
        'days': days,
        'pairs': pairs,  
        'mode': mode,
        'min_percentage': min_percentage,
        'max_percentage': max_percentage,
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
            loading_animation("Capturing News", duration=10)
            trend_animation("Trend Filtering", duration=10)
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
