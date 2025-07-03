import os
from datetime import datetime

import pytz
from fasthtml.common import *
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
print(os.getenv("SUPABASE_URL"))
print(os.getenv("SUPABASE_KEY"))

# Constants for input character limits and timestamp format
MAX_NAME_CHAR = 15
MAX_MESSAGE_CHAR = 50
TIMESTAMP_FMT = "%Y-%m-%d %I:%M:%S %p CET"

# Initialize Supabase client
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


def get_cet_time():
    cet_tz = pytz.timezone("CET")
    return datetime.now(cet_tz)


def add_message(name, message):
    timestamp = get_cet_time().strftime(TIMESTAMP_FMT)
    supabase.table("guestbook").insert(
        {"name": name, "message": message, "timestamp": timestamp}
    ).execute()


def get_messages():
    # Sort by 'id' in descending order to get the latest entries first
    response = supabase.table("guestbook").select("*").order("id", desc=True).execute()
    return response.data


def render_message(entry):
    avatar = entry['name'][0].upper() if entry['name'] else '👤'
    return Div(
        Div(
            Div(avatar, style="background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%); color: white; width: 56px; height: 56px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2em; font-weight: bold; margin-right: 1.5em;"),
            Div(
                Header(entry['name'], style="font-weight: bold; font-size: 1.25em; margin-bottom: 0.2em;"),
                P(entry["message"], style="margin: 0; color: inherit; font-size: 1.1em;"),
                Footer(Small(Em(f"Posted: {entry['timestamp']}")), style="color: #888; font-size: 1em; margin-top: 0.3em;"),
                style="flex: 1;"
            ),
            style="display: flex; align-items: flex-start;"
        ),
        _class="message-card card-box",
        style="padding: 1.5em; margin-bottom: 2em; width: 100%;"
    )


app, rt = fast_app(
    hdrs=(
        Link(rel="icon", type="assets/x-icon", href="/assets/favicon.png"),
        Style("""
            body { background: linear-gradient(120deg, #181c2f 0%, #232946 100%); color: #f4f4f4; font-family: 'Segoe UI', 'Roboto', Arial, sans-serif; margin: 0; padding: 0; min-height: 100vh; }
            input, textarea { background: #232946; color: #f4f4f4; border-color: #444; }
            .send-btn {
                background: linear-gradient(90deg, #43cea2 0%, #185a9d 100%);
                color: #fff;
                border: none;
                border-radius: 32px;
                padding: 1.1em 2.7em;
                font-size: 1.25em;
                font-weight: bold;
                box-shadow: 0 4px 16px rgba(24,90,157,0.13);
                cursor: pointer;
                transition: background 0.2s, transform 0.2s, box-shadow 0.2s;
                margin-top: 0.5em;
                letter-spacing: 0.02em;
                width: 100%;
                display: block;
            }
            .send-btn:hover {
                background: linear-gradient(90deg, #185a9d 0%, #43cea2 100%);
                transform: translateY(-2px) scale(1.04);
                box-shadow: 0 8px 24px rgba(24,90,157,0.18);
            }
            .form-box, .card-box, .message-card {
                background: #232946;
                color: #f4f4f4;
                border-radius: 24px;
                box-shadow: 0 4px 32px rgba(24,90,157,0.18);
                border: 1px solid #2e3650;
                transition: background 0.3s, color 0.3s, box-shadow 0.3s;
            }
            @keyframes popBtn {
                0% { transform: scale(0.8); box-shadow: 0 0 0 0 rgba(67,206,162,0.0); }
                60% { transform: scale(1.08); box-shadow: 0 8px 32px 0 rgba(67,206,162,0.18); }
                100% { transform: scale(1); box-shadow: 0 4px 24px 0 rgba(67,206,162,0.15); }
            }
        """),
    ),
)


def render_message_list():
    messages = get_messages()
    return Div(
        *[render_message(entry) for entry in messages],
        id="message-list",
        style="margin-top: 2.5em; width: 100%;"
    )


def render_content():
    logo = Div(
        "🌟 Guestbook+",
        style="font-size: 2.2em; font-weight: bold; text-align: center; margin-top: 2em; margin-bottom: 0.3em; background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"
    )
    subtitle = P(Em("Share your thoughts, feedback, or just say hi! ✨"), style="text-align: center; color: #bbb; margin-bottom: 1.5em; font-size: 1.3em; margin-top: 0.2em;")
    form = Div(
        Form(
            Div(
                Input(
                    type="text",
                    name="name",
                    placeholder="Your Name",
                    required=True,
                    maxlength=MAX_NAME_CHAR,
                    style="flex: 1 1 0; min-width: 0; padding: 1.2em; border-radius: 16px 0 0 16px; border: 1px solid #d0d7de; border-right: none; font-size: 1.1em; background: inherit; color: inherit; height: 60px; box-sizing: border-box;"
                ),
                Input(
                    type="text",
                    name="message",
                    placeholder="Your Message",
                    required=True,
                    maxlength=MAX_MESSAGE_CHAR,
                    style="flex: 2 1 0; min-width: 0; padding: 1.2em; border-radius: 0; border: 1px solid #d0d7de; border-left: none; border-right: none; font-size: 1.1em; background: inherit; color: inherit; height: 60px; box-sizing: border-box;"
                ),
                Button("Send Message", type="submit", _class="send-btn", style="flex: 1 1 0; min-width: 0; height: 60px; border-radius: 0 16px 16px 0; font-size: 1.25em; font-weight: bold; margin: 0; display: flex; align-items: center; justify-content: center; transition: box-shadow 0.2s, transform 0.2s; box-shadow: 0 4px 24px 0 rgba(67,206,162,0.15); animation: popBtn 0.7s cubic-bezier(.68,-0.55,.27,1.55);"),
                style="display: flex; width: 100%; align-items: stretch; margin-bottom: 1.5em;"
            ),
            method="post",
            hx_post="/submit-message",
            hx_target="#message-list",
            hx_swap="outerHTML",
            hx_on__after_request="this.reset()",
            style="width: 100%;"
        ),
        _class="form-box card-box",
        style="padding: 2.5em; width: 100%; max-width: 900px; margin: 0 auto; margin-top: 2.5em;"
    )

    return Div(
        logo,
        subtitle,
        form,
        Div(
            render_message_list(),
            style="width: 100%; max-width: 900px; margin: 0 auto;"
        ),
        Div(
            Hr(),
            Div(
                "Made with ❤️ by ",
                A("Ayush Kakkar", href="https://www.linkedin.com/in/ayush-kakkar-11a24a252/", target="_blank", style="color: #43cea2; font-weight: bold; text-decoration: none;"),
                " | Guestbook+ 2024",
                style="text-align: center; color: #888; font-size: 1.1em; margin-top: 2.5em;"
            ),
        ),
        style="width: 100vw; min-height: 100vh; max-width: 100vw; margin: 0; padding-bottom: 2em;"
    )


@rt("/", methods=["GET"])
def get():
    return Titled("Guestbook+ | Share Your Thoughts", render_content())
    


@rt("/submit-message", methods=["POST"])
def post(name: str, message: str):
    add_message(name, message)
    return render_message_list()


serve()
