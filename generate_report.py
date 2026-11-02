from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

with open("emotion.txt") as f:
    emotion = f.read()

with open("score.txt") as f:
    score = f.read()

with open("feedback.txt") as f:
    feedback = f.read()

with open("result.txt") as f:
    result_status = f.read()

c = canvas.Canvas("interview_report.pdf", pagesize=letter)

c.drawString(100,700,"AI Interview Report")
c.drawString(100,650,"Emotion: "+emotion)
c.drawString(100,620,"Score: "+score)
c.drawString(100,590,"Feedback: "+feedback)
c.drawString(100,560,"Result: "+result_status)

c.save()

print("PDF Report Generated")