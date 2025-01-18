// Listen for messages from the background script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "GET_TAB_DATA") {
    // Retrieve data from the DOM
    let number = document.getElementById("number").innerText;

    const dataFromDOM = {
      value: number,
    };
    sendResponse(dataFromDOM); // Respond with the DOM data
  }
});