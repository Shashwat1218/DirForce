import requests
import pyfiglet
from colorama import init, Fore, Style
import threading

# Initialize colorama
init()

# Function to print the banner using pyfiglet
def print_banner():
    banner = pyfiglet.figlet_format("DirForce")
    print(Fore.CYAN + banner + Style.RESET_ALL)
    print(Fore.YELLOW + "Developed by Shashwat Singhal" + Style.RESET_ALL)

# Function to make a request to the given URL
def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

# Function to check if a directory exists on the target URL
def check_directory(target_url, directory, output_file_name, lock):
    full_url = target_url + '/' + directory.strip()
    response = request(full_url)
    with lock:  # Ensure thread-safe access to shared resources
        if response:
            print(Fore.GREEN + '[FOUND] ' + Style.BRIGHT + full_url + Style.RESET_ALL)
            # Append the found directory to the output file
            with open(output_file_name, 'a') as output_file:
                output_file.write(full_url + '\n')
        else:
            print(Fore.RED + '[NOT FOUND] ' + Style.BRIGHT + full_url + Style.RESET_ALL)

# Main function to run the script
def main():
    print_banner()
    # Get user inputs
    target_url = input('[*] Enter Target URL: ')
    file_path = input('[*] Enter Path Of The File Containing Directories: ')
    output_file_name = input('[*] Enter Name Of The Output File: ')
    thread_count = int(input('[*] Enter Number Of Threads: '))

    # Create output file instantly
    open(output_file_name, 'w').close()
    
    # Read the directories from the file
    with open(file_path, 'r') as file:
        directories = file.readlines()

    lock = threading.Lock()  # Lock for thread-safe file access
    threads = []

    # Create and start threads for each directory
    for directory in directories:
        while threading.active_count() > thread_count:
            pass
        thread = threading.Thread(target=check_directory, args=(target_url, directory, output_file_name, lock))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print(Fore.YELLOW + '[*] Scanning completed. Results have been saved to ' + output_file_name + Style.RESET_ALL)

# Run the main function
if __name__ == "__main__":
    main()
