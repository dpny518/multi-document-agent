import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://backend:8000/query', { query });
      setResponse(res.data.response);
    } catch (error) {
      console.error("There was an error!", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Multi-Document Query App</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your query"
          />
          <button type="submit">Submit</button>
        </form>
        {response && <div className="response"><h2>Response:</h2><p>{response}</p></div>}
      </header>
    </div>
  );
}

export default App;
