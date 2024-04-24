from transformers import pipeline, set_seed

generator = pipeline("text-generation", model="gpt2")
set_seed(42)
output = generator("Hello, I'm a language model,", max_length=30, num_return_sequences=5)

for i, sample_output in enumerate(output):
    print(f"{i+1}: {sample_output['generated_text']}")
    print("--------------------------------------------------")