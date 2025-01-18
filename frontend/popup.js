const fetchButton = document.getElementById('fetch-btn');
const dataElement = document.getElementById('data');

// Establish a connection with the background script
const port = chrome.runtime.connect({ name: "popup" });

// Request data for the currently active tab
port.postMessage({ type: "REQUEST_ACTIVE_TAB_DATA" });

let number_value;

// Function to fetch data from the remote server
async function fetchData() {
  console.log("number_value when fetchData() is called", number_value);
  // Replace the URL with the endpoint you want to fetch data from
  const data = {
    value: number_value
  }

  console.log("JSON.stringify(data, null, 2) in fetchData(): ", JSON.stringify(data, null, 2));
  const url = 'https://asbjorn.eu.pythonanywhere.com/add_five';
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  }

  await fetch(url, options)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json(); // Assuming the server returns JSON
    })
    .then(data => {
      // Update the DOM with the fetched data
      dataElement.textContent = JSON.stringify(data, null, 2); // Format JSON for readability
    })
    .catch(error => {
      console.error('Error fetching data:', error);
      dataElement.textContent = 'Failed to fetch data. See console for details.';
    });
}

// Add a click event listener to the button
fetchButton.addEventListener('click', fetchData);



// Listen for the response and update the popup HTML
port.onMessage.addListener((message) => {
  if (message.type === "DATA_RESPONSE" && message.payload) {
    const { value } = message.payload;

    number_value = value;
  }
});


