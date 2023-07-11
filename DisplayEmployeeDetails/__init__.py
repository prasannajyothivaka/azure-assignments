import logging
import azure.functions as func
import csv
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('DisplayEmployeeDetails Start')

    employee_id = req.params.get('EmployeeID')

    if not employee_id:
        return func.HttpResponse(
            "EmployeeID parameter is missing.",
            status_code=400
        )

    csv_file = 'employees.csv'
    employee_details = []

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)

        if employee_id == '0':
            # If EmployeeID is 0, return all entries present in the CSV file
            for row in reader:
                employee_details.append({
                    'EmployeeID': row[0],
                    'Name': row[1],
                    'DOB': row[2],
                    'Position': row[3]
                })
        else:
            # Find the details of the employee with the specified EmployeeID
            for row in reader:
                if row[0] == employee_id:
                    employee_details.append({
                        'EmployeeID': row[0],
                        'Name': row[1],
                        'DOB': row[2],
                        'Position': row[3]
                    })
                    break

    if not employee_details:
        return func.HttpResponse(
            "Employee details not found.",
            status_code=404
        )

    response = {
        'status': 'success',
        'message': 'Employee details retrieved successfully',
        'data': employee_details
    }

    return func.HttpResponse(json.dumps(response), mimetype='application/json')