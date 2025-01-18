// Handle messages and connections from the popup
chrome.runtime.onConnect.addListener((port) => {
  if (port.name === "popup") {
    port.onMessage.addListener((message) => {
      if (message.type === "REQUEST_ACTIVE_TAB_DATA") {
        // Query the active tab
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          if (tabs.length > 0) {
            const activeTab = tabs[0];

            // Send a message to the content script in the active tab
            chrome.tabs.sendMessage(
              activeTab.id,
              { type: "GET_TAB_DATA" },
              (response) => {
                // Relay the response back to the popup
                port.postMessage({ type: "DATA_RESPONSE", payload: response });
              }
            );
          }
        });
      }
    });
  }
});
