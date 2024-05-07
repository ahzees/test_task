# Image Converter API

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Test](#test)
- [Logging](#logging)
- [Dependencies](#dependencies)
- [Configuration](#configuration)

## Introduction
This project provides an API for converting uploaded images to grayscale. Utilizing FastAPI, the application is designed for high performance and scalability. It uses multithreading to handle image processing tasks efficiently, integrates Redis for caching results to improve response times for previously processed images, and incorporates comprehensive logging for troubleshooting and monitoring.

## Features
- **Multithreading for Image Processing:** Utilizes Python's `ThreadPoolExecutor` to manage image processing tasks concurrently.
- **Caching Mechanism:** Integrates Redis to store paths to converted images, reducing the need to reprocess the same files and speeding up response times for subsequent requests.
- **Robust File Handling:** Automatically saves uploaded files, converts them to grayscale, and manages file storage.
- **Detailed Logging:** Configures Python's logging library to track application activity and errors, aiding in debugging and ensuring the system's reliability.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.7 or higher
- Redis server (Ensure it is running on your system for caching functionalities)
- Environment management tool (e.g., poetry for dependency management)

### Installing
Follow these steps to set up the project on your local machine:

```bash
# Clone the repository
git clone git@github.com:ahzees/test_task.git
cd test_task

# Install dependencies using poetry
poetry install
poetry shell

#To run server from root
cd test_task

#Ensure that you have .env file
uvicorn main:app --reload
```
## Dependencies
Dependencies are listed in the `pyproject.toml` file and locked with `poetry.lock`, ensuring reproducible builds. Here’s how to manage them:

- Use `poetry add <package>` to add new packages.
- Run `poetry update` to update the dependencies.

## Usage
The main functionality is accessed through the /convert/ endpoint, which accepts image uploads and returns the grayscale image:
```bash
# Use fastapi openapi docs to send request
# Open in browser
http://127.0.0.1:8000/docs
#Then open /convert/ and send post request with file or send post request on
http://127.0.0.1:8000/convert/
```
### Test
Also, you can test project using unit test in test/ folder
```bash
#You have to be in the project root
cd tests
pytest
```
### Logging
To view log file u have to open test_task/images_logger.log
```bash
#using terminal
vim test_task/images_logger.log
```

## Configuration
- **Environment Variables:** Store sensitive information and configuration settings in a `.env` file which is loaded at runtime using `dotenv`.
- **Logging Configuration:** Adjust logging levels and handlers in `conf.py` to change how logs are captured and stored.
- **Redis Connection:** Modify Redis connection settings (`HOST`, `PORT`, `PASSWORD`) in your `.env` file as specified in `conf.py`.
