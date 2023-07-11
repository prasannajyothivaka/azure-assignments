import logging
import azure.functions as func
import csv
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('DeleteEmployeeDetails start')

    employee_id = req.params.get('EmployeeID')

    if not employee_id:
        return func.HttpResponse(
            "EmployeeID parameter is missing.",
            status_code=400
        )

    csv_file = 'employees.csv'
    employee_details = []
    deleted_employee = None

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        employee_details = list(reader)

    with open(csv_file, 'w') as file:
        writer = csv.writer(file)
        
        for row in employee_details:
            if row[0] == employee_id:
                deleted_employee = row
            else:
                writer.writerow(row)

    if not deleted_employee:
        return func.HttpResponse(
            "Employee not found.",
            status_code=404
        )

    response = {
        'status': 'success',
        'message': 'Employee details deleted successfully',
        'data': {
            'EmployeeID': deleted_employee[0],
            'Name': deleted_employee[1],
            'DOB': deleted_employee[2],
            'Position': deleted_employee[3]
        }
    }

    return func.HttpResponse(json.dumps(response), mimetype='application/json')
