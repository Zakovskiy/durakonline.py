from setuptools import setup, find_packages

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name = "durakonline.py",
    version = "3.4.1",
    url = "https://github.com/Zakovskiy/durakonline.py",
    download_url = "https://github.com/Zakovskiy/durakonline.py/tarball/master",
    license = "MIT",
    author = "Zakovskiy",
    author_email = "gogrugu@gmail.com",
    description = "A library to create Durak Online bots.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    keywords = [
        "durak",
        "online",
        "durakonline",
        "durakonline.py",
        "durakonline-bot",
        "rstgame",
        "rstgames",
        "api",
        "socket",
        "python",
        "python3",
        "python3.x",
        "zakovskiy",
        "official"
    ],
    install_requires = [
        "setuptools",
        "requests",
        "loguru",
        "aiohttp"
    ],
    setup_requires = [
        "wheel"
    ],
    packages = find_packages()
)
