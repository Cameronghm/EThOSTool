import evaluate
from datasets import load_dataset
from transformers import AutoTokenizer, BigBirdPegasusForConditionalGeneration, pipeline, LongformerTokenizer, LongformerModel, LEDForConditionalGeneration, LEDTokenizer
import torch
import os
import FlaskWebProject.ATS_demo as esearch
from evaluate import load


# def calculateMetrics(reference, prediction):
#     bertscore = bertscorer.compute(predictions=[prediction], references=[reference], lang="en")
#     # {'precision':[value], 'recall':[value], 'f1':[value]}
#     # Rogue
#     rougescore = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL', 'rougeLsum'], use_stemmer=True)
#     rougescore = rougescore.score(reference, prediction)
#     # {'rogue1':value, 'rouge2':value, 'rogueL':value, 'rogueLsum':value}
#     rougescore['bertscore'] = bertscore
#     return rougescore

# Legacy Summary 
def legacy_summariser(text, min_length):
    stop_word = []
    with open('./stopWordList.txt','r') as f:
        for line in f.readlines():
            cword = line.strip()
            stop_word.append(cword)

    summarization = ""
    min_characters = min_length
    abstract_characters = len(text)
    proportion = min_characters / abstract_characters

    if proportion < 1:
        sentence_set,sentence_with_index = esearch.split_sentence(text, punctuation_list="!.?")
        tfidf_matrix = esearch.get_tfidf_matrix(sentence_set,stop_word)
        sentence_with_words_weight = esearch.get_sentence_with_words_weight(tfidf_matrix)
        sentence_with_position_weight = esearch.get_sentence_with_position_weight(sentence_set)
        sentence_score = esearch.get_similarity_weight(tfidf_matrix)
        sort_sent_weight = esearch.ranking_base_on_weigth(sentence_with_words_weight,sentence_with_position_weight,sentence_score, feature_weight = [0.6,0.2,0.2])
        summarization = esearch.get_summarization(sentence_with_index,sort_sent_weight,topK_ratio =proportion)
        
    return summarization.strip()

def new_summariser(text, model):
    #text = legacy_summariser(text, 1000)
    tokenizer = LEDTokenizer.from_pretrained(model)
    token_ids = tokenizer.encode(text, return_tensors="pt").to("cuda")
    decoder = LEDForConditionalGeneration.from_pretrained(model).to("cuda")
    summary = decoder.generate(token_ids, num_beams=2, min_length=250, max_length=1000)
    summary = tokenizer.decode(summary[0])
    
    del token_ids
    del decoder

    return summary

# Summarising all both and then together
def combined_summarisation(introduction, conclusion):
    tokenizer = LEDTokenizer.from_pretrained("allenai/led-base-16384")
    intro_ids = tokenizer.encode(introduction, return_tensors="pt").to("cuda")
    decoder = LEDForConditionalGeneration.from_pretrained("allenai/led-base-16384").to("cuda")
    summary_ids_intro = decoder.generate(intro_ids, num_beams=3, min_length=250, max_length=500)

    del intro_ids
    del decoder

    concl_ids = tokenizer.encode(conclusion, return_tensors="pt").to("cuda")
    decoder = LEDForConditionalGeneration.from_pretrained("allenai/led-base-16384").to("cuda")
    summary_ids_concl = decoder.generate(concl_ids, num_beams=3, min_length=250, max_length=500)

    del concl_ids
    del decoder

    combined = tokenizer.decode(summary_ids_intro[0]) + tokenizer.decode(summary_ids_concl[0])
    combined_ids = tokenizer.encode(combined, return_tensors="pt").to("cuda")
    decoder = LEDForConditionalGeneration.from_pretrained("allenai/led-base-16384").to("cuda")
    summary_ids_combi = decoder.generate(combined_ids, num_beams=3,min_length=250, max_length=1000)

    del combined_ids
    del decoder

    generated_abstract = tokenizer.decode(summary_ids_combi[0])

    return generated_abstract

# Summarising all both and combining
def combined_summarisation2(introduction, conclusion):
    tokenizer = LEDTokenizer.from_pretrained("allenai/led-base-16384")
    intro_ids = tokenizer.encode(introduction, return_tensors="pt").to("cuda")
    decoder = LEDForConditionalGeneration.from_pretrained("allenai/led-base-16384").to("cuda")
    summary_ids_intro = decoder.generate(intro_ids, num_beams=1, min_length=250, max_length=1000)

    del intro_ids
    del decoder

    concl_ids = tokenizer.encode(conclusion, return_tensors="pt").to("cuda")
    decoder = LEDForConditionalGeneration.from_pretrained("allenai/led-base-16384").to("cuda")
    summary_ids_concl = decoder.generate(concl_ids, num_beams=1, min_length=250, max_length=1000)

    del concl_ids
    del decoder

    combined = tokenizer.decode(summary_ids_intro[0]) + tokenizer.decode(summary_ids_concl[0])

    return combined

# Summarising all both and combining
def combined_summarisation_both(introduction, conclusion):
    tokenizer = LEDTokenizer.from_pretrained("allenai/led-base-16384")
    intro_ids = tokenizer.encode(introduction, return_tensors="pt").to("cuda")
    decoder = LEDForConditionalGeneration.from_pretrained("allenai/led-base-16384").to("cuda")
    summary_ids_intro = decoder.generate(intro_ids, num_beams=1, min_length=250, max_length=1000)

    del intro_ids
    del decoder

    concl_ids = tokenizer.encode(conclusion, return_tensors="pt").to("cuda")
    decoder = LEDForConditionalGeneration.from_pretrained("allenai/led-base-16384").to("cuda")
    summary_ids_concl = decoder.generate(concl_ids, num_beams=1, min_length=250, max_length=1000)

    del concl_ids
    del decoder

    combined = tokenizer.decode(summary_ids_intro[0]) + tokenizer.decode(summary_ids_concl[0])

    return combined

# Summarising all both and combining
def combined_summarisation_seperate(introduction, conclusion):
    tokenizer = LEDTokenizer.from_pretrained("allenai/led-base-16384")
    intro_ids = tokenizer.encode(introduction, return_tensors="pt").to("cuda")
    decoder = LEDForConditionalGeneration.from_pretrained("allenai/led-base-16384").to("cuda")
    summary_ids_intro = decoder.generate(intro_ids, num_beams=1, min_length=250, max_length=1000)

    del intro_ids
    del decoder

    combined = tokenizer.decode(summary_ids_intro[0]) + conclusion

    return combined
