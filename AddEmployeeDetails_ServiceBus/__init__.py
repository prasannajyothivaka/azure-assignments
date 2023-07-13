import csv, json, random, logging
import azure.functions as func
from azure.servicebus import ServiceBusClient, ServiceBusMessage

subscription_name = "TopicTriggerSubscription"
topic_name = "topic-trigger"
connection_string = "Endpoint=sb://thirdassignmenttesting.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=WN0D3mfn1AnEKgt/uSNUlq3N501M2TovO+ASbJzK3aQ="
employee_id = random.randint(10000, 99999)
message_body = f'{{"employeeId": "{employee_id}","name": "John","dob": "1990-05-15","position": "Quality Assurance"}}'

def send_message_to_service_bus_topic(topic_name, connection_string, message_body):
    servicebus_client = ServiceBusClient.from_connection_string(connection_string)
    sender = servicebus_client.get_topic_sender(topic_name)
    try:
        message = ServiceBusMessage(message_body)
        sender.send_messages(message)
    finally:
        servicebus_client.close()

def receive_messages_from_service_bus_subscription(topic_name, subscription_name, connection_string, max_messages=1):
    servicebus_client = ServiceBusClient.from_connection_string(connection_string)
    receiver = servicebus_client.get_subscription_receiver(topic_name, subscription_name, prefetch=max_messages)
    try:
        with receiver:
            messages = receiver.receive_messages(max_message_count=max_messages)
            for message in messages:
                print(f"Received message: {message}")
                data = json.loads(str(message))
                employee_details = {
                    'EmployeeID': data['employeeId'],
                    'Name': data['name'],
                    'DOB': data['dob'],
                    'Position': data['position']
                }
                csv_file = 'employees.csv'
                with open(csv_file, 'a', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=employee_details.keys())
                    writer.writerow(employee_details)
                
                receiver.complete_message(message)
    finally:
        servicebus_client.close()

def main(message: func.ServiceBusMessage):
    message_content_type = message.content_type
    message_body = message.get_body().decode("utf-8")

    logging.info("Python ServiceBus topic trigger processed message.")
    logging.info("Message Content Type: " + message_content_type)
    logging.info("Message Body: " + message_body)

    send_message_to_service_bus_topic(topic_name, connection_string, message_body)
    receive_messages_from_service_bus_subscription(topic_name, subscription_name, connection_string, max_messages=5)
