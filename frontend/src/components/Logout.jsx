import React from "react";
import { Link, useHistory } from "react-router-dom";


function Logout(props) {
    const history = useHistory();


    function logoutUser() {
        localStorage.removeItem('token');
        history.push("/login");
    }
    return (
        <button onClick={logoutUser}>Log out</button>
    )
}

export default Logout;
