import logo from './logo.svg';
import './App.css';
import {useCallback, useEffect, useState} from 'react';

function loadTweets(callback){
  const xhr = new XMLHttpRequest()
  const method = 'GET'
  const url = 'http://127.0.0.1:8000/tweets'
  const responseType = 'json'

  //Lets xhr request know it's getting json back
  xhr.responseType = responseType
  xhr.open(method,url)
  //What gets created when the function triggers
  xhr.onload = function (){
    callback(xhr.response, xhr.status)
  }
  xhr.onerror = function(e){
    console.log(e)
    callback({"message": "The request was an error"}, 400)
  }
//triggers the request
  xhr.send()
}

function App() {
    const [tweets, setTweets] = useState([{content:"123"}])

    useEffect(()=>{
      const myCallback = (response, status)=>{
        if(status===200){
          setTweets(response)
        }
      }
      loadTweets(myCallback)
      // const tweetItems = [{"content": 123}, {"content": "Hello World"}]
      
    }, [])
    
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <p>
          {tweets.map((tweet, index)=>{
            return <li>{tweet.content}</li>
          })}

        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
