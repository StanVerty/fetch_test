## Requirements
#### Python 3.11+
#### Google Chrome Browser
#### Chrome WebDriver (installed automatically using webdriver_manager)

## Setup
1. Clone the repository,
2. cd into project,
3. create a vertual environment and activate it,
4. Run coomand to install the required packages:
   pip install -r requirements.txt

## Running the Test
#### in visible mode:
pytest -v -s --tb=short {--headless=false}

#### in headless mode:
pytest -v -s --tb=short --headless=true
