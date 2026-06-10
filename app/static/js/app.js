async function generateVideo() {

    const niche =
        document.getElementById("niche").value;

    const resultDiv =
        document.getElementById("result");

    const loadingDiv =
        document.getElementById("loading");

    if (!niche.trim()) {

        resultDiv.innerHTML = `
        <div style="color:red">
            Please enter a niche
        </div>
        `;

        return;
    }

    loadingDiv.style.display = "block";

    resultDiv.innerHTML = "";

    try {

        const response =
            await fetch(
                "/api/content/generate",
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                        "application/json"
                    },
                    body: JSON.stringify({
                        niche
                    })
                }
            );

        const data =
            await response.json();

        loadingDiv.style.display =
            "none";

        if (!response.ok) {

            resultDiv.innerHTML = `
            <div style="color:red;">
                <h3>Error</h3>
                <pre>
${JSON.stringify(data,null,2)}
                </pre>
            </div>
            `;

            return;
        }

        resultDiv.innerHTML = `

        <div class="result-card">

            <h2>${data.title}</h2>

            <p>
                <strong>Status:</strong>
                ${data.status}
            </p>

            <p>
                <strong>Video:</strong>
                ${data.video_path}
            </p>

            <p>
                <strong>YouTube:</strong>
                <a href="${data.youtube_url}"
                   target="_blank">
                   Open Video
                </a>
            </p>

        </div>

        `;

    } catch(error){

        loadingDiv.style.display =
            "none";

        resultDiv.innerHTML = `
        <div style="color:red">
            ${error}
        </div>
        `;
    }
}