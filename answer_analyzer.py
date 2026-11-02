import re


# -----------------------------------------
# READ CURRENT QUESTION
# -----------------------------------------

try:

    with open(
        "current_question.txt",
        "r",
        encoding="utf-8"
    ) as f:

        question = f.read().strip()

except FileNotFoundError:

    question = "Explain what Python is."


# -----------------------------------------
# READ CANDIDATE ANSWER
# -----------------------------------------

try:

    with open(
        "candidate_answer.txt",
        "r",
        encoding="utf-8"
    ) as f:

        answer = f.read().strip()

except FileNotFoundError:

    answer = ""


print("\n==============================")
print("AI INTERVIEW ANALYSIS")
print("==============================")

print("\nQuestion:")
print(question)

print("\nCandidate Answer:")
print(answer)


# -----------------------------------------
# QUESTION-SPECIFIC KEYWORDS
# -----------------------------------------

question_data = {

    "python": [
        "programming",
        "language",
        "high level",
        "interpreted",
        "automation",
        "web development",
        "data analysis",
        "machine learning"
    ],

    "machine learning": [
        "data",
        "model",
        "training",
        "prediction",
        "algorithm",
        "machine",
        "learning",
        "dataset"
    ],

    "data structures": [
        "array",
        "list",
        "stack",
        "queue",
        "tree",
        "graph",
        "data",
        "structure"
    ]
}


# -----------------------------------------
# FIND KEYWORDS FOR CURRENT QUESTION
# -----------------------------------------

question_lower = question.lower()

selected_keywords = []


if "python" in question_lower:

    selected_keywords = question_data["python"]


elif "machine learning" in question_lower:

    selected_keywords = question_data["machine learning"]


elif "data structures" in question_lower:

    selected_keywords = question_data["data structures"]


else:

    selected_keywords = []


# -----------------------------------------
# NORMALIZE ANSWER
# -----------------------------------------

answer_lower = answer.lower()


# -----------------------------------------
# FIND MATCHED KEYWORDS
# -----------------------------------------

matched_keywords = []


for keyword in selected_keywords:

    if keyword in answer_lower:

        matched_keywords.append(keyword)


# -----------------------------------------
# TECHNICAL SCORE
# -----------------------------------------

if len(selected_keywords) > 0:

    technical_score = (
        len(matched_keywords)
        / len(selected_keywords)
    ) * 100

else:

    technical_score = 0


technical_score = round(
    technical_score,
    2
)


# -----------------------------------------
# WORD COUNT
# -----------------------------------------

word_count = len(
    answer.split()
)


# -----------------------------------------
# ANSWER QUALITY SCORE
# -----------------------------------------

if word_count >= 40:

    quality_score = 100

elif word_count >= 30:

    quality_score = 90

elif word_count >= 20:

    quality_score = 75

elif word_count >= 10:

    quality_score = 60

elif word_count >= 5:

    quality_score = 40

else:

    quality_score = 20


# -----------------------------------------
# RELEVANCE SCORE
# -----------------------------------------

if technical_score >= 50:

    relevance_score = 90

elif technical_score >= 30:

    relevance_score = 70

elif technical_score >= 10:

    relevance_score = 50

else:

    relevance_score = 20


# -----------------------------------------
# OVERALL SCORE
# -----------------------------------------

overall_score = (

    technical_score * 0.50

    + quality_score * 0.20

    + relevance_score * 0.30

)


overall_score = round(
    overall_score,
    2
)


# -----------------------------------------
# GENERATE FEEDBACK
# -----------------------------------------

feedback = []


if technical_score >= 70:

    feedback.append(
        "Strong technical understanding."
    )

elif technical_score >= 40:

    feedback.append(
        "You mentioned some relevant technical concepts."
    )

else:

    feedback.append(
        "Include more technical concepts related to the question."
    )


if word_count < 10:

    feedback.append(
        "Your answer is too short. Explain the concept in more detail."
    )

elif word_count < 20:

    feedback.append(
        "Try to provide a more detailed explanation and an example."
    )

else:

    feedback.append(
        "Your answer has a reasonable amount of detail."
    )


if relevance_score >= 70:

    feedback.append(
        "Your answer is relevant to the question."
    )

else:

    feedback.append(
        "Try to stay more focused on the question."
    )


final_feedback = " ".join(feedback)


# -----------------------------------------
# FINAL RESULT
# -----------------------------------------

if overall_score >= 70:

    result_status = "PASS"

elif overall_score >= 50:

    result_status = "AVERAGE"

else:

    result_status = "FAIL"


# -----------------------------------------
# SAVE RESULTS
# -----------------------------------------

with open(
    "score.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(str(overall_score))


with open(
    "feedback.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(final_feedback)


with open(
    "result.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(result_status)


# -----------------------------------------
# DISPLAY ANALYSIS
# -----------------------------------------

print("\n------------------------------")

print(
    "Matched Keywords:",
    matched_keywords
)

print(
    "Technical Score:",
    technical_score
)

print(
    "Answer Quality:",
    quality_score
)

print(
    "Relevance Score:",
    relevance_score
)

print(
    "Overall Score:",
    overall_score
)

print(
    "Result:",
    result_status
)

print(
    "Feedback:",
    final_feedback
)

print("------------------------------")