from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# Load tokenizer and model
tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

# Summarization function with adjustable summary length
def summarize(text, length="medium"):
    size_limit = {
        "short": 100,
        "medium": 200,
        "detailed": 300
    }

    # Encode the input text
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)

    # Generate summary
    summary_ids = model.generate(
        inputs,
        max_length=size_limit[length],
        min_length=20,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )

    # Decode and return the summary
    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return output
