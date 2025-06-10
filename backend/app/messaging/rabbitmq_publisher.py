import aio_pika
import json
import asyncio

RABBITMQ_URL = "amqp://guest:guest@rabbitmq/"

async def publish_download_message(message: dict):
    # Conecta ao RabbitMQ
    connection = await aio_pika.connect_robust(RABBITMQ_URL)

    # Cria canal de comunicação
    channel = await connection.channel()

    # Declara (ou garante existência da) fila
    queue = await channel.declare_queue("download_queue", durable=True)

    # Publica mensagem na fila
    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(message).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT  # Garante que a mensagem não se perca
        ),
        routing_key=queue.name
    )

    await connection.close()
