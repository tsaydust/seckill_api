from pydantic import BaseModel, ConfigDict


class BuySchema(BaseModel):
    # 把整形，转换为字符串类型
    model_config = ConfigDict(coerce_numbers_to_str=True)
    seckill_id: int
    count: int
    # 这里传的是地址的具体信息，比如：北京市朝阳区xxx，而不是存储address_id
    address: str