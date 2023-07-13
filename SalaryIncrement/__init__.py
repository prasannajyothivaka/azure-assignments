import datetime
import logging
import os
import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    salary_file_path = os.path.join(os.getcwd(), 'salary.txt')

    # Read the current salary from the file
    with open(salary_file_path, 'r') as file:
        current_salary = float(file.read())

    # Calculate the incremented salary
    incremented_salary = current_salary * 1.025

    # Write the updated salary back to the file
    with open(salary_file_path, 'w') as file:
        file.write(str(incremented_salary))

    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

    logging.info(f'Salary increment function ran at {utc_timestamp}. Current salary: {current_salary:.2f}, '
                 f'Incremented salary: {incremented_salary:.2f}')
