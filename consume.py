import functools
import pika
import config

encoding = 'utf-8'

def file_write(filename, msg):
    fp = open(filename, "a")
    fp.write(msg + "\n")
    fp.close()


def on_message(chan, method_frame, _header_frame, body):
    """Called when a message is received. Log message and ack it."""
    msg = body.decode(encoding)
    print('Receive: ' + msg)
    if config.CONSUME_LOGFILE != '':
        file_write(config.CONSUME_LOGFILE, msg)
    chan.basic_ack(delivery_tag=method_frame.delivery_tag)


def main():
    """Main method."""
    credentials = pika.PlainCredentials(config.RABBITMQ_USER, config.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(config.RABBITMQ_HOST, credentials=credentials, virtual_host=config.TARGET_VHOST)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.exchange_declare(
        exchange=config.TARGET_QUEUE,
        exchange_type='direct',
        passive=False,
        durable=True,
        auto_delete=False)
    channel.queue_declare(queue=config.TARGET_QUEUE)
    channel.queue_bind(
        queue=config.TARGET_QUEUE, exchange=config.TARGET_QUEUE, routing_key=config.TARGET_QUEUE)
    channel.basic_qos(prefetch_count=config.CONSUME_QOS)

    on_message_callback = functools.partial(on_message)
    channel.basic_consume(config.TARGET_QUEUE, on_message_callback)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    connection.close()


if __name__ == '__main__':
    main()
