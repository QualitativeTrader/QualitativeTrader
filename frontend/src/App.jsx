import { useState } from 'react'
import './App.css'

function App() {
  const [formData, setFormData] = useState({ email: '' });

  const handleInputChange = (e) => {
    const {value} = e.target;
    setFormData({
      email: value
    });
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://localhost:8000/register/', {
        method: 'POST',
        body: JSON.stringify(formData),
    });

    const data = await response.json();
    console.log(data);
  };


  
  return (
    <>
      <form onSubmit={handleSubmit}>
          <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleInputChange}
          />
          <button type="submit">Register</button>
      </form>
    </>
  )
}

export default App
