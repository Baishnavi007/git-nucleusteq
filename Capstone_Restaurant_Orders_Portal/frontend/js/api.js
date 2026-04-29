const BASE_URL = "http://localhost:8080";

async function loginAPI(email, password) {
    const res = await fetch(`${BASE_URL}/auth/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ email, password })
    });
    return res.text();
}

async function registerAPI(data) {
    const res = await fetch(`${BASE_URL}/auth/register`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });
    return res.json();
}

async function getUserMenu(categoryId) {
    const res = await fetch(`${BASE_URL}/users/menu?categoryId=${categoryId}`);
    return res.json();
}

async function getOwnerMenu(categoryId) {
    const token = localStorage.getItem("token");

    const res = await fetch(`${BASE_URL}/owner/menu?categoryId=${categoryId}`, {
        headers: { "Authorization": "Bearer " + token }
    });
    return res.json();
}

async function addMenuItem(data) {
    const token = localStorage.getItem("token");

    const res = await fetch(
        `${BASE_URL}/owner/menu/add?categoryId=${data.categoryId}&name=${data.name}&description=${data.description}&price=${data.price}`,
        {
            method: "POST",
            headers: { "Authorization": "Bearer " + token }
        }
    );
    return res.json();
}