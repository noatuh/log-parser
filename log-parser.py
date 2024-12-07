import os
import re
import datetime

def extract_log_entries(log_file, keyword=None, start_time=None, end_time=None):
    """
    Extracts log entries based on keyword and optional time range filtering.
    """
    extracted_entries = []
    try:
        with open(log_file, 'r') as file:
            for line in file:
                if keyword and keyword not in line:
                    continue
                if start_time or end_time:
                    log_time = extract_time(line)
                    if log_time:
                        if start_time and log_time < start_time:
                            continue
                        if end_time and log_time > end_time:
                            continue
                extracted_entries.append(line.strip())
    except FileNotFoundError:
        print(f"Log file {log_file} not found.")
    except PermissionError:
        print(f"Permission denied. Please check your permissions for {log_file}.")
    return extracted_entries

def extract_time(log_line):
    """
    Extracts the timestamp from a log line (if present).
    Example format: 'Nov 26 14:29:50'
    """
    try:
        parts = log_line.split()
        if len(parts) < 3:
            return None
        log_time = " ".join(parts[:3])  # 'Nov 26 14:29:50'
        current_year = datetime.datetime.now().year
        return datetime.datetime.strptime(f"{log_time} {current_year}", "%b %d %H:%M:%S %Y")
    except ValueError:
        return None

def ensure_log_extension(file_name):
    """
    Ensures the file name has a .log extension.
    """
    return file_name if file_name.endswith(".log") else f"{file_name}.log"

def get_log_file_path():
    """
    Gets the log file path by asking the user or searching the default syslog directory.
    """
    # Prompt user to check default syslog directory
    use_syslog_dir = input("Do you want to check the default syslog directory (/var/log/)? (y/n): ").strip().lower()
    if use_syslog_dir == 'y':
        syslog_path = "/var/log/syslog"
        if os.path.isfile(syslog_path):
            print(f"Default log file found: {syslog_path}")
            return syslog_path
        else:
            print("No syslog file found in /var/log/.")
    
    # Custom directory option
    use_custom_dir = input("Do you want to specify a custom directory? (y/n): ").strip().lower()
    if use_custom_dir == 'y':
        custom_dir = input("Enter the custom directory path (leave blank for current directory): ").strip()
        if not custom_dir:
            custom_dir = os.getcwd()  # Default to current directory
        log_file_name = input("Enter the log file name: ").strip()
        return os.path.join(custom_dir, ensure_log_extension(log_file_name))
    
    print("No valid log file found or specified. Exiting.")
    exit()

def save_to_csv(entries, output_file):
    """
    Saves log entries to a CSV file with timestamps.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(output_file, 'a') as file:
        for entry in entries:
            file.write(f'"{timestamp}","{entry}"\n')

def main():
    print("=== Log Parser ===")
    log_file = get_log_file_path()

    keyword = input("Enter a keyword to filter logs (leave blank for all entries): ").strip()

    start_time_str = input("Enter start time (YYYY-MM-DD HH:MM:SS) or leave blank: ").strip()
    end_time_str = input("Enter end time (YYYY-MM-DD HH:MM:SS) or leave blank: ").strip()

    start_time = None
    end_time = None

    if start_time_str:
        start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    if end_time_str:
        end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

    log_entries = extract_log_entries(log_file, keyword, start_time, end_time)

    if log_entries:
        print(f"Found {len(log_entries)} entries matching your criteria.")
        save_to_csv(log_entries, "parsed_log.csv")
        print("Entries successfully saved to parsed_log.csv.")
        print("\nSummary of appended entries:")
        for entry in log_entries[:5]:  # Show the first 5 entries
            print(f" - {entry}")
    else:
        print("No matching log entries found.")

if __name__ == "__main__":
    main()
