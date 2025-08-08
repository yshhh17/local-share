// This line waits for the entire HTML page to be loaded before running any code.
document.addEventListener('DOMContentLoaded', () => {

    // --- DEVICE DISCOVERY SECTION ---

    // Get references to the HTML elements we need to interact with.
    const refreshButton = document.getElementById('refresh-btn');
    const deviceList = document.getElementById('device-list');

    // Add a "click" event listener to the refresh button.
    // The 'fetchDevices' function will run every time the button is clicked.
    refreshButton.addEventListener('click', fetchDevices);

    // This is the main function that talks to our Python backend for discovery.
    function fetchDevices() {
        // Clear the current list and show a "searching" message.
        deviceList.innerHTML = '<li class="no-devices">Searching for devices...</li>';

        // Use the browser's built-in 'fetch' function to make a request
        // to the API endpoint we created in main.py.
        fetch('/api/discovery')
        .then(response => {
            // When the server responds, we first check if the response was successful.
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // We get the response body as plain text.
            return response.text();
        })
        .then(data => {
            // 'data' is the comma-separated string of IP addresses from our server.

            // Clear the "searching" message.
            deviceList.innerHTML = '';

            if (data) {
                // Split the string into an array of individual IPs.
                const ips = data.split(',');

                // Loop through each IP and create a new list item for it.
                ips.forEach(ip => {
                    const listItem = document.createElement('li');
                    listItem.textContent = ip.trim(); // .trim() removes any extra spaces
                    deviceList.appendChild(listItem);
                });
            } else {
                // If the server returns an empty string, show a "not found" message.
                deviceList.innerHTML = '<li class="no-devices">No devices found.</li>';
            }
        })
        .catch(error => {
            // If anything goes wrong with the fetch request, show an error message.
            console.error('Error fetching devices:', error);
            deviceList.innerHTML = '<li class="no-devices">Error finding devices. Check console.</li>';
        });
    }


    // --- FILE UPLOAD SECTION ---

    // Get references to the new HTML elements for the upload form.
    const uploadForm = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');

    // Add a "submit" event listener to the form.
    uploadForm.addEventListener('submit', event => {
        // Prevent the browser's default form submission behavior.
        event.preventDefault();

        const file = fileInput.files[0];

        if (!file) {
            alert('Please select a file first!');
            return;
        }

        // Wrap the file in a FormData object. This is the correct, modern way.
        const formData = new FormData();
        formData.append('file', file);

        // Make the fetch call WITHOUT the manual headers object.
        // The browser will automatically create the correct 'Content-Type'
        // header with the necessary boundary string.
        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server responded with ${response.status}`);
            }
            return response.text();
        })
        .then(result => {
            alert('File sent successfully!');
            console.log('Server response:', result);
            uploadForm.reset(); // Clear the file input
        })
        .catch(error => {
            console.error('Error uploading file:', error);
            alert('Error uploading file. See console for details.');
        });
    });
});
