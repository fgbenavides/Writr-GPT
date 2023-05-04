import openai
import random
import re


# Set up OpenAI API credentials
openai.api_key = "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"

# Ask user for input
reference_author = input("Please enter the name of a reference author: ")
num_chapters = int(input("Please enter the number of chapters in the book: "))
desired_num_words = int(input("Enter the desired number of words for Chapter 1: "))

# Generate book title based on reference author using ChatGPT
model_engine = "text-davinci-002"
prompt = f"Generate a book title in the style of {reference_author}"
generated_title = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=30, n=1,stop=None, temperature=0.7)
title = generated_title.choices[0].text.strip()

# Generate book summary based on title using ChatGPT
prompt = f"Generate a 150-word summary for a book titled '{title}', in the style of {reference_author}. Make sure you mention that the books is written in the style of {reference_author} somewhere in the summary"
generated_summary = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=300, n=1,stop=None, temperature=0.3)
summary = generated_summary.choices[0].text.strip()

# Generate chapter names based on title and summary using ChatGPT
prompt =f"Generate {num_chapters} chapter names for a book titled '{title}', in the style of {reference_author}. The chapter names should be consistent with the arc of the story of the following '{summary}' Make sure the chapter names are catchy and different from each other."
generated_chapters = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=500, n=1,stop=None, temperature=0.3)
chapters = generated_chapters.choices[0].text.strip()

# Generate chapter 1 content based on title and summary using ChatGPT
prompt = f"Write the first chapter for a book titled '{title}', in the style of {reference_author}, consistent with the arc of the story of the following '{summary}' and consistent with the chapter name for chapter 1 generated in {chapters}. Combine long and short paragraphs, use dialogues, long and short sentences, always in the style of {reference_author}. Be excruciatingly detailed in the description of the characters, physically and their personalities."
generated_chapter1 = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=1024, n=1,stop=None, temperature=0.3)
chapter1 = generated_chapter1.choices[0].text.strip()

# count the number of words in the generated text
num_words = len(re.findall(r'\w+', chapter1))

# check if the number of words is less than the desired number
while num_words < desired_num_words:
    # continue generating text
    response = openai.Completion.create(
      engine="davinci",
      prompt=chapter1,
      max_tokens=100,
      n=1,
      stop=None,
      temperature=0.3
    )

# extract the generated text from the response
    new_chapter1 = response.choices[0].text
    
    # add the new text to the generated text
    chapter1 += new_chapter1

# count the number of words in the updated generated text
    num_words = len(re.findall(r'\w+', chapter1))


# Write the book information to a file
file_name = f"{title}.txt"
with open(file_name, "w") as f:
    f.write(f"Title: {title}\n\n")
    f.write(f"Summary: {summary}\n\n")
    f.write(f"Chapters: \n{chapters}\n\n")
    f.write(f"Chapter 1: {chapter1}\n\n")


print("Job completed!")
print("Chapter 1 has ", chapter1," words")
