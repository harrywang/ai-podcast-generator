import openai
import os
from dotenv import load_dotenv
import anthropic
import datetime

# Load environment variables
load_dotenv()  # take environment variables from .env

# Model settings
ant_model = "claude-3-5-haiku-latest"  # Best quality Anthropic model
oai_model = "gpt-4o-mini"     # Best quality OpenAI model

# Conversation settings
language = "english"  # conversation language
num_of_turns = 5  # number of turns in the conversation

# Cost tracking
# GPT-4o-mini: $0.150 / 1M input tokens, $0.600 / 1M output tokens
# Claude 3.5 Haiku: $0.80 / MTok Input, $4 / MTok Output
oai_cost = 0
ant_cost = 0

def setup_podcast_roles():
    """Setup the system prompts for the conversation"""
    ant_system_prompt = f"you are a female painter and is going to chat with another person in {language} don't include any tone or scene description in the chat, and don't say your gender and now start chatting"
    oai_system_prompt = f"you are a male musician and is going to chat with another person in {language}, don't say your gender and now start chatting"
    
    return ant_system_prompt, oai_system_prompt

def get_anthropic_response(messages):
    """Get response from Anthropic's Claude model"""
    client = anthropic.Anthropic()
    
    # Convert messages to the format expected by Anthropic
    ant_messages = []
    for msg in messages:
        if msg["role"] == "user":
            ant_messages.append({"role": "user", "content": msg["content"]})
        elif msg["role"] == "assistant":
            ant_messages.append({"role": "assistant", "content": msg["content"]})
    
    response = client.messages.create(
        model=ant_model,
        max_tokens=1024,
        messages=ant_messages
    )
    
    global ant_cost
    ant_cost += response.usage.input_tokens * 0.80/1000000 + response.usage.output_tokens * 4/1000000
    
    return response.content[0].text

def get_openai_response(messages):
    """Get response from OpenAI's GPT model"""
    oai_client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    
    oai_response = oai_client.chat.completions.create(
        model=oai_model,
        messages=messages
    )
    
    global oai_cost
    oai_cost += oai_response.usage.prompt_tokens * 0.150/1000000 + oai_response.usage.completion_tokens * 0.600/1000000
    
    return oai_response.choices[0].message.content

def save_conversation(conversation, filename):
    """Save the conversation to a text file"""
    with open(filename, 'w', encoding='utf-8') as f:
        for i, exchange in enumerate(conversation):
            if i % 2 == 0:
                f.write("Painter: " + exchange + "\n\n")
            else:
                f.write("Musician: " + exchange + "\n\n")

def simulate_conversation():
    """Simulate a conversation between Claude and GPT"""
    # Setup the roles
    ant_system_prompt, oai_system_prompt = setup_podcast_roles()
    
    # Initialize message histories
    ant_messages = [{"role": "user", "content": ant_system_prompt}]
    oai_messages = [{"role": "system", "content": oai_system_prompt}]
    
    # Store conversation for saving to file
    conversation = []
    
    # Get first message from Claude (Painter)
    ant_reply = get_anthropic_response(ant_messages)
    print("Painter:", ant_reply)
    ant_messages.append({"role": "assistant", "content": ant_reply})
    conversation.append(ant_reply)
    
    # Start conversation loop
    for _ in range(num_of_turns):
        # Musician's turn (GPT)
        oai_messages.append({"role": "user", "content": ant_reply})
        oai_reply = get_openai_response(oai_messages)
        print("\nMusician:", oai_reply)
        oai_messages.append({"role": "assistant", "content": oai_reply})
        conversation.append(oai_reply)
        
        # Painter's turn (Claude)
        ant_messages.append({"role": "user", "content": oai_reply})
        ant_reply = get_anthropic_response(ant_messages)
        print("\nPainter:", ant_reply)
        ant_messages.append({"role": "assistant", "content": ant_reply})
        conversation.append(ant_reply)
    
    # Print final costs
    print(f"\nFinal costs:")
    print(f"Claude cost: ${ant_cost:.4f}")
    print(f"GPT cost: ${oai_cost:.4f}")
    print(f"Total cost: ${(ant_cost + oai_cost):.4f}")
    
    # Save conversation to file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversation_{timestamp}.txt"
    save_conversation(conversation, filename)
    print(f"\nConversation saved to {filename}")

if __name__ == "__main__":
    simulate_conversation()
