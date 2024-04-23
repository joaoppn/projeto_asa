import pika
import logging
from .config import config

logger = logging.getLogger(__name__)
logging.getLogger("pika").propagate = False
FORMAT = (
    "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
)
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)


class Publisher(object):
    def publish(self, routing_key, message):
        try:
            connection = self.create_connection()
            channel = connection.channel()

            channel.exchange_declare(exchange=config["exchange"], exchange_type="topic")
            channel.queue_declare(queue=config["queue"])
            channel.queue_bind(
                exchange=config["exchange"],
                queue=config["queue"],
                routing_key=routing_key,
            )

            channel.basic_publish(
                exchange=config["exchange"], routing_key=routing_key, body=message
            )

            connection.close()

        except Exception as e:
            logger.error(f"Erro na conexão do RabbitMQ: {e}")

    def create_connection(self):
        param = pika.ConnectionParameters(host=config["host"], port=config["port"])
        return pika.BlockingConnection(param)
