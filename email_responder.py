from crewai.flow.flow import Flow, start, listen
import google.generativeai as genai
from gmail_responder.gmail_service import get_latest_email, send_email
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")

class EmailAutoResponderFlow(Flow):
    def __init__(self):
        super().__init__()
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.sender_email = None 
        self.email_content = None

    @start()
    def classify_email(self):
        """Fetch the sender's email and classify the email content."""
        self.sender_email, email_text = get_latest_email()  
        if not email_text:
            return "No Email Found"
        
        # Store the email content for later use
        self.email_content = email_text

        response = self.model.generate_content(
            f"Classify this email into its category. Just identify the name only:\n'{email_text}'"
        )
        category = response.text.strip()
        print("-----------------------------------------------------------------")
        print(f"📌 Email classified as: {category}")
        return category

    @listen(classify_email)
    def generate_response(self, category):
        """Generate a personalized response based on the email content and category."""
        if category == "No Email Found":
            return "No response needed."

        if not self.email_content:
            return "Error: No email content available."

        prompt = f"""
        You are an AI customer support agent. You need to respond to a '{category}' email.
        
        Here is the original email:
        '{self.email_content}'
        
        Instructions:
        1. Extract specific details from the email (customer name, order numbers, dates, etc.)
        2. Use these specific details in your response
        3. Provide a complete, personalized response addressing their specific concerns
        4. Maintain a polite and professional tone
        5. Do not ask for additional information that was already provided in the email
        6. Generate a final, appropriate reply that includes all relevant extracted information
        
        Your response should look like a complete email with proper greeting and sign-off.
        """

        response = self.model.generate_content(prompt)
        email_reply = response.text.strip()
        return email_reply


    @listen(generate_response)
    def send_auto_reply(self, email_reply):
        """Sends the generated email response to the original sender."""
        if self.sender_email:
            # Extract a subject line based on the email category
            subject_prompt = f"Generate a brief, relevant subject line for this email reply: '{email_reply}'"
            subject_response = self.model.generate_content(subject_prompt)
            subject = f"Re: {subject_response.text.strip()}"
            
            send_email(self.sender_email, subject, email_reply) 
            print(f"\n📩 **Final Email Sent to {self.sender_email}**")
        return email_reply

def kickoff():
    flow = EmailAutoResponderFlow()
    flow.kickoff()

def plot():
    flow = EmailAutoResponderFlow()
    flow.plot()
