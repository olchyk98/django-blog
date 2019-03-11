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
    });
}