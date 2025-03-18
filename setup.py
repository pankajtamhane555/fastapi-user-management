from setuptools import setup, find_packages

setup(
    name="user-management-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.110.0",
        "sqlalchemy>=2.0.27",
        "alembic>=1.13.1",
        "python-jose>=3.3.0",
        "passlib>=1.7.4",
        "python-multipart>=0.0.9",
        "email-validator>=2.1.0.post1",
        "psycopg2-binary>=2.9.9",
        "bcrypt>=4.1.2",
        "python-dotenv>=1.0.1",
        "oso>=0.27.0",
    ],
)
