# Email Productivity Agent

This is a Streamlit web application that acts as an AI-powered email productivity agent. It helps you manage your emails by categorizing them, extracting action items, and providing a chat interface to interact with your inbox.

## Features

- **Email Categorization:** Automatically categorizes emails into "Important", "To-Do", "Newsletter", and "Spam" using a large language model.
- **Action Item Extraction:** Identifies and extracts tasks and deadlines from your emails.
- **Interactive Chat:** A chat interface to ask questions about your emails, get summaries, and more.
- **Quick Actions:**
  - **Summarize:** Get a quick summary of any email.
  - **Draft Reply:** Generate a professional and friendly reply to an email.
  - **Show Tasks:** View a consolidated list of all action items from your inbox.
- **Modern UI:** A clean and modern user interface built with Streamlit.

## Getting Started

### Prerequisites

- Python 3.7+
- An API key from Google AI Studio for the Gemini API.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Manas-Gpt/Email-Productivity-Agent.git
   cd Email-Productivity-Agent
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```


3. **Set up your environment variables:**
   - Create a file named `.env` in the root of the project.
   - Add your Gemini API key to the `.env` file:
     ```
     GEMINI_API_KEY="YOUR_API_KEY_HERE"
     ```

4. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

### Creating `requirements.txt`

This project uses the following Python libraries:

- `streamlit`
- `google-generativeai`
- `python-dotenv`

You can create the `requirements.txt` file with the following content:

```
streamlit
google-generativeai
python-dotenv
```

## Usage

1. Launch the application.
2. Click "Load Mock Inbox" to load a set of sample emails.
3. Click "Process Emails" to have the AI categorize and analyze them.
4. Click on any email in the inbox to select it.
5. Use the chat interface or the quick action buttons to interact with your emails.
