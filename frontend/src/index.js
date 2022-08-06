import React, {useState} from 'react';
import ReactDOM from 'react-dom';
import Board from './components/Board';
import {BrowserRouter, Switch, Route, Redirect} from "react-router-dom";
import Register from "./components/Register";


function App() {
  const [token, setToken] = useState();
  return (
    <BrowserRouter>
      <Switch>
        <Route exact path="/">
          {
            !token ? 
            <Redirect to="/register" /> :
            <Board token={token} />
          }
        </Route>
        <Route path="/register">
          <Register setToken={setToken}/>
        </Route>
      </Switch>
    </BrowserRouter>
  )
}


ReactDOM.render(
  <App />,
document.getElementById('root')
);
