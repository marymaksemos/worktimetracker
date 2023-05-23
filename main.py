"""
Module: main
Description: WorkTimeTracker CLI application.
"""

from database_manager import (
    add_employer,
    add_work_hours,
    get_all_employers,
    get_work_hours_by_employer,
    calculate_monthly_hours,
    calculate_monthly_earnings,
)


def main_menu():
    """
    Display the main menu and handle user input.
    """
    print("WorkTimeTracker")
    print("--------------")
    print("1. Add Employer")
    print("2. Add Work Hours")
    print("3. View Employers")
    print("4. View Work Hours")
    print("5. Calculate Monthly Hours")
    print("6. Calculate Monthly Earnings")
    print("0. Exit")

    while True:
        choice = input("Select an option: ")

        if choice == "1":
            name = input("Enter employer name: ")
            additional_info = input("Enter additional information: ")
            hourly_rate = float(input("Enter hourly rate: "))
            add_employer(name, additional_info, hourly_rate)
            print("Employer added successfully.")
        elif choice == "2":
            employer_id = int(input("Enter employer ID: "))
            date = input("Enter date (YYYY-MM-DD): ")
            hours = float(input("Enter hours worked: "))
            add_work_hours(employer_id, date, hours)
            print("Work hours added successfully.")
        elif choice == "3":
            employers = get_all_employers()
            print("Employers:")
            for employer in employers:
                print(
                    f"ID: {employer.id}, Name: {employer.name}, "
                    f"Additional Info: {employer.additional_info}"
                )
        elif choice == "4":
            employer_id = int(input("Enter employer ID: "))
            work_hours = get_work_hours_by_employer(employer_id)
            print("Work Hours:")
            for work_hour in work_hours:
                print(
                    f"ID: {work_hour.id}, Date: {work_hour.date}, "
                    f"Hours: {work_hour.hours}"
                )
        elif choice == "5":
            employer_id = int(input("Enter employer ID: "))
            month = int(input("Enter month: "))
            year = int(input("Enter year: "))
            total_hours = calculate_monthly_hours(employer_id, month, year)
            print(f"Total hours for the month: {total_hours}")
        elif choice == "6":
            employer_id = int(input("Enter employer ID: "))
            month = int(input("Enter month: "))
            year = int(input("Enter year: "))
            pre_tax_earnings = calculate_monthly_earnings(
                employer_id, month, year, pre_tax=True
            )
            post_tax_earnings = calculate_monthly_earnings(
                employer_id, month, year, pre_tax=False
            )
            print(f"Pre-tax earnings for the month: {pre_tax_earnings}")
            print(f"Post-tax earnings for the month: {post_tax_earnings}")
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

        print()  # Print a blank line for readability


if __name__ == '__main__':
    main_menu()
    