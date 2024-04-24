
from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base", legacy=False)
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

input_text = "translate English to German: How old are you?"
input_ids = tokenizer(input_text, return_tensors="pt").input_ids

outputs = model.generate(input_ids, max_new_tokens=100)
print(tokenizer.decode(outputs[0]))