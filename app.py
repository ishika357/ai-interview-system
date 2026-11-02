from flask import Flask, render_template, request, session
import subprocess
import os
import imageio_ffmpeg

app = Flask(__name__)

app.secret_key = "ai_interview_project_secret_key"


questions = [
    "Explain what Python is.",
    "What is machine learning?",
    "Explain the concept of data structures."
]


@app.route("/")
def home():

    # Always start a new interview
    session["question_index"] = 0

    return render_template(
        "interview.html",
        question=questions[0],
        question_number=1,
        total_questions=len(questions)
    )


@app.route("/upload_audio", methods=["POST"])
def upload_audio():

    try:

        # --------------------------------
        # GET CURRENT QUESTION
        # --------------------------------

        question_index = session.get(
            "question_index",
            0
        )

        if question_index >= len(questions):
            question_index = 0

        current_question = questions[question_index]

        print()
        print("================================")
        print("QUESTION:", current_question)
        print("================================")


        # --------------------------------
        # RECEIVE AUDIO
        # --------------------------------

        if "audio" not in request.files:

            return """
            <h1>Something went wrong</h1>
            <p>No audio file received.</p>
            """, 400


        audio = request.files["audio"]

        audio.save("answer.webm")

        print("Audio received.")


        # --------------------------------
        # CONVERT WEBM → WAV
        # --------------------------------

        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

        subprocess.run(
            [
                ffmpeg_path,
                "-y",
                "-i",
                "answer.webm",
                "-ar",
                "16000",
                "-ac",
                "1",
                "answer.wav"
            ],
            check=True
        )

        print("Audio converted.")


        # --------------------------------
        # SPEECH TO TEXT
        # --------------------------------

        subprocess.run(
            [
                "python",
                "speech_to_text.py"
            ],
            check=True
        )

        print("Speech converted to text.")


        # --------------------------------
        # SAVE CURRENT QUESTION
        # --------------------------------

        with open(
            "current_question.txt",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(current_question)


        # --------------------------------
        # ANALYZE ANSWER
        # --------------------------------

        subprocess.run(
            [
                "python",
                "answer_analyzer.py"
            ],
            check=True
        )

        print("Answer analyzed.")


        # --------------------------------
        # READ SCORE
        # --------------------------------

        with open(
            "score.txt",
            "r",
            encoding="utf-8"
        ) as f:

            score = f.read()


        # --------------------------------
        # READ FEEDBACK
        # --------------------------------

        with open(
            "feedback.txt",
            "r",
            encoding="utf-8"
        ) as f:

            feedback = f.read()


        # --------------------------------
        # READ RESULT
        # --------------------------------

        with open(
            "result.txt",
            "r",
            encoding="utf-8"
        ) as f:

            result_status = f.read()


        # --------------------------------
        # READ CANDIDATE ANSWER
        # --------------------------------

        if os.path.exists("candidate_answer.txt"):

            with open(
                "candidate_answer.txt",
                "r",
                encoding="utf-8"
            ) as f:

                candidate_answer = f.read()

        else:

            candidate_answer = "No answer detected."


        # --------------------------------
        # MOVE TO NEXT QUESTION
        # --------------------------------

        next_index = question_index + 1


        # --------------------------------
        # MORE QUESTIONS AVAILABLE
        # --------------------------------

        if next_index < len(questions):

            session["question_index"] = next_index

            return render_template(
                "interview.html",
                question=questions[next_index],
                question_number=next_index + 1,
                total_questions=len(questions),
                previous_answer=candidate_answer,
                previous_score=score,
                previous_feedback=feedback
            )


        # --------------------------------
        # INTERVIEW FINISHED
        # --------------------------------

        session.pop("question_index", None)

        return render_template(
            "result.html",
            score=score,
            emotion="Unknown",
            feedback=feedback,
            result_status=result_status,
            candidate_answer=candidate_answer
        )


    except Exception as e:

        print()
        print("================================")
        print("ERROR")
        print("================================")
        print(e)

        return f"""
        <h1>Something went wrong</h1>

        <p>{e}</p>

        <br>

        <a href="/">
            Start Interview Again
        </a>
        """, 500


if __name__ == "__main__":

    app.run(
        debug=True,
        use_reloader=False
    )