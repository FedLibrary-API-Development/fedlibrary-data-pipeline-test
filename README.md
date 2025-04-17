# API to SQL Server Data Pipeline

This Python script fetches resource data from an API endpoint and inserts it into a SQL Server database on a scheduled interval using the `schedule` library.

## Features

- Fetch data from a REST API
- Insert into a local SQL Server database
- Runs every minute (adjustable)
- Logs success and errors

## Requirements

- Python 3.x
- SQL Server with the required table created
- ODBC Driver 17 for SQL Server

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/api_to_sqlserver_pipeline.git
   cd api_to_sqlserver_pipeline
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Edit the connection string and API URL in `config.py` as needed.

4. Run the script:
   ```
   python main.py
   ```
5. If successful, you’ll see logging entries in pipeline.log.   
   