# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from chatbot import ChatHandler
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

# Directly embed the GROQ_API_KEY securely on the server
GROQ_API_KEY = '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'

# In-memory storage for sessions
sessions = {}

# Function to generate a personalized roadmap using Groq API
def generate_roadmap(user_info, api_key, model):
    print("[INFO] Generating personalized roadmap...")
    groq_chat = ChatGroq(api_key=api_key, model_name=model)
    
    system_prompt = (
        "You are an expert career advisor. Create a detailed and personalized roadmap "
        "for the user based on their information and career goals."
    )
    
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt),
        HumanMessagePromptTemplate.from_template("{user_info}")
    ])

    chain = LLMChain(llm=groq_chat, prompt=prompt)

    user_info_str = (
        f"{user_info['name']} is a {user_info['age']}-year-old student in {user_info['location']}, "
        f"studying in {user_info['additional_info']['standard']}. "
        f"They aspire to become a {user_info['career_goal']}. "
        f"Interests/Hobbies: {user_info['additional_info']['interests_and_hobbies']}. "
        f"Strengths: {user_info['additional_info']['academic_strengths']}. "
        f"Areas for improvement: {user_info['additional_info']['weaknesses']}. "
        f"Learning style: {user_info['additional_info']['learning_style']}. "
        f"Additional details: {user_info['additional_info']['other_details']}. "
        "Create a comprehensive roadmap including academic steps and extracurricular activities."
    )

    roadmap = chain.predict(user_info=user_info_str)
    print("[INFO] Roadmap generated successfully.")
    return roadmap

@app.route('/api/generate-roadmap', methods=['POST'])
def generate_roadmap_endpoint():
    try:
        data = request.json
        user_info = data.get('user_info')

        if not user_info:
            return jsonify({'error': 'User information is required.'}), 400

        roadmap = generate_roadmap(user_info, GROQ_API_KEY, 'mixtral-8x7b-32768')

        # Create a unique session ID
        session_id = str(uuid.uuid4())

        # Initialize ChatHandler for the session
        chat_handler = ChatHandler(GROQ_API_KEY, 'mixtral-8x7b-32768', roadmap)

        # Store the session
        sessions[session_id] = chat_handler

        return jsonify({'roadmap': roadmap, 'session_id': session_id}), 200

    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({'error': 'An error occurred while generating the roadmap.'}), 500

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    try:
        data = request.json
        session_id = data.get('session_id')
        user_message = data.get('message')

        if not session_id or not user_message:
            return jsonify({'error': 'Session ID and message are required.'}), 400

        chat_handler = sessions.get(session_id)

        if not chat_handler:
            return jsonify({'error': 'Invalid session ID.'}), 400

        response = chat_handler.process_input(user_message)

        return jsonify({'response': response}), 200

    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({'error': 'An error occurred while processing the message.'}), 500

if __name__ == "__main__":
    app.run(debug=True)
