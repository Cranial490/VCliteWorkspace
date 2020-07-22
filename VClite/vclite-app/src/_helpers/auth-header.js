// helper function returns  HTTP Authorization header containing the JWT

export function authHeader() {
    // return authorization header with jwt token
    let user = JSON.parse(localStorage.getItem('user'));

    if (user && user.token) {
        return { 'Authorization': 'JWT ' + user.token };
    } else {
        return {};
    }
}