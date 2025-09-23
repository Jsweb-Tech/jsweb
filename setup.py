# setup.py
import os

from setuptools import setup, find_packages

with open(os.path.join("jsweb", "__init__.py"), "r") as f:
    for line in f:
        if line.startswith("__VERSION__ = "):
            version = line.split("=")[1].strip().strip('\"')
            break
        else:
            version = "0.1.0"
            break

requirements = [
    'jinja2',
    "sqlalchemy",
    "werkzeug",
    "itsdangerous",
    "alembic",
]
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
setup(
    name="jsweb",
    version=version,
    install_requires=requirements,
    packages=find_packages(),
    keywords=["JsWeb", "Framework", "Web", "Python", "WSGI", "Web Server", "ORM", "Database", "Routing", "Authentication", "Forms", "CLI"],
    description="JsWeb - A lightweight and modern Python web framework designed for speed and simplicity.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Jones Peter",
    author_email="jonespetersoftware@gmail.com",
    url="https://github.com/Jones-peter/jsweb",
    license="MIT",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ],
    include_package_data=True,
    package_data={
        'jsweb': [
            'templates/*.html',
            'static/*.css',
            'project_templates/*.jinja',
        ]
    },
    entry_points={
        "console_scripts": [
            "jsweb=jsweb.cli:cli"
        ]
    },
    extras_require={
        "dev": ["watchdog", "websockets"],
        "qr": ["qrcode[pil]"],
        "postgresql": ["psycopg2-binary"],
    },
    project_urls={
        "Homepage": "https://github.com/Jones-peter/jsweb",
        "Bug Tracker": "https://github.com/Jones-peter/jsweb/issues",
    },
)
