# 🤖 AI-Powered Email Auto Responder

Automates Gmail responses using CrewAI, Google Gemini 1.5 Pro, and Gmail API.  
Fetches unread emails, classifies them, generates intelligent replies, and sends them back — fully hands-free.

---

## 🚀 Features
- Fetches unread Gmail messages via Gmail API
- Classifies emails into Inquiry, Complaint, Support, etc.
- Generates personalized responses (includes name, order number, etc.)
- Automatically replies to each sender using Gmail
- Filters out spam and marketing messages
- Supports batch processing of multiple emails
- Logs sent replies to a local file
- Runs continuously with a refresh loop

---

## 🛠️ Tech Stack
- Python 3.12
- Google Gemini 1.5 Pro (via Generative AI SDK)
- Gmail API (OAuth2)
- CrewAI (workflow/task management)
- LiteLLM (for language model abstraction)

---

## 🔧 Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/UmaiRyden/Email-Auto-Responder
   cd email-auto-responder
