import pandas as pd
from datetime import datetime, timedelta

def analyze_employee_schedule(file_path):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Sort the DataFrame by Employee Name and Time
    df.sort_values(by=['Employee Name', 'Time'], inplace=True)

    # Reset the index for easier iteration
    df.reset_index(drop=True, inplace=True)

    # Loop through the DataFrame to analyze each employee's schedule
    for i in range(len(df) - 1):
        current_row = df.loc[i]
        next_row = df.loc[i + 1]

        # Parse date and time strings to datetime objects
        current_time = parse_date_time(current_row['Time'])
        next_time = parse_date_time(next_row['Time'])

        # Parse 'Time Out' string to datetime object
        current_time_out = parse_date_time(current_row['Time Out'])

        # Skip rows with missing or invalid date-time values
        if current_time is None or next_time is None or current_time_out is None:
            continue

        # a) Check for employees who have worked for 7 consecutive days
        if (next_time - current_time_out).days == 1:
            consecutive_days = 1
            j = i + 1
            while j < len(df) - 1:
                next_time_out = parse_date_time(df.loc[j]['Time Out'])
                if next_time_out is None:
                    break  # Stop if 'Time Out' is missing or invalid
                if (parse_date_time(df.loc[j + 1]['Time']) - next_time_out).days == 1:
                    consecutive_days += 1
                    j += 1
                else:
                    break

            if consecutive_days >= 7:
                print(f"Employee {current_row['Employee Name']} has worked for 7 consecutive days.")

        # b) Check for employees with less than 10 hours between shifts but greater than 1 hour
        time_between_shifts = next_time - current_time_out
        if timedelta(hours=1) < time_between_shifts < timedelta(hours=10):
            print(f"Employee {current_row['Employee Name']} has less than 10 hours between shifts but greater than 1 hour.")

        # c) Check for employees who have worked for more than 14 hours in a single shift
        shift_duration = current_time_out - current_time
        if shift_duration > timedelta(hours=14):
            print(f"Employee {current_row['Employee Name']} has worked for more than 14 hours in a single shift.")

def parse_date_time(date_time_str):
    try:
        return datetime.strptime(str(date_time_str), '%m/%d/%Y %I:%M %p')
    except (ValueError, TypeError):
        return None

if __name__ == "__main__":
    file_path = input("Enter the CSV file path: ")  # Prompt user for the file path
    analyze_employee_schedule(file_path)
