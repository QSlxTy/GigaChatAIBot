import aioboto3

from bot_start import logger
from src.config import BotConfig


class S3Cloud:
    _instance = None
    _logger = logger

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(S3Cloud, cls).__new__(cls)
        return cls._instance

    async def upload_file_bucket(self, path, name):
        async with aioboto3.Session().client(
                service_name='s3',
                endpoint_url='https://storage.yandexcloud.net',
                aws_access_key_id=BotConfig.yandex_access_key,
                aws_secret_access_key=BotConfig.yandex_secret_key,
                region_name=BotConfig.yandex_region
        ) as s3:
            await s3.upload_file(path, BotConfig.yandex_bucket_name, name)

    async def url_file_bucket(self, name):
        async with aioboto3.Session().client(
                service_name='s3',
                endpoint_url='https://storage.yandexcloud.net',
                aws_access_key_id=BotConfig.yandex_access_key,
                aws_secret_access_key=BotConfig.yandex_secret_key,
                region_name=BotConfig.yandex_region
        ) as s3:
            url = await s3.generate_presigned_url('get_object',
                                                  Params={'Bucket': BotConfig.yandex_bucket_name, 'Key': name},
                                                  ExpiresIn=172800)
            return url

    async def delete_file_bucket(self, name):
        async with aioboto3.Session().client(
                service_name='s3',
                endpoint_url='https://storage.yandexcloud.net',
                aws_access_key_id=BotConfig.yandex_access_key,
                aws_secret_access_key=BotConfig.yandex_secret_key,
                region_name=BotConfig.yandex_region
        ) as s3:
            await s3.delete_object(Bucket=BotConfig.yandex_bucket_name, Key=name)

    async def start_bucket(self, path, name):
        await self.upload_file_bucket(path, name)
        url = await self.url_file_bucket(name)
        return url, name


s3 = S3Cloud()
