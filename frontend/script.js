// This line waits for the entire HTML page to be loaded before running any code.
document.addEventListener('DOMContentLoaded', () => {

    // Get references to the HTML elements we need to interact with.
    const refreshButton = document.getElementById('refresh-btn');
    const deviceList = document.getElementById('device-list');

    // Add a "click" event listener to the refresh button.
    // The 'fetchDevices' function will run every time the button is clicked.
    refreshButton.addEventListener('click', fetchDevices);

    // This is the main function that talks to our Python backend.
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
});
