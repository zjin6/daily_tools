import openai

# Initialize the OpenAI API client
openai.api_key = "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"

# Start a conversation loop
while True:
    # Get the prompt from the user
    prompt = input("You: ")

    # Use the completions endpoint to generate a response
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Get the first completion from the response
    completion = response["choices"][0]["text"]

    # Print the response
    print("ChatGPT: " + completion)



# This code sets up a while loop that continuously asks for a prompt from the user, 
# generates a response from GPT-3, and prints the response. 
# Note that you will need to replace "YOUR_API_KEY" with your actual 
# OpenAI API key in order to run this code.