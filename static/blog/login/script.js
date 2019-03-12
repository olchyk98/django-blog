window.onload = function() {
    const fields = {
        login: '',
        password: ''
    }

    function setField(id, field) {
        document.getElementById(id).addEventListener('input', ({ target: { value: a } }) => {
            fields[field] = a
        });
    }

    setField("login-flogin", 'login');
    setField("login-fpassword", 'password');

    document.getElementById('login-form').addEventListener('submit', function(e) {
        e.preventDefault();

        function disableInputs(dis = true) {
            const a = document.getElementsByClassName('auth-form-input');
            for(io of a) {
                io.disabled = dis;                
            }
        }

        disableInputs(true);

        fetch(`${ window._HOSTPATH_ }/login/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken")
            },
            body: JSON.stringify({
                login: fields.login,
                password: fields.password
            })
        }).then((res) => {
            disableInputs(false);

            if(res.ok) {
                return res.json();
            } else {
                throw new Error(`Error ${ res.status } (${ res.statusText })`);
            }
        }).then((res) => {
            switch(res.status) {
                case 200: { // Success
                    const a = document.getElementById('auth-form-message');

                    a.classList.remove('error', 'hidden');
                    a.textContent = "Success!";

                    window.location.href = this.getAttribute('success-url');
                }
                break;
                case 400: { // Invalid data
                    const a = document.getElementById('auth-form-message');
                    a.textContent = "Invalid login or password!";
                    a.classList.add('error');
                    a.classList.remove('hidden');
                }
                break;
                default:break;
            }
        }).catch((err) => {
            disableInputs(false);
            console.error(err);
        });
    });
}