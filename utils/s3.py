import boto3

from bot_start import logger
from src.config import BotConfig


class S3Cloud:
    _instance = None
    _client = None
    _logger = logger
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=BotConfig.yandex_access_key,
        aws_secret_access_key=BotConfig.yandex_secret_key,
        region_name=BotConfig.yandex_region
    )

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(S3Cloud, cls).__new__(cls)
        return cls._instance

    def upload_file_bucket(self, path, name):
        self.s3.upload_file(path, BotConfig.yandex_bucket_name, name)

    def url_file_bucket(self, name):
        url = self.s3.generate_presigned_url('get_object',
                                                   Params={'Bucket': BotConfig.yandex_bucket_name, 'Key': name},
                                                   ExpiresIn=172800)
        return url

    async def start_bucket(self, path, name):
        self.upload_file_bucket(path, name)
        url = self.url_file_bucket(name)
        return url


s3 = S3Cloud()
