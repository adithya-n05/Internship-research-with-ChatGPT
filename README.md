# Company Information Markdown Generator

## Overview

This repository contains a Python script that generates detailed markdown files for various companies based on data from an Excel file and additional research using the OpenAI API. The script is designed to create comprehensive markdown files with information about each company's programs, application processes, general information, key facts, company culture, technologies, and tools.

## Features

- **Company Lists**: The script includes predefined lists of finance-related and tech-related companies.
- **Excel Data Integration**: Reads data from an Excel file (`Trackr Application Tracker 2024-25 Technology.xlsx`) to populate specific sections of the markdown files.
- **OpenAI API Integration**: Utilizes the OpenAI API to generate detailed content for each company based on a structured prompt.
- **Asynchronous Requests**: Uses `aiohttp` and `asyncio` for making asynchronous API requests to OpenAI.
- **Markdown File Generation**: Creates individual markdown files for each company with detailed information via prompt engineering a custom prompt for ChatGPT.

## Dependencies

- `aiohttp`
- `asyncio`
- `pandas`
- `openai`
- `base64`
- `os`

## Setup

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install the required Python packages**:
    ```sh
    pip install aiohttp pandas openai asyncio base64 os
    ```

3. **Set up OpenAI API Key**:
    Ensure you have your OpenAI API key set as an environment variable:
    ```sh
    export OPENAI_API_KEY='your-api-key'
    ```

4. **Place the Excel file**:
    Ensure the Excel file `Trackr Application Tracker 2024-25 Technology.xlsx` is in the root directory of the repository.

## Usage

Run the script to generate markdown files for the companies listed in the `tech_related` list:
```sh
python Prompt generator.py
```