# chatbot.py
import os
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain.chains.conversation.memory import ConversationBufferMemory

class ChatHandler:
    def __init__(self, api_key, model, initial_roadmap):
        print("[INFO] Initializing Chat Handler...")
        self.groq_chat = ChatGroq(api_key=api_key, model_name=model)
        self.memory = ConversationBufferMemory(return_messages=True)
        
        system_template = (
            'You are a friendly and knowledgeable chatbot that provides personalized roadmaps '
            'and answers follow-up questions based on the roadmap. Always be encouraging and supportive. '
            'Maintain context from previous messages and refer back to the initial roadmap when relevant. '
            'If asked to summarize, focus on summarizing the roadmap content.'
        )
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template("{chat_history}\nHuman: {human_input}\nAI: ")
        ])
        
        self.conversation = LLMChain(llm=self.groq_chat, prompt=prompt)

        # Store initial roadmap in memory
        self.memory.chat_memory.add_message(AIMessage(content=initial_roadmap))
        print("[INFO] Chat Handler initialized with initial roadmap.")

    def process_input(self, user_input):
        print("[DEBUG] Processing user input...")
        
        # Get chat history
        chat_history = self.get_chat_history_str()
        
        # Generate response
        response = self.conversation.predict(human_input=user_input, chat_history=chat_history)
        print("[DEBUG] Generated response.")

        # Store messages in memory
        self.memory.chat_memory.add_message(HumanMessage(content=user_input))
        self.memory.chat_memory.add_message(AIMessage(content=response))
        
        return response

    def get_chat_history(self):
        return self.memory.chat_memory.messages

    def get_chat_history_str(self):
        messages = self.get_chat_history()
        return "\n".join([f"{msg.__class__.__name__}: {msg.content}" for msg in messages])
