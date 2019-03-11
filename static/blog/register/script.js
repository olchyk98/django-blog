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

    document.getElementById("register-form").addEventListener('submit', e => {
        e.preventDefault();
        console.log("REGISTER");
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
            if(res.ok) {
                return res.json();
            } else {
                throw new Error(`${ res.status } (${ res.statusText })`)
            }
        }).then((e) => {
            switch(e.status) {
                case 400: // ERROR: user exists
                    console.log("ERROR");
                break;
                case 200: // SUCCESS: registered
                    console.log("SUCCESS");
                break;
            }
        }).catch(console.error);
    });
}