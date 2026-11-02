let mediaRecorder = null;
let audioChunks = [];
let mediaStream = null;
let isRecording = false;


async function startCamera() {

    const video = document.getElementById("video");
    const status = document.getElementById("status");
    const cameraStatus = document.getElementById("cameraStatus");
    const placeholder = document.getElementById("cameraPlaceholder");

    if (!video) {
        console.log("Video element not found.");
        return;
    }

    try {

        mediaStream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: true
        });

        video.srcObject = mediaStream;

        if (placeholder) {
            placeholder.style.display = "none";
        }

        if (cameraStatus) {
            cameraStatus.innerText = "Camera ready";
        }

        if (status) {
            status.innerText = "Camera ready. Click Start Answer.";
        }

        const statusDot = document.getElementById("statusDot");

        if (statusDot) {
            statusDot.classList.add("active");
        }

        mediaRecorder = new MediaRecorder(mediaStream);

        mediaRecorder.ondataavailable = function(event) {

            if (event.data && event.data.size > 0) {
                audioChunks.push(event.data);
            }

        };


        mediaRecorder.onstop = async function() {

            console.log("Recording stopped.");

            if (audioChunks.length === 0) {

                alert("No audio was recorded.");

                return;
            }


            const audioBlob = new Blob(
                audioChunks,
                {
                    type: "audio/webm"
                }
            );


            const formData = new FormData();


            formData.append(
                "audio",
                audioBlob,
                "answer.webm"
            );


            /*
             IMPORTANT:
             Send the current question number
             to Flask.
            */

            let questionNumber =
                window.currentQuestionNumber || 1;


            formData.append(
                "question_number",
                questionNumber
            );


            console.log(
                "Sending question number:",
                questionNumber
            );


            if (status) {

                status.innerText =
                    "Processing your answer...";

            }


            try {

                console.log(
                    "Uploading answer..."
                );


                const response = await fetch(
                    "/upload_audio",
                    {
                        method: "POST",
                        body: formData
                    }
                );


                if (!response.ok) {

                    throw new Error(
                        "Server error: " +
                        response.status
                    );

                }


                const html =
                    await response.text();


                console.log(
                    "Analysis completed."
                );


                /*
                 Replace current page
                 with next question/report.
                */

                document.open();

                document.write(html);

                document.close();


            }

            catch (error) {

                console.error(
                    "Upload error:",
                    error
                );


                alert(
                    "Something went wrong while processing your answer."
                );


                if (status) {

                    status.innerText =
                        "Processing failed.";

                }

            }

        };


        console.log(
            "Camera and microphone ready."
        );

    }

    catch (error) {

        console.error(
            "Camera error:",
            error
        );


        alert(
            "Camera or microphone permission was denied."
        );


        if (status) {

            status.innerText =
                "Camera not started.";

        }

    }

}



function startRecording() {

    if (!mediaRecorder) {

        alert(
            "Please click Start Camera first."
        );

        return;

    }


    if (isRecording) {

        console.log(
            "Recording already in progress."
        );

        return;

    }


    audioChunks = [];

    isRecording = true;


    mediaRecorder.start();


    console.log(
        "Recording started..."
    );


    const status =
        document.getElementById("status");


    if (status) {

        status.innerText =
            "🔴 Recording... Speak your answer now.";

    }


    const cameraStatus =
        document.getElementById("cameraStatus");


    if (cameraStatus) {

        cameraStatus.innerText =
            "Recording";

    }


    const statusDot =
        document.getElementById("statusDot");


    if (statusDot) {

        statusDot.classList.add(
            "recording"
        );

    }


    setTimeout(
        function() {

            if (
                mediaRecorder &&
                mediaRecorder.state === "recording"
            ) {

                mediaRecorder.stop();

                isRecording = false;


                console.log(
                    "Recording stopped."
                );


                if (cameraStatus) {

                    cameraStatus.innerText =
                        "Processing";

                }


                if (statusDot) {

                    statusDot.classList.remove(
                        "recording"
                    );

                }

            }

        },
        8000
    );

}