// Define your ABC class
class Item {
    constructor() {
      this.BookTitle = 'HarryYes';
    }
  }
  
  // Create an instance of the ABC class
  const myObject = new Item();
  
  // Convert the object to JSON format
  const jsonData = JSON.stringify(myObject);
  
  // Send the JSON data as a POST request to a server
  fetch('<your server URL>', {
    method: 'POST',

    body: jsonData,
  })
  .then(response => console.log('Object sent to server:', jsonData))
  .catch(error => console.error('Error sending object to server:', error));
  