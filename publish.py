import pika
import config
import time

def main():
    """Main method."""
    credentials = pika.PlainCredentials(config.RABBITMQ_USER, config.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(config.RABBITMQ_HOST, credentials=credentials, virtual_host=config.TARGET_VHOST)

    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=config.TARGET_QUEUE)

        counter = 0

        while True:
            if connection == '' and config.SEND_KEEP_CONNECTION == False:
                connection = pika.BlockingConnection(parameters)
                channel = connection.channel()
                channel.queue_declare(queue=config.TARGET_QUEUE)
            counter += 1
            if config.SEND_FLAG == 1:
                msg = str(counter)
            elif config.SEND_FLAG == 2:
                current_milli_time = lambda: int(round(time.time() * 1000))
                msg = str(current_milli_time())

            channel.basic_publish(exchange='',
                                  routing_key=config.TARGET_QUEUE,
                                  body=msg)
            print("Sent: " + msg)
            if config.SEND_KEEP_CONNECTION == False:
                connection.close()
                connection = ''
            if counter >= config.SEND_COUNTER_LIMIT and config.SEND_COUNTER_LIMIT > 0:
                break
            time.sleep(config.SEND_DELAY)
    except KeyboardInterrupt:
        connection.close()


if __name__ == '__main__':
    main()
