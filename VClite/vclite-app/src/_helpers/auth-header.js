// helper function returns  HTTP Authorization header containing the JWT

export function authHeader() {
    // return authorization header with jwt token
    if (localStorage.getItem('user') && localStorage.getItem('access_token')) {

        return { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') };
    } else {
        return {};
    }
}