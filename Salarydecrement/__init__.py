import datetime
import logging

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    salary_file_path = "salary.txt"

    with open(salary_file_path, "r+") as file:
        # Read the base salary from the file
        base_salary = float(file.read())

        # Calculate the new salary after decrement
        new_salary = base_salary * 0.99

        # Write the updated salary back to the file
        file.seek(0)
        file.write(str(new_salary))
        file.truncate()

    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    logging.info(f"Salary decreased. New salary: {new_salary}. Timestamp: {utc_timestamp}")
