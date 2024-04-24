from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "gpt2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

prompt = "I am the"
input_ids = tokenizer.encode(prompt, return_tensors="pt")

attention_mask = input_ids.ne(0).long()

output = model.generate(
    input_ids,
    max_length=50,
    num_return_sequences=1,
    attention_mask=attention_mask,
    pad_token_id=tokenizer.eos_token_id,
)

print(tokenizer.decode(output[0], skip_special_tokens=True))