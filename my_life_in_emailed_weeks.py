import yagmail
from datetime import datetime

# === CONFIG ===
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # Use Gmail App Password
EMAIL_RECEIVER = "your_email@gmail.com"
BIRTHDATE = "1995-01-01"  # YYYY-MM-DD
LIFE_EXPECTANCY = 80
TEMPLATE_PATH = "template.html"
OUTPUT_HTML = "life_in_weeks_output.html"

def generate_life_in_weeks_html(birthdate: str, life_expectancy=80):
    weeks_per_year = 52
    total_weeks = life_expectancy * weeks_per_year

    birth = datetime.strptime(birthdate, "%Y-%m-%d")
    today = datetime.today()
    lived_weeks = (today - birth).days // 7

    html = '<table cellspacing="0" cellpadding="0" style="line-height: 1px; margin: 10px 0;">'

    for row in range(life_expectancy):
        html += '<tr>'
        for col in range(weeks_per_year):
            i = row * weeks_per_year + col
            if i < lived_weeks:
                color = "#000000"
            elif i == lived_weeks:
                color = "#FF0000"
            else:
                color = "#CCCCCC"

            html += (
                f'<td style="width:8px;height:8px;'
                f'background-color:{color};'
                f'padding:1px;'
                f'margin:1px;"></td>'
            )
        html += '</tr>'

    html += '</table>'
    return html

def read_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def send_email():
    grid_html = generate_life_in_weeks_html(BIRTHDATE, LIFE_EXPECTANCY)
    template = read_template()
    full_html = template.replace("{{GRID}}", grid_html)

    # Save the HTML for reference
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(full_html)

    subject = "Your Life in Weeks – Weekly Update"
    yag = yagmail.SMTP(EMAIL_SENDER, EMAIL_PASSWORD)
    yag.send(
        to=EMAIL_RECEIVER,
        subject=subject,
        contents=full_html
    )
    print("✅ Email sent. HTML saved as", OUTPUT_HTML)

if __name__ == "__main__":
    send_email()
