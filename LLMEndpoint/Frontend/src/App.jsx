import { useState } from 'react'
import './App.css'
import ReactMarkdown from 'react-markdown'

function App() {
  var endpointUrl = "http://localhost:8000/LLMChat"

  const [userInput, setUserInput] = useState("");
  const [systemOutput, setSystemOutput] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();

    var response = await fetch(endpointUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_input: userInput })
    });

    const streamReader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await streamReader.read();
      if (done) {
        break
      }
      const chunk = decoder.decode(value, { stream: true });
      const line = JSON.parse(chunk);
      setSystemOutput((prev) => prev + line.text);
    }

  }

  return (
    <>
    <div className='response-area'>
      <ReactMarkdown>{systemOutput}</ReactMarkdown>
    </div>
      <div>
        <form onSubmit={handleSubmit}>
          <input type='text'
           name='userInput' 
           value={userInput} 
           onChange={(e)=>setUserInput(e.target.value)}
           placeholder='Enter example movie'>
           </input>
          <button type="submit"> submit </button>
        </form>
      </div>

    </>
  )
}

export default App
