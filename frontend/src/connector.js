class CustomConnector {
  constructor() {
    this.host = "http://localhost:8000";
  }

  async onSearch(query, options) {
    const response = await fetch(this.host + "/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        query,
        options
      })
    });
    return response.json();
  }

  async onAutocomplete(query, options) {
    const response = await fetch(this.host + "/autocomplete", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        query,
        options
      })
    });
    return response.json();
  }
}

export default CustomConnector