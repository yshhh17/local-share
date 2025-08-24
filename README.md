# Local Sharer

A self-hosted file sharing app for your local network. Built with Python's standard libraries, it allows file transfers between devices without internet or third-party services.

## ✨ Features

- **Web UI:** Access via any browser on your network.
- **Uploads & Downloads:** Share files easily.
- **Device Discovery:** Finds other servers automatically.
- **Zero Dependencies:** Runs on Python 3 standard libraries.

## 📂 Project Structure

- local_share_app/
  - backend/
    - main.py — Main server application  
    - discovery_handler.py — Network device discovery logic  
    - transfer_handler.py — File upload handling  
  - frontend/
    - success.html — Page after successful upload  
    - style.css — Dark-themed CSS  
  - uploads/ — Default folder for uploaded files  
  - shared/ — Files here are downloadable
## 🚀 Setup

### Prerequisites
- Python 3

### Create Folders
In the project root:

uploads/
shared/

### Run the Server
```bash
cd backend/
python3 main.py
You should see:

Server is running on http://0.0.0.0:8080
💻 Usage
Find your local IP:

Windows: ipconfig

macOS/Linux: ifconfig or ip addr

Open on any device:

http://YOUR_IP_ADDRESS:8080
