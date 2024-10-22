function login() {
    console.log("login")
    var username = document.getElementById('login').value;
    var password = document.getElementById('pwd').value;
    //window.location.href = "/auth/login?username=" + username + "&password=" + password;


    var xhr = new XMLHttpRequest();
    xhr.open('GET', "/auth/login-action?username=" + username + "&password=" + password, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.status === 'success') {
                console.log("rrr", response)
                if (response.login === 'success') {
                    window.location.href = '/dashboard';
                }
                else {
                    alert("You are not an admin")
                }

            }

        }
    }
    xhr.send();
}

function printPage() {
            window.print();
        }