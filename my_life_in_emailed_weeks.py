import yagmail
import matplotlib.pyplot as plt
from datetime import datetime
import os

# CONFIGURATION
EMAIL_SENDER = "amavirananda.2001@gmail.com"
EMAIL_PASSWORD = "hxwhpaodkolqgxbb"
EMAIL_RECEIVER = "amavirananda.2001@gmail.com"
BIRTHDATE = "2001-07-13"  # YYYY-MM-DD
LIFE_EXPECTANCY = 80
OUTPUT_IMAGE = "lifeinweeks.png"
TEMPLATE_PATH = "template.html"

def generate_life_weeks_image(birthdate_str, life_expectancy, output_path):
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
    today = datetime.today()
    lived_weeks = (today - birthdate).days // 7
    total_weeks = life_expectancy * 52  # 52 weeks per year

    fig, ax = plt.subplots(figsize=(12, 15))
    ax.set_xlim(0, 52)
    ax.set_ylim(0, life_expectancy)
    ax.set_aspect('equal')
    ax.axis('off')

    # Adjust box size
    box_width = 1  # Width of each box
    box_height = 1  # Height of each box
    margin = 0.2  # Space between each box

    # Loop through each week
    for i in range(total_weeks):
        row = i // 52
        col = i % 52

        if i < lived_weeks:
            color = "#000000"  # Lived weeks
        elif i == lived_weeks:
            color = "#FF0000"  # Current week
        else:
            color = "#CCCCCC"  # Future weeks

        # Create each rectangle with an outline and padding (margin)
        rect = plt.Rectangle(
            (col + margin, life_expectancy - row - 1 - margin),  # Offset by margin
            box_width - 2 * margin,  # Reduced width to account for margin
            box_height - 2 * margin,  # Reduced height to account for margin
            color=color,
            edgecolor="black",  # Black outline around each box
            lw=1  # Line width for the outline
        )
        ax.add_patch(rect)

    # Adjust layout and save the image
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"✅ Saved image to {output_path}")

def read_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def send_email_with_image(birthdate_str, output_image):
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
    today = datetime.today()
    lived_weeks = (today - birthdate).days // 7

    subject = "Your Life in Weeks – A Gentle Reminder"
    # body = f"Here's a visual representation of your lived life in weeks. \n\n You're living your {lived_weeks}th week - an occasion to celebrate, or a reminder to act upon?"

    generate_life_weeks_image(BIRTHDATE, LIFE_EXPECTANCY, f".github/images/{output_image}")

    # embed image in html
    template = read_template()
    full_html = template.replace("{{GRID}}", '<img src="https://raw.githubusercontent.com/yourusername/repo/main/images/life-in-weeks.png"'>)

    yag = yagmail.SMTP(EMAIL_SENDER, EMAIL_PASSWORD)
    yag.send(
        to=EMAIL_RECEIVER,
        subject=subject,
        # contents=[body, output_image]
        contents=full_html
    )
    print("✅ Email sent with image.")

if __name__ == "__main__":
    send_email_with_image(BIRTHDATE, OUTPUT_IMAGE)