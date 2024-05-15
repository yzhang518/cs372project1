## Getting Started
These instructions will guide you through setting up and running the project on your local machine for evaluation purposes.

### Prerequisites
- Ensure Python 3.12.1 is installed on your machine.

### Setup

1. **Extract the Project**:
   - Extract the zipped file to your preferred location.

2. **Install Required Packages**:
   - Navigate to the project directory.
   - Run the following command to install the required packages:
   
     pip install -r requirements.txt
     

### Running the Application

1. **Start the Monitoring Service**:
   - We will be running two Monitoring services.
      So we need to open two command line window.

   For window 1:
      - Navigate to the folder where `monitor.py` is located.
      - Run the following command to start the echo server:
      ```
      python monitor.py 127.0.0.1 65432
      ```
      - After running the command, you should see the message 
      "Server listening on 127.0.0.1:65432" 
      This indicates that the monitor service is up and ready.
      - Keep this window open.

   For window 2:
      - Navigate to the folder where `monitor.py` is located.
      - Run the following command to start the echo server:
      ```
      python monitor.py 127.0.0.1 65433
      ```
      - After running the command, you should see the message 
      "Server listening on 127.0.0.1:65433" 
      This indicates that the monitor service is up and ready.
      - Keep this window open.

2. **Start the Management Service**:
   - Open another command line window.
   - Navigate to the same directory.
   - Run the following command to start monitoring the services:
     ```
     python mgmt.py
     ```
     

### Stopping the Application

- To stop Management Service, 
	simply press `Ctrl + C` or `Ctrl + Z`. Upon doing this, you will see the message 
	"Shutdown signal received" And the process is being properly terminated.
- To stop Monitoring Service, 
	simply close out the command line windows.

