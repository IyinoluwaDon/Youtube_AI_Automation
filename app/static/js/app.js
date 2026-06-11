async function generateVideo() {

    const niche = document
        .getElementById("niche")
        .value
        .trim();

    if (!niche) {

        alert("Please enter a niche");

        return;
    }

    const generateBtn =
        document.getElementById(
            "generateBtn"
        );

    const progressSection =
        document.getElementById(
            "progressSection"
        );

    const progressFill =
        document.getElementById(
            "progressFill"
        );

    const progressText =
        document.getElementById(
            "progressText"
        );

    const resultSection =
        document.getElementById(
            "result"
        );

    generateBtn.disabled = true;

    progressSection.style.display =
        "block";

    resultSection.style.display =
        "none";

    progressFill.style.width =
        "0%";

    progressText.innerText =
        "Starting Pipeline...";

    const stages = [

        {
            pct: 10,
            text: "Generating Idea..."
        },

        {
            pct: 25,
            text: "Writing Script..."
        },

        {
            pct: 45,
            text: "Generating Voice..."
        },

        {
            pct: 65,
            text: "Downloading Videos..."
        },

        {
            pct: 80,
            text: "Generating Subtitles..."
        },

        {
            pct: 95,
            text: "Rendering Video..."
        }
    ];

    let stageIndex = 0;

    const interval = setInterval(() => {

        if (
            stageIndex <
            stages.length
        ) {

            progressFill.style.width =
                stages[
                    stageIndex
                ].pct + "%";

            progressText.innerText =
                stages[
                    stageIndex
                ].text;

            stageIndex++;
        }

    }, 2500);

    try {

        console.log(
            "Calling backend..."
        );

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

                        niche: niche
                    })
                }
            );

        if (!response.ok) {

            const errorText =
                await response.text();

            throw new Error(
                errorText
            );
        }

        const data =
            await response.json();

        console.log(data);

        clearInterval(
            interval
        );

        progressFill.style.width =
            "100%";

        progressText.innerText =
            "Video Generated Successfully";

        resultSection.style.display =
            "block";

        document
            .getElementById(
                "videoTitle"
            )
            .innerText =
            data.title ||
            "Generated Video";

        const videoPlayer =
            document
            .getElementById(
                "videoPlayer"
            );

        videoPlayer.src =
            data.video_path;

        videoPlayer.load();

        const youtubeLink =
            document
            .getElementById(
                "youtubeLink"
            );

        youtubeLink.href =
            data.youtube_url;

        youtubeLink.innerText =
            "Watch On YouTube";

    } catch (error) {

        clearInterval(
            interval
        );

        console.error(
            error
        );

        progressText.innerText =
            "Pipeline Failed";

        alert(
            "Error:\n\n" +
            error.message
        );
    }

    generateBtn.disabled = false;
}