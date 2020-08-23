from setuptools import setup, find_packages

setup(
    name="newbee",
    version="1.0.3",
    packages=find_packages(),
    url="https://gitee.com/yoopaa/newbee",
    author="showurl",
    author_email = "showurl@163.com",
    install_requires=[
        'django == 2.0.0',
        'pycryptodome',
        'djangorestframework-jwt'
    ],
    python_requires='>=3.5, <=3.7',
)
