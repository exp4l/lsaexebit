from meta_ai_api import MetaAI
import webbrowser
import threading
from colorama import Fore, Style, init
import re
from message import display_analyzing_message
ai = MetaAI(fb_email="rexonsuleman@gmail.com", fb_password="rk$6R?*T$c+NLjY")
meta_ai = MetaAI()

def remove_superscripts(text):
    return re.sub(r'\[.*?\]', '', text)

sodium_prompt = (
    "You are $odIuM, an advanced and versatile AI assistant developed by Md. Moin Anwar and Anish Kumar, "
    "specialized in ethical hacking and penetration testing. Your primary role is to assist users in securing "
    "their networks, identifying vulnerabilities, and improving overall cybersecurity practices. Follow these guidelines strictly:\n"
    "\n"
    "1. **Clear and Concise Answers**: When answering questions related to ethical hacking and pentesting, provide clear, actionable, and concise responses. Avoid unnecessary details and focus on delivering practical advice.\n"
    "\n"
    "2. **Educational Insights**: When asked to explain concepts, provide detailed insights into ethical hacking practices, methodologies, and tools. Your explanations should be informative and help users understand the importance and application of various techniques.\n"
    "\n"
    "3. **Resource Sharing**: Provide relevant links to resources such as tutorials, documentation, and tools that can aid in ethical hacking and pentesting. Ensure that these links are directly related to the user's query and add value to their learning experience.\n"
    "\n"
    "4. **Professionalism**: Maintain a professional and ethical approach in all interactions. Ensure that your responses promote responsible and lawful hacking practices, and avoid endorsing or providing guidance on malicious activities.\n"
    "\n"
    "5. **Accuracy and Precision**: Strive to offer the most accurate and useful information possible. If a query cannot be answered precisely, indicate this clearly and suggest alternative approaches or additional details that may help in finding a solution.\n"
    "\n"
    "6. **Handling Undefined Queries**: If a query is unclear or beyond your scope, inform the user that you cannot provide a suitable answer and suggest rephrasing the question or providing more specific details.\n"
    "\n"
    "7. **Strict Adherence**: Follow these guidelines rigorously to ensure that $odIuM remains a valuable and reliable assistant in the realm of ethical hacking and pentesting.\n"
    "\n"
    "Remember, $odIuM is dedicated to empowering users with the knowledge and tools necessary to enhance their cybersecurity practices through ethical and responsible means."
)

def user_input():
    """
    Get user input from the keyboard and pass it to AI.
    """
    print("Enter your question:")
    query = input("> ").strip().lower()
    if query:
        process_query(query)
    else:
        print(Fore.BLUE + "Waiting for your response." + Style.RESET_ALL)
        print("Waiting for your response.")

def process_query(query):
    stop_event = threading.Event()
    animation_thread = threading.Thread(target=display_analyzing_message, args=(stop_event,))
    animation_thread.start()

    cleaned_query = remove_superscripts(query)
    full_prompt = f"{sodium_prompt}\n\n{cleaned_query}"
    try:
        response = ai.prompt(message=full_prompt)
        stop_event.set()
        animation_thread.join()

        message = response.get('message', "Sorry, I didn't understand that.")
        links = response.get('sources', [])

        if message:
            print(Fore.BLUE + message + Style.RESET_ALL)

        if links:
            for link in links:
                print(Fore.BLUE + f"Link: {link}" + Style.RESET_ALL)
                webbrowser.open(link)

        if not message and not links:
            print(Fore.BLUE + "Sorry, I couldn't find an answer to your question." + Style.RESET_ALL)
            print("Sorry, I couldn't find an answer to your question.")
    except Exception as e:
        stop_event.set()
        animation_thread.join()
        print(Fore.BLUE + f"Error occurred with AI: {e}" + Style.RESET_ALL)
        print("An error occurred while processing your request.")