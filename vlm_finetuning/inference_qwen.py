"""
NOTE run inference with qwen model (base or finetuned)
"""

import pandas as pd
from tqdm import tqdm
from qwen_helper_funcs import load_model, inference
from constants import SYSTEM_PROMPT
import os
from helper_funcs import display_image


LORA_MODEL_PATH = "./finetuned_qwen_models/lora_model_20250414_134955"


# ---
# inference
# ---


cols_to_predict = [
    "wild_strawberry_timespan",
    "wood_sorrel_flowering",
    "wood_sorrel_fruit",
    "wood_sorrel_timespan",
    "arctic_starflower_flowering",
    "arctic_starflower_fruit",
    "arctic_starflower_timespan",
    "linnaea_flowering",
    "linnaea_fruit",
    "linnaea_timespan",
]

if __name__ == "__main__":

    # base_model, base_tokenizer = load_model() # base model
    model, tokenizer = load_model(LORA_MODEL_PATH)  # finetuned model

    df = pd.read_pickle("data/phenology_df.pkl")
    display_image(df["number_image"].values[0])

    for col_to_predict in cols_to_predict:

        predictions = []
        for i in tqdm(range(len(df))):

            image_bytes = df.iloc[i][col_to_predict + "_image"]
            response = inference(model, tokenizer, image_bytes, SYSTEM_PROMPT)
            predictions.append(response)
            if i % 10 == 0:
                display_image(image_bytes)
                print("Prediction: ", response)

        # write predictions to file
        labels_path = f"labels/label_{col_to_predict}.txt"
        if os.path.exists(labels_path):
            print("PATH ALREADY EXISTS; SKIPPING WRITING")
        else:
            with open(labels_path, "w") as f:
                for pred in predictions:
                    f.write(pred + "\n")

            print(f"Predictions written to {labels_path}")
