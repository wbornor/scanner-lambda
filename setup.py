import os
from setuptools import setup

setup(
    name="scanner-lambda",
    version="0.0.1",
    author="Wesley Bornor",
    author_email="wbornor+github@gmail.com",
    description="Ingest scanner events (barcode, qr) triggering additional actions.",
    license="Apache2",
    keywords="barcode,upc,qr",
    url="https://github.com/wbornor/scanner-lambda",
    install_requires=[
        'boto3'
    ]
)
