Local Sharer
A simple, self-hosted file sharing application that runs on your local network. Built from scratch with Python's standard libraries, this application allows you to easily transfer files between devices (like your computer and phone) without needing an internet connection or any third-party services.

✨ Features
Web-Based UI: Access the application from any device on your network with a web browser. No client software needed.

File Uploads & Downloads: Easily upload files to the server and download shared files from it.

Automatic Device Discovery: The application can automatically find other devices running the same server on the network (feature implemented in the backend).

Zero Dependencies: Runs using only the standard libraries included with Python 3.

📂 Project Structure
The project is organized into a backend for server logic and a frontend for the user interface.

local_share_app/
├── backend/
│   ├── main.py                 # The main server application
│   ├── discovery_handler.py    # Logic for network device discovery
│   └── transfer_handler.py     # Logic for handling file uploads
│
├── frontend/
│   ├── success.html            # The page shown after a successful upload
│   └── style.css               # The dark-themed CSS for the UI
│
├── uploads/                    # Default folder for uploaded files
└── shared/                     # Place files here to make them downloadable

🚀 Manual Setup and Installation
Follow these steps to get the server running on your machine.

Prerequisites
Python 3: Make sure you have Python 3 installed on your system.

Set Up the Project Folders
Before running the server, you need to create the folders where files will be stored. In the root directory of the project, create the following folders if they don't exist:

uploads/

shared/

▶️ Running the Application
Open your terminal.

Navigate into the backend/ directory:

cd backend/

Run the main.py script:

python3 main.py

If everything is set up correctly, you will see a message:
Server is running on http://0.0.0.0:8080

💻 How to Use
Find your computer's local IP address.

On Windows, run ipconfig in the command prompt.

On macOS or Linux, run ifconfig or ip addr in the terminal.

Look for an address that looks like 192.168.x.x.

On any device on the same Wi-Fi network (your phone, another laptop, etc.), open a web browser and navigate to:
http://YOUR_IP_ADDRESS:8080
(e.g., http://192.168.1.104:8080)

You will now see the application's main page, where you can upload and download files.
