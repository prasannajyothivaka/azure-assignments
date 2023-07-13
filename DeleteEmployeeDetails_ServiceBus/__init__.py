import logging
import random
import json
import azure.functions as func
from azure.servicebus import ServiceBusClient, ServiceBusMessage

employee_id = random.randint(10000, 99999)
data = f'{{"employeeId": "{employee_id}"}}'
queue_name = "queue-trigger"
connection_string = "Endpoint=sb://thirdassignmenttesting.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=WN0D3mfn1AnEKgt/uSNUlq3N501M2TovO+ASbJzK3aQ="
message_body = data
    
def queue_message_to_service_bus(queue_name, connection_string, message_body):
    servicebus_client = ServiceBusClient.from_connection_string(connection_string)
    sender = servicebus_client.get_queue_sender(queue_name)
    message = ServiceBusMessage(message_body)
    with sender:
        sender.send_messages(message)
    servicebus_client.close()

def receive_messages_from_service_bus(queue_name, connection_string, max_messages=1):
    servicebus_client = ServiceBusClient.from_connection_string(connection_string)
    receiver = servicebus_client.get_queue_receiver(queue_name, prefetch=max_messages)
    try:
        with receiver:
            messages = receiver.receive_messages(max_message_count=max_messages)
            print("reading messages")
            for message in messages:
                print(f"Received message: {message}")
                data = json.loads(str(message))
                employee_id = data['employeeId']
                employee_id = str(employee_id)

                csv_file_path = "employees.csv"
                lines = []
                with open(csv_file_path, 'r') as file:
                    for line in file:
                        if not line.startswith(employee_id + ','):
                            lines.append(line)

                with open(csv_file_path, 'w') as file:
                    for line in lines:
                        file.write(line)

                receiver.complete_message(message) 
    finally:
        servicebus_client.close()

def main(msg: func.ServiceBusMessage):
    logging.info('Python ServiceBus queue trigger processed message: %s',
                 msg.get_body().decode('utf-8'))
    
    queue_message_to_service_bus(queue_name, connection_string, message_body)
    receive_messages_from_service_bus(queue_name, connection_string, max_messages=5)
