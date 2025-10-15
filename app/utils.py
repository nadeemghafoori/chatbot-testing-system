from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Initializing the tokenizer and model.
tokenizer = AutoTokenizer.from_pretrained("tuner007/pegasus_paraphrase")
model = AutoModelForSeq2SeqLM.from_pretrained("tuner007/pegasus_paraphrase")

def paraphrase(question):
    # Prefixing the text with "paraphrase: " to guide the model to generate paraphrase.
    text = "paraphrase: " + question
    # Defining the maximum length of the generated paraphrase.
    max_len = 100

    # Encoding the input text using the tokenizer.
    encoding = tokenizer.encode_plus(
        text, pad_to_max_length=True, return_tensors="pt")
    input_ids, attention_masks = encoding["input_ids"], encoding["attention_mask"]

    # Using the model to generate paraphrases of the input text.
    outputs = model.generate(
        input_ids=input_ids, attention_mask=attention_masks,
        max_length=max_len, num_beams=10, num_return_sequences=1, temperature=1.5
    )

    # Decoding the output from the model and returning it as a string.
    return tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
