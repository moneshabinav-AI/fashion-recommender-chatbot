import streamlit as st
import requests
import json

# Set up the Streamlit UI
st.set_page_config(page_title="Fashion Recommender", page_icon="👗", layout="centered")

st.title("👗👕 Fashion Recommendation Chatbot")
st.write("Ask for outfit suggestions, fashion tips, and styling advice!")

# Gender selection
gender = st.selectbox("Select your gender", ["Male", "Female", "Other"])

# Define the Llama 3 API Call
def query_llama3(prompt):
    url = "http://localhost:11434/api/generate"  # Ollama API endpoint
    payload = {"model": "llama3", "prompt": prompt, "stream": False}
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    if response.status_code == 200:
        return response.json().get("response", "Sorry, I couldn't generate a response.")
    else:
        return f"Error: {response.status_code}, {response.text}"

# Define the system prompt with clarification logic and no brand names
SYSTEM_PROMPT = """
You are xyx Assistant, a fashion recommendation expert developed by xyx Company. 
Your job is to suggest outfits based on user preferences. You should provide recommendations for different occasions, body types, and personal styles. 
Give detailed advice on colors, fabrics, and accessories. Do not suggest any specific brand names—focus only on the color and type of clothing or accessories.

You should only answer fashion-related questions. If a user asks anything unrelated, respond formally with: 
"I'm here to assist with fashion recommendations. Please ask me something related to fashion."

If asked "Who created you?", respond: 
"I was developed by xyx Company to provide expert fashion recommendations."

If asked "What are you?" or "Who are you?", respond: 
"I am xyx Assistant, your personal fashion recommendation expert."

For vague queries like "sportswear," "outdoor wear," "indoor wear," or similar broad terms, respond with:
"Could you please provide more details? For example, what occasion, weather, or specific activity are you dressing for?"

Format responses as:
- **Outfit Suggestion**: [Describe the full outfit with colors and cloth types, no brands]
- **Accessories**: [Recommended shoes, bags, or jewelry with colors and types, no brands]
- **Style Tip**: [One fashion styling tip]

Example:
User: "What should I wear for a formal event?"
Assistant:
- **Outfit Suggestion**: A tailored black suit with a crisp white shirt and a silk tie.
- **Accessories**: Leather Oxford shoes in black and a classic wristwatch in silver.
- **Style Tip**: Ensure your suit fits perfectly—get it tailored if needed.

Now, answer the user's question.
"""

# Create a form for Enter key submission
with st.form(key="fashion_form", clear_on_submit=True):
    user_query = st.text_input("What do you need fashion advice on?")
    submit = st.form_submit_button(label="Submit", use_container_width=True)
    # Hide the button visually with CSS, but keep it functional for Enter key
    st.markdown(
        """
        <style>
        div.stButton > button {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Process the input and get response when Enter is pressed
if submit and user_query:
    # List of vague terms to check against
    vague_terms = ["sportswear", "outdoor wear", "indoor wear", "casual", "formal"]
    # List of thank you phrases
    thank_you_phrases = ["thank you", "thanks"]
    # List of unethical/illegal activity terms
    unethical_terms = ["heist", "robbery", "steal", "crime", "burglary"]
    
    user_query_lower = user_query.lower().strip()
    
    # Check if the user is saying thank you
    if any(phrase in user_query_lower for phrase in thank_you_phrases):
        response = "You’re welcome! I’m happy to help you look your best. Anything else I can assist with?"
    # Check if the query involves unethical/illegal activities
    elif any(term in user_query_lower for term in unethical_terms):
        response = "I’m sorry, but I can’t assist with recommendations for illegal or unethical activities. How about something stylish for a different occasion?"
    # Check if the query is vague
    elif any(term in user_query_lower for term in vague_terms) and len(user_query.split()) <= 2:
        response = "Could you please provide more details? For example, what occasion, weather, or specific activity are you dressing for?"
    # Otherwise, process as a fashion query
    else:
        full_prompt = SYSTEM_PROMPT + f"\nUser (Gender: {gender}): " + user_query + "\nAssistant:"
        response = query_llama3(full_prompt)
    
    st.markdown(response)
