window.onload = function() {
    const fields = {
        title: "Type your title here",
        content: 'Hello, World!',
        image: null
    }

    document.querySelector("#newpost-title").textContent = fields.title;
    document.querySelector("#newpost-content").textContent = fields.content;

    { // Image preview section
        let cachedIMG = "";

        document.querySelector("#newpost-imageinp").addEventListener('change', ({ target: { files: [a] } }) => {
            fields.image = a;

            URL.revokeObjectURL(cachedIMG);
            cachedIMG = URL.createObjectURL(a);
            
            const image = document.createElement('img');
            image.src = cachedIMG;
            image.alt = "Preview";

            const b = document.querySelector("#newpost-image");
            b.innerHTML = '';
            b.appendChild(image)
        });
    }

    document.getElementById("newpost-submit").addEventListener('click', function() {
        const { title, content, image } = fields;
        if(!title.replace(/\s|\n/g, "").length || !content.replace(/\s|\n/g, "").length || !image) return;

        const prevSContent = this.textContent; // Previous text content

        this.contentType = "Loading...";
        this.disabled = true;

        // Post
        fetch(`${ window._HOSTPATH_ }/write/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken")
            },
            body: (() => {
                const a = new FormData();

                a.append('data', JSON.stringify({
                    title, content
                }))
                a.append('image', image);

                return a
            })()
        }).then((res) => {
            if(res.ok) {
                return res.json();
            } else {
                throw new Error(`Error ${ res.status } (${ res.statusText })`);
            }
        }).then((res) => {
            this.contentType = prevSContent;
            this.disabled = false;

            switch(res.status) {
                case 200: // Success
                    alert("Success");
                    window.location.reload();
                break;
                case 500: // Session wasn't confirmed
                    window.location.href = window._HOSTPATH_;
                break;
                default:break;
            }
        }).catch(console.error);
    });
}