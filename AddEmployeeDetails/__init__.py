import logging
import json
import csv
from azure.functions import HttpRequest, HttpResponse

def main(req: HttpRequest) -> HttpResponse:
    logging.info('Add Employee Details Start')

    try:
        req_body = req.get_json()
        employee_id = req_body.get('EmployeeID')
        name = req_body.get('Name')
        dob = req_body.get('DOB')
        position = req_body.get('Position')

        if not all([employee_id, name, dob, position]):
            return HttpResponse(
                "One or more input parameters are missing.",
                status_code=400
            )

        employee_details = {
            'EmployeeID': employee_id,
            'Name': name,
            'DOB': dob,
            'Position': position
        }

        csv_file = 'employees.csv'
        with open(csv_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=employee_details.keys())
            writer.writerow(employee_details)

        response = {
            'status': 'success',
            'message': 'Employee details added successfully',
            'data': employee_details
        }

        return HttpResponse(json.dumps(response), mimetype='application/json')

    except ValueError:
        return HttpResponse(
            "Invalid JSON payload in the request body.",
            status_code=400
        )
