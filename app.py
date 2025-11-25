import streamlit as st
import json
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict
import google.generativeai as genai



load_dotenv()

def get_gemini_model():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error("Gemini API key not found. Make sure your .env file is correct.")
        st.stop()

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash")

model = get_gemini_model()




st.set_page_config(
    page_title="Email Productivity Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
.main {background-color:#1a1a1a;color:#e0e0e0;}
.stApp {background-color:#1a1a1a;}
.email-card {
    background:#2d2d2d; padding:1.5rem; border-radius:10px;
    margin-bottom:1rem; border-left:4px solid #ff6b35;
}
.email-header {font-size:1.1rem;font-weight:bold;color:#ff6b35;margin-bottom:0.5rem;}
.email-meta {color:#888;font-size:0.9rem;margin-bottom:0.5rem;}
.category-badge {padding:0.25rem 0.75rem;border-radius:15px;font-size:0.85rem;}
.important {background:#ff4444;color:white;}
.todo {background:#ffaa00;color:white;}
.newsletter {background:#4488ff;color:white;}
.spam {background:#666;color:white;}
.chat-message {padding:1rem;border-radius:10px;margin-bottom:1rem;}
.user-message {background:#2d4a2d;margin-left:2rem;}
.assistant-message {background:#2d2d4a;margin-right:2rem;}
</style>
""", unsafe_allow_html=True)

if "emails" not in st.session_state:
    st.session_state.emails = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "selected_email" not in st.session_state:
    st.session_state.selected_email = None
if "processed" not in st.session_state:
    st.session_state.processed = False
if "drafts" not in st.session_state:
    st.session_state.drafts = []


# Mock Inbox

MOCK_INBOX = [
  {
    "id": "1",
    "sender": "manager@company.com",
    "subject": "Project deadline update",
    "body": "Hi, Please complete the analytics dashboard UI by Friday evening and share a short status update.",
    "timestamp": "2025-11-20T10:30:00Z"
  },
  {
    "id": "2",
    "sender": "newsletter@devnews.com",
    "subject": "This week in JavaScript and React",
    "body": "Hello developer, Here are the top JavaScript and React articles for this week.",
    "timestamp": "2025-11-19T08:00:00Z"
  },
  {
    "id": "3",
    "sender": "hr@company.com",
    "subject": "Mandatory security awareness training",
    "body": "Dear team, Please complete the security awareness training module on the internal LMS by 30th November.",
    "timestamp": "2025-11-18T09:15:00Z"
  },
  {
    "id": "4",
    "sender": "no-reply@randomoffers.com",
    "subject": "You won a FREE iPhone! Limited time offer!!!",
    "body": "Congratulations!!! You have been selected to win a brand new iPhone. Click now.",
    "timestamp": "2025-11-17T22:05:00Z"
  },
  {
    "id": "5",
    "sender": "product-owner@company.com",
    "subject": "User feedback summary for Sprint 14",
    "body": "Hi, We received several user feedback tickets. Please review the attached summary.",
    "timestamp": "2025-11-17T14:20:00Z"
  },
  {
    "id": "6",
    "sender": "calendar@meetings.com",
    "subject": "Meeting request: Backend API review",
    "body": "Hi, I would like to schedule a 45-minute meeting tomorrow at 3:00 PM.",
    "timestamp": "2025-11-16T11:45:00Z"
  },
  {
    "id": "7",
    "sender": "teamlead@company.com",
    "subject": "Code review for feature branch",
    "body": "Hello, Kindly create a pull request for the new notification feature.",
    "timestamp": "2025-11-15T16:00:00Z"
  },
  {
    "id": "8",
    "sender": "support@saas-tool.com",
    "subject": "Your subscription will expire in 5 days",
    "body": "Hi, Your subscription for SaaS Tool Pro will expire in 5 days.",
    "timestamp": "2025-11-14T07:30:00Z"
  },
  {
    "id": "9",
    "sender": "spam@unknown-domain.xyz",
    "subject": "Earn money FAST from home!!!",
    "body": "Make money FAST from home with zero effort. No skills required.",
    "timestamp": "2025-11-13T20:10:00Z"
  },
  {
    "id": "10",
    "sender": "colleague@company.com",
    "subject": "Help needed with test case coverage",
    "body": "Hey, Could you please help me increase the test case coverage?",
    "timestamp": "2025-11-13T13:55:00Z"
  },
  {
    "id": "11",
    "sender": "recruiter@anothercompany.com",
    "subject": "Opportunity for Software Engineer role",
    "body": "Hi, I came across your profile and wanted to check if you would be interested.",
    "timestamp": "2025-11-12T10:05:00Z"
  },
  {
    "id": "12",
    "sender": "newsletter@cloudweekly.com",
    "subject": "Cloud Weekly: Kubernetes, AWS, and more",
    "body": "Welcome to this week's edition of Cloud Weekly.",
    "timestamp": "2025-11-11T06:45:00Z"
  },
  {
    "id": "13",
    "sender": "project-manager@company.com",
    "subject": "Sprint planning agenda for Monday",
    "body": "Hi team, On Monday's sprint planning call, we will finalize the scope for Sprint 16.",
    "timestamp": "2025-11-10T09:00:00Z"
  },
  {
    "id": "14",
    "sender": "admin@office.com",
    "subject": "Office maintenance downtime",
    "body": "Dear all, There will be scheduled maintenance on the office VPN this Sunday.",
    "timestamp": "2025-11-09T18:20:00Z"
  },
  {
    "id": "15",
    "sender": "client@partnercompany.com",
    "subject": "API integration issues in staging",
    "body": "Hello, We are facing issues while integrating with your payment API.",
    "timestamp": "2025-11-08T12:10:00Z"
  },
  {
    "id": "16",
    "sender": "calendar@meetings.com",
    "subject": "Meeting request: Design review for mobile app",
    "body": "Hi, Can we schedule a 1-hour design review meeting?",
    "timestamp": "2025-11-07T11:00:00Z"
  },
  {
    "id": "17",
    "sender": "teammate@company.com",
    "subject": "Knowledge transfer session before leave",
    "body": "Hi, I will be on leave next week. Let's do a KT session.",
    "timestamp": "2025-11-06T15:40:00Z"
  },
  {
    "id": "18",
    "sender": "no-reply@ecommerce.com",
    "subject": "Your order has been shipped",
    "body": "Hi, Your recent order has been shipped.",
    "timestamp": "2025-11-05T07:55:00Z"
  },
  {
    "id": "19",
    "sender": "team@hackathon.com",
    "subject": "Reminder: Hackathon submission deadline",
    "body": "Hello participant, This is a reminder that the hackathon project submission deadline is this Saturday.",
    "timestamp": "2025-11-04T19:30:00Z"
  },
  {
    "id": "20",
    "sender": "mentor@company.com",
    "subject": "Career discussion follow-up",
    "body": "Hi, It was good speaking with you about your career goals.",
    "timestamp": "2025-11-03T10:25:00Z"
  },
  {
    "id": "21",
    "sender": "reservations@airlines.com",
    "subject": "Flight Confirmation: NYC to LON",
    "body": "Your flight (FL123) to London is confirmed for Dec 12th. Please arrive 3 hours early. See attached ticket.",
    "timestamp": "2025-11-02T08:00:00Z",
    "attachment_url": "https://drive.google.com/file/d/1snMJ3cAZuXpLgXBSb9nBKO8Fw6X7QsKj/view?usp=sharing"
  },
  {
    "id": "22",
    "sender": "bookings@railway.com",
    "subject": "Train Ticket Booking Confirmed",
    "body": "Your train to Paris departs on Nov 28th at 09:00 AM. Seat 42A. Safe travels!",
    "timestamp": "2025-11-01T14:15:00Z"
  },
  {
    "id": "23",
    "sender": "finance@vendor.com",
    "subject": "Invoice #99283 for Q3 Services",
    "body": "Please find the attached invoice for the services rendered in Q3. Payment is due in 15 days.",
    "timestamp": "2025-10-31T09:30:00Z",
    "attachment_url": "https://drive.google.com/file/d/1pGmyW9l0lpoQTB3t4NMbfGu0Kty7O_Q0/view?usp=sharing"
  },
  {
    "id": "24",
    "sender": "lottery@winner.com",
    "subject": "LAST CHANCE TO CLAIM $1,000,000",
    "body": "This is your final notice. Click here to claim your massive cash prize now!",
    "timestamp": "2025-10-30T11:00:00Z"
  },
  {
    "id": "25",
    "sender": "marketing@superstore.com",
    "subject": "Black Friday Sale Starts Now!",
    "body": "Get 50% off on all electronics this weekend only. Check out our catalog attached.",
    "timestamp": "2025-10-29T16:45:00Z",
    "attachment_url": "https://drive.google.com/file/d/1snMJ3cAZuXpLgXBSb9nBKO8Fw6X7QsKj/view?usp=sharing"
  }
]

def load_mock_inbox():
    st.session_state.emails = []
    for email in MOCK_INBOX:
        e = email.copy()
        e.setdefault("category", None)
        e.setdefault("action_items", [])
        st.session_state.emails.append(e)
    st.session_state.processed = False
    st.success(f"Loaded {len(st.session_state.emails)} emails")

def call_llm(prompt: str, context: str = "") -> str:
    try:
        final_prompt = context + "\n\n" + prompt if context else prompt
        response = model.generate_content(final_prompt)
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"

def categorize_email(email: Dict) -> str:
    prompt = f"""
You are an email classifier. Categorize this email into exactly one of:
Important, Newsletter, Spam, To-Do.

Email:
From: {email["sender"]}
Subject: {email["subject"]}
Body: {email["body"]}

Return only the category word.
"""
    result = call_llm(prompt).lower()
    if "spam" in result:
        return "Spam"
    if "newsletter" in result:
        return "Newsletter"
    if "to-do" in result or "todo" in result:
        return "To-Do"
    return "Important"

def extract_action_items(email: Dict) -> List[Dict]:
    prompt = f"""
Email:
{email["body"]}

Extract tasks from this email.
Respond ONLY in valid JSON:

{{"tasks":[{{"task":"task description","deadline":"deadline or 'Not specified'"}}]}}
If there are no tasks, respond with {{"tasks":[]}}.
"""
    response = call_llm(prompt)
    try:
        data = json.loads(response)
        return data.get("tasks", [])
    except Exception:
        return []

def process_emails():
    if not st.session_state.emails:
        st.warning("Load the inbox first.")
        return
    with st.spinner("Processing emails with Gemini..."):
        for email in st.session_state.emails:
            if email.get("category") is None:
                email["category"] = categorize_email(email)
            email["action_items"] = email.get("action_items") or extract_action_items(email)
    st.session_state.processed = True
    st.success("Emails processed successfully!")

def render_email_card(email: Dict):
    category = email.get("category")
    category_class = (category or "Important").lower()
    st.markdown(f"""
    <div class="email-card">
        <div class="email-header">{email['subject']}</div>
        <div class="email-meta">
            From: {email['sender']} | {email['timestamp']}
        </div>
        <div>
            <span class="category-badge {category_class}">{category or "Unprocessed"}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


#sidebar
with st.sidebar:
    st.title("Email Agent")
    st.markdown("---")
    if st.button("Load Mock Inbox", use_container_width=True):
        load_mock_inbox()
    if st.button("Process Emails", use_container_width=True):
        process_emails()
    st.markdown("---")
    if st.session_state.emails:
        st.metric("Total Emails", len(st.session_state.emails))
        if st.session_state.processed:
            cats = [e.get("category") for e in st.session_state.emails if e.get("category")]
            for c in sorted(set(cats)):
                st.metric(c, cats.count(c))

#layout
col1, col2 = st.columns([1.2, 1.8])

with col1:
    st.markdown("## 📬 Inbox")
    if not st.session_state.emails:
        st.info("Click 'Load Mock Inbox' to get started.")
    else:
        filter_cat = st.selectbox(
            "Filter by category",
            ["All"] + sorted(list(set([e.get("category") for e in st.session_state.emails if e.get("category")])))
        )
        emails = st.session_state.emails
        if filter_cat != "All":
            emails = [e for e in emails if e.get("category") == filter_cat]

        for email in emails:
            if st.button(f"📧 {email['subject'][:40]}...", key=f"email_{email['id']}", use_container_width=True):
                st.session_state.selected_email = email
            render_email_card(email)

#chat
with col2:
    st.markdown("## 💬 Email Agent Chat")

    if st.session_state.selected_email:
        e = st.session_state.selected_email
        with st.expander("Selected Email", expanded=True):
            st.markdown(f"**From:** {e['sender']}")
            st.markdown(f"**Subject:** {e['subject']}")
            st.markdown(f"**Date:** {e['timestamp']}")
            st.markdown(f"**Category:** {e.get('category') or 'Not processed'}")
            st.markdown(f"**Body:**\n{e['body']}")
            if e.get("attachment_url"):
                st.markdown(f"[📎 View attachment]({e['attachment_url']})")
            if e.get("action_items"):
                st.markdown("**Action Items:**")
                for item in e.get("action_items", []):
                    st.markdown(f"- {item.get('task','N/A')} (Deadline: {item.get('deadline','Not specified')})")

    st.markdown("---")


    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">👤 You: {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message assistant-message"> Agent: {msg["content"]}</div>', unsafe_allow_html=True)

    user_query = st.chat_input("Ask me anything about your emails...")
    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})

        context = "You are an email productivity assistant.\n\n"
        if st.session_state.selected_email:
            e = st.session_state.selected_email
            context += f"Current email:\nFrom: {e['sender']}\nSubject: {e['subject']}\nBody: {e['body']}\nCategory: {e.get('category')}\n\n"

        context += "All emails summary:\n"
        for e in st.session_state.emails[:5]:
            context += f"- {e['subject']} (from {e['sender']}, category: {e.get('category')})\n"

        answer = call_llm(user_query, context)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    st.markdown("### Quick Actions")
    qa1, qa2, qa3 = st.columns(3)

    with qa1:
        if st.button("Summarize", use_container_width=True) and st.session_state.selected_email:
            e = st.session_state.selected_email
            context = f"Email from {e['sender']} with subject '{e['subject']}'. Body:\n{e['body']}\n"
            summary = call_llm("Provide a brief summary of this email in 2–3 sentences.", context)
            st.session_state.chat_history.append({"role": "assistant", "content": f"Summary:\n{summary}"})
            st.rerun()

    with qa2:
        if st.button("Draft Reply", use_container_width=True) and st.session_state.selected_email:
            e = st.session_state.selected_email
            context = f"Email:\nFrom: {e['sender']}\nSubject: {e['subject']}\nBody: {e['body']}\n"
            draft = call_llm(
                "Write a polite, professional reply to this email. Keep it short and friendly.",
                context
            )
            st.session_state.drafts.append({
                "original_email": e,
                "draft": draft,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            st.session_state.chat_history.append({"role": "assistant", "content": f"Draft created:\n\n{draft}"})
            st.rerun()

    
    with qa3:
        if st.button("Show Tasks", use_container_width=True):
            tasks = []
            for e in st.session_state.emails:
                if e.get("action_items"):
                    for item in e.get("action_items", []):
                        tasks.append(f"- {item.get('task','N/A')} (from {e['subject']})")

            if tasks:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "Here are your tasks:\n\n" + "\n".join(tasks)
                })
            else:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "No tasks found in your emails."
                })
            st.rerun()


    if st.session_state.drafts:
        with st.expander("Saved Drafts"):
            for i, draft in enumerate(st.session_state.drafts):
                st.markdown(f"**Draft {i+1}** (Created: {draft['timestamp']})")
                st.markdown(f"*Reply to: {draft['original_email']['subject']}*")
                st.text_area(
                    f"Draft content {i}",
                    draft["draft"],
                    height=150,
                    key=f"draft_{i}"
                )
                st.markdown("---")
