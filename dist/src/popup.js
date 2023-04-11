document.addEventListener('DOMContentLoaded', async function() {
    var myButton = document.getElementById('captureButton');
    myButton.addEventListener('click', async() => {
      console.log('Button clicked!');
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      chrome.tabs.sendMessage(tab.id, {type: 'init'}, (resp) => {
      });
    });
  });