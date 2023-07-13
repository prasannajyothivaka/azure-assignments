import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Get the request body
        req_body = req.get_json()

        # Read the operation from the request body
        operation = req_body.get('Operation')

        if operation == 'AddEmployee':
            # Read EmployeeID, Name, DOB, Position from the request body
            employee_id = req_body.get('EmployeeID')
            name = req_body.get('Name')
            dob = req_body.get('DOB')
            position = req_body.get('Position')

            data = 'AddEmployeeDetails', 'your-subscription-name', 'your-connection-string', {
                'employeeId': employee_id,
                'name': name,
                'dob': dob,
                'position': position
            }

            # Send the message to the AddEmployeeDetails_ServiceBus topic subscription

        elif operation == 'DeleteEmployee':
            # Read EmployeeID from the request body
            employee_id = req_body.get('EmployeeID')

            # Send the message to the DeleteEmployeeDetails_ServiceBus queue

        else:
            return func.HttpResponse("Invalid operation.", status_code=400)

        return func.HttpResponse(f"Operation '{operation}' processed successfully.")

    except Exception as e:
        logging.error(f"Error processing the request: {str(e)}")
        return func.HttpResponse("Internal Server Error.", status_code=500)
