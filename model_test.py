import numpy as np
import pandas as pd
from tqdm import tqdm, tqdm_pandas
import torch
from transformers import PreTrainedTokenizerFast
from transformers.models.bart import BartForConditionalGeneration

model = BartForConditionalGeneration.from_pretrained('./kobart_summary')
tokenizer = PreTrainedTokenizerFast.from_pretrained('gogamza/kobart-base-v1')
docs = pd.read_csv('/home/nsun/nlp_project/kobart/KoBART-summarization/data/final_test_clean.tsv', sep='\t')
cols = docs.columns

# text = input()

# if text:
#     input_ids = tokenizer.encode(text)
#     input_ids = torch.tensor(input_ids)
#     input_ids = input_ids.unsqueeze(0)
#     output = model.generate(input_ids, eos_token_id=1, max_length=512, num_beams=5)
#     output = tokenizer.decode(output[0], skip_special_tokens=True)
#     print(output)

def input_text(text, tokenizer, model):
    input_ids = tokenizer.encode(text)
    input_ids = torch.tensor(input_ids)
    input_ids = input_ids.unsqueeze(0)
    output = model.generate(input_ids, eos_token_id=1, max_length=512, num_beams=5)
    output = tokenizer.decode(output[0], skip_special_tokens=True)
    return output

tqdm_pandas(tqdm())
docs['model_summary'] = docs[cols[0]].progress_apply(lambda x: input_text(x, tokenizer, model) if bool(x)==True else np.nan)
docs.to_csv('/home/nsun/nlp_project/kobart/KoBART-summarization/output/final_test_modeloutput.csv', index=False)
print('output saved')