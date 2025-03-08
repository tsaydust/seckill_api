from kafka import KafkaConsumer
import settings
import json
import asyncio
from utils.cache import sec_redis
from loguru import logger
from models import AsyncSessionFactory
from models.order import Order
from utils.alipay_service import alipay_service


async def seckill_queue_handle():
    consumer = KafkaConsumer(
        'seckill',
        auto_offset_reset='latest',
        bootstrap_servers=[settings.KAFKA_SERVER],
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    print('正在监听中...')
    for message in consumer:
        seckill_dict = message.value
        seckill_id = seckill_dict['seckill_id']
        user_id = seckill_dict['user_id']
        count = seckill_dict['count']
        address = seckill_dict['address']

        seckill = await sec_redis.get_seckill(seckill_id)
        if not seckill:
            logger.info(f'{seckill_id}秒杀商品不存在！')
        if count > seckill['sk_per_max_count']:
            logger.info(f"{user_id}抢购了{count}，超过了{seckill['sk_per_max_count']}")
        async with AsyncSessionFactory() as session:
            async with session.begin():
                order = Order(
                    user_id=user_id, seckill_id=seckill_id, count=count,
                    amount=seckill['sk_price']*count,
                    address=address
                )
                session.add(order)
            await session.refresh(order, attribute_names=['seckill'])
        alipay_order = alipay_service.app_pay(
            out_trade_no=str(order.id),
            total_amount=float(order.amount),
            subject=seckill['commodity']['title']
        )
        await sec_redis.add_order(order, alipay_order['alipay_order'])


async def main():
    await seckill_queue_handle()


if __name__ == '__main__':
    asyncio.run(main())