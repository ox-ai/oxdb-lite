const apiUrlHead = "http://127.0.0.1:8000";

class Oxdb {
  constructor(apiUrl = apiUrlHead) {
    this.apiUrl = apiUrl;
  }

  async push(data) {
    const url = `${this.apiUrl}/push`;
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        const errorDetail = await response.json();
        throw new Error(`Error: ${response.status}, ${errorDetail.detail}`);
      }

      const result = await response.json();
      return 'ox-db : ' + result;

    } catch (error) {
      console.error('Error:', error);
      return { error: error.message };
    }
  }
}

// Example usage
const pushData = {
  data: "data",
  embeddings: true,
  description: "from ox-ai.studio api call",
  metadata: { source: "ox-ai.studio.api" },
  key: "key"
};

// const db = new Oxdb("http://127.0.0.1:8000");
// const result = await db.push(pushData);
// console.log(result)

module.exports = {
  Oxdb,
  pushData
  
};