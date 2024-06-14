from libs.libs_func import load_config
from libs.modules.data_pipeline import DataProcessingPipeline
from libs.modules.model_modules import ModelModules
from libs.libs_func import display_word_mispronounce, compare_transcript_canonical

# config
conf = load_config("./configs/default.yaml")

# init model modules
model_modules = ModelModules(config=conf)

# data pipeline
data_pipeline = DataProcessingPipeline(conf=conf)

# vmd service
def vmd_service(media, text):
    phonetic_emb, canonical_phoneme = data_pipeline.get_processed_input(
        media, text
    )  # get phonetic embedding and canonical phoneme

    prediction = model_modules.get_prediction(phonetic_emb, canonical_phoneme)

    canonical_phoneme = canonical_phoneme.split()  # split to List

    compared_list = compare_transcript_canonical(canonical_phoneme, prediction)
    compared_result = display_word_mispronounce(canonical_phoneme, compared_list)
    text = text.split()  # split target text to align with result

    result = dict(zip(text, compared_result))

    return result
