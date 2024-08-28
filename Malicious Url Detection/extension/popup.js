function checkPermissions() {
  var url = document.getElementById('urlInput').value;
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, { action: 'checkPermissions', url: url }, function(response) {
      document.getElementById('result').textContent = response.permissions;
    });
  });
}
