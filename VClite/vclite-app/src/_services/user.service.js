// Encloses All Backend API calls from here like logging in and out, registering, getting list of users, deletion of users etc.
import { authHeader } from '../_helpers/auth-header'

export const userService = {
    login,
    logout,
    //register,
    getAllUsers,
    //getById,
    //update
};

function login(username, password) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    };
    return fetch('http://127.0.0.1:8000/auth/obtain_token/', requestOptions)
        .then(handleResponse)
        .then(user => {
            // login successful if there's a jwt token in the response
            if (user.token) {
                // store user details and jwt token in local storage to keep user logged in between page refreshes
                localStorage.setItem('user', JSON.stringify(user));
            }

            return user;
        });
}

function getAllUsers() {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };

    return fetch('http://127.0.0.1:8000/apiv0/user/', requestOptions).then(handleResponse);
}


function logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('user');
}

// this method checks if the http response from the api is unauthorized and if yes will logout the user 
function handleResponse(response) {
    return response.text().then(text => {
        const data = text && JSON.parse(text);
        if (!response.ok) {
            if (response.status === 401) {
                // auto logout if 401 response returned from api
                logout();
                location.reload(true);
            }

            const error = (data && data.message) || response.statusText;
            return Promise.reject(error);
        }
        console.log(data);
        return data;
    });
}

