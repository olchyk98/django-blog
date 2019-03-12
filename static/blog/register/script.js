window.onload = function() {
    const fields = {
        name: '',
        login: '',
        password: ''
    }

    function setField(id, field) {
        document.getElementById(id).addEventListener('input', ({ target: { value: a } }) => {
            fields[field] = a;
        });
    }

    setField("register-fname", "name");
    setField("register-flogin", "login");
    setField("register-fpassword", "password");

    document.getElementById("register-form").addEventListener('submit', function(e) {
        e.preventDefault();
        
        function disableInputs(dis = true) {
            const a = document.getElementsByClassName('auth-form-disable');
            for(io of a) {
                io.disabled = dis;
            }
        }

        disableInputs(true);

        fetch(`${ window._HOSTPATH_ }/register/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken")
            },
            body: JSON.stringify({
                login: fields.login,
                name: fields.name,
                password: fields.password
            })
        }).then((res) => {
            disableInputs(false);
            if(res.ok) {
                return res.json();
            } else {
                throw new Error(`${ res.status } (${ res.statusText })`)
            }
        }).then((e) => {
            switch(e.status) {
                case 200: { // SUCCESS: registered
                    const a = document.getElementById('auth-form-message');
                    a.textContent = "Success";
                    a.classList.remove('error', 'hiden');
                    window.location.href = this.getAttribute('success-url');
                }
                break;
                case 400: { // ERROR: user exists
                    const a = document.getElementById('auth-form-message');
                    a.textContent = "User with this login already exists!";
                    a.classList.add('error');
                    a.classList.remove('hidden');
                }
                break;
                default:break;
            }
        }).catch(() => {
            disableInputs(false);
        });
    });
}