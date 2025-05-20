import yagmail
import matplotlib.pyplot as plt
from datetime import datetime
import os
import requests

# CONFIGURATION
EMAIL_SENDER = "amavirananda.2001@gmail.com"
EMAIL_PASSWORD = "hxwhpaodkolqgxbb"
EMAIL_RECEIVER = "amavirananda.2001@gmail.com"
BIRTHDATE = "2001-07-13"  # YYYY-MM-DD
LIFE_EXPECTANCY = 80
OUTPUT_IMAGE = "lifeinweeks.png"
TEMPLATE_PATH = "template.html"
client_id = "35eeec5e6625fe6" #imgur upload

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

def upload_to_imgur(image_path, client_id):
    headers = {"Authorization": f"Client-ID {client_id}"}
    with open(image_path, "rb") as img:
        data = {"image": img.read()}
        response = requests.post("https://api.imgur.com/3/upload", headers=headers, files=data)
    if response.status_code == 200:
        return response.json()["data"]["link"]
    else:
        raise Exception(f"Upload failed: {response.status_code}, {response.text}")

def send_email_with_image(birthdate_str, output_image):
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
    today = datetime.today()
    lived_weeks = (today - birthdate).days // 7

    subject = "Your Life in Weeks – A Gentle Reminder"
    # body = f"Here's a visual representation of your lived life in weeks. \n\n You're living your {lived_weeks}th week - an occasion to celebrate, or a reminder to act upon?"

    # generate image and POST to imgur
    generate_life_weeks_image(BIRTHDATE, LIFE_EXPECTANCY, output_image)
    img_url = upload_to_imgur(output_image, client_id)
    print(f"uploaded image to {img_url}")

    # embed image in html
    template = read_template()
    html_string = f"""
                    <div style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: auto; text-align: center;">
                        <p style="font-size: 18px; color: #333;">
                            Here's a visual representation of your life in weeks.<br>
                            You’re living your <strong>{lived_weeks}</strong><sup>th</sup> week —
                            <em>an occasion to celebrate, or a reminder to act upon?</em>
                        </p>
                        <img src="{img_url}" alt="Life in Weeks Chart" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); margin-top: 20px;">
                    </div>
                    """
    full_html = template.replace("{{GRID}}", html_string)

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