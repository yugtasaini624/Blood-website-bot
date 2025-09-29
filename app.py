from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Hardcoded FAQ Bot

previous_context = None

def answer_question(question):
    global previous_context
    question = question.lower()

    # Greetings
    if "hello" in question or "hi" in question or "hey" in question:
        return "Hii!! How can I help you today? 😊 Do you want to donate blood or request blood?"

    # Blood donation
    elif "donate" in question or "give blood" in question or "blood donation" in question:
            previous_context = "donate_followup"
            return ("You can donate blood by registering on our website. "
                    "Make sure you meet the eligibility criteria: age 18–65, healthy, not under medication, etc. "
                    "Do you want me to guide you donation will happen?")

    # Request blood
    elif "get blood" in question or "request blood" in question or "need blood" in question:
            previous_context = "request_followup"
            return ("To request blood, fill out the 'Request Blood' form on our website. "
                    "Our team will match you with a donor as soon as possible. "
                    "Do you want me to show you what will it happen?")

    # Eligibility
    elif "who can donate" in question or "eligibility" in question or "criteria" in question:
            previous_context = "eligibility_followup"
            return ("Anyone aged 18–65 in good health can donate blood. "
                    "Do you want more details about the health checks?")
    
    # Safety
    elif "safe" in question or "is it safe" in question or "donation safe" in question:
            previous_context = "safety_followup"
            return ("Yes, donations are safe. Sterile equipment is used, and the process is supervised by professionals. "
                    "All equipment is sterile, and trained staff monitor the process. "
                    "Do you want me to explain the donation procedure step by step?")

    # Frequency
    elif "how often" in question or "frequency" in question:
        previous_context = "frequency_followup"
        return "You can donate whole blood every 3 months, and platelets every 2 weeks. Would you like me to explain why?"

    # Benefits
    elif "benefits" in question or "advantages" in question:
        previous_context = "benefits_followup"
        return ("Donating blood helps save lives and can also benefit your health, like improving heart health. "
                "Do you want me to list all the health benefits?")

    # Contact / Support
    elif "contact" in question or "help" in question:
        previous_context = "contact_followup"
        return ("You can contact our support team via email or phone listed on our website. "
                "Do you want me to give you the contact details?")
    elif "okay" in question or "ok" in question or "fine" in question:
         return ("I am glad to be helpful to you 😊!! Do you want to ask something else?")
    
    # Yes/No follow-ups
    elif "yes" in question or "sure" in question:
        # Donation flow
        if previous_context == "donate_followup":
            previous_context = None  # reset after flow ends
            return ("On donation day, you'll go through registration, a health check, and then the donation process. "
                    "It usually takes about 30–45 minutes.")
        
        # Request blood flow
        elif previous_context == "request_followup":
            previous_context = None
            return "Once you submit the 'Request Blood' form, our team will contact you with donor details.""Make sure to keep your contact info accurate."

        # Eligibility flow

        elif previous_context == "eligibility_followup":
            previous_context = "eligibility_step2"
            return ("You must also meet hemoglobin and weight requirements, and be in good health. "
                    "Would you like me to give you a checklist to see if you qualify?")
        
        elif previous_context == "eligibility_step2":
            previous_context = None
            return ("Checklist:\n- Age 18–65\n- Weight ≥ 50kg\n- Hemoglobin normal\n- No recent illness or medication\n"
                   )

        # Safety flow
        elif previous_context == "safety_followup":
            previous_context = None
            return ("Step-by-step donation process:\n1. Registration\n2. Health check\n3. Donation\n4. Refreshments\n"
                    "It is safe and quick.")

        # Frequency flow
        elif previous_context == "frequency_followup":
            previous_context = None
            return "Blood needs to regenerate, so the minimum gaps are important for donor safety."

        # Benefits flow
        elif previous_context == "benefits_followup":
            previous_context = None
            return ("Health benefits include:\n- Heart health improvement\n- Reduces harmful iron stores\n- Burns calories\n"
                    "- Psychological satisfaction\n")

        # Contact flow
        elif previous_context == "contact_followup":
            previous_context = None
            return "Support contacts:\nEmail: support@bloodbank.com\nPhone: +1234567890"

        # Unknown follow-up
        else:
            previous_context = None
            return "Could you please clarify your question?"

    # Default response
    else:
        return "Sorry, I didn't understand. Please check our FAQ page or contact support."

# Serve HTML page
@app.route("/")
def home():
    with open("index.html", "r") as f:
        return render_template_string(f.read())

# Endpoint for chat
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    answer = answer_question(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)