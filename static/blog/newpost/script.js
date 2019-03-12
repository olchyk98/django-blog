window.onload = function() {
    { // Image preview section
        let cachedIMG = "";

        document.querySelector("#newpost-imageinp").addEventListener("change", ({ target: { files: [a] } }) => {
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
}