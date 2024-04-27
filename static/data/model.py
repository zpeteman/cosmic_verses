from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed


def poem_gen(prompt):
    max_length_1 = 16
    min_length_1 = 10
    prompt_length = 3

    set_seed(42)
    model_name = "elgeish/gpt2-medium-arabic-poetry"
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Encode the prompt for the first line
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    # Generate text with the prompt for the first line
    samples = model.generate(
        input_ids,
        do_sample=True,
        max_length=max_length_1,
        min_length=min_length_1,
        pad_token_id=50256,
        repetition_penalty=1.5,
        top_k=32,
        top_p=0.95,
    )

    # Decode the generated text for the first line
    generated_text = tokenizer.decode(samples[0].tolist())

    # Initialize an empty string to store the poem
    poem_str = generated_text.strip() + "\n"  # Initialize with the first line

    # Keep track of already seen words
    seen_words = set()

    # Remove duplicate words from the current line
    words = generated_text.split()
    unique_words = [word for word in words if word not in seen_words]
    seen_words.update(unique_words)  # Add unique words to the set

    # Extract last words for subsequent lines
    last_words = generated_text.split()[-prompt_length:]

    for i in range(7):  # Generate 4 more lines
        new_prompt = " ".join(last_words)
        input_ids = tokenizer.encode(new_prompt, return_tensors="pt")

        samples = model.generate(
            input_ids,
            do_sample=True,
            max_length=max_length_1 + 5,
            min_length=min_length_1,
            pad_token_id=50256,
            repetition_penalty=1.5,
            top_k=32,
            top_p=0.95,
        )

        generated_text = tokenizer.decode(samples[0].tolist())

        # Remove duplicate words from the current line
        words = generated_text.split()
        unique_words = [word for word in words if word not in seen_words]
        seen_words.update(unique_words)  # Add unique words to the set

        # Reconstruct the line without duplicates
        filtered_line = " ".join(unique_words)
        poem_str += filtered_line.strip() + "\n"  # Add the line to the poem string

        # Update last words for the next iteration
        last_words = filtered_line.split()[-prompt_length:]

    # Return the poem string
    return poem_str