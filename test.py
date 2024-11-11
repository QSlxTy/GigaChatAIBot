import asyncio
from utils.s3_test import S3Cloud


async def main():
    s3_cloud = S3Cloud()
    image_urls = await s3_cloud.upload_image_to_s3(['img.png'])
    print(image_urls)
if __name__ == '__main__':
    asyncio.run(main())