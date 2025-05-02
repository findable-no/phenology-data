"""
Finetune qwen to extract phenology data

I recommend running this file as an interactive window first
"""

from qwen_helper_funcs import inference
from constants import SYSTEM_PROMPT
import pandas as pd
import numpy as np
from tqdm import tqdm
from helper_funcs import display_image
from unsloth import FastVisionModel
from unsloth import is_bf16_supported
from unsloth.trainer import UnslothVisionDataCollator
from trl import SFTTrainer, SFTConfig
from datetime import datetime
from prepare_data_qwen import prepare_dataset, make_labelled_df

# from PIL import Image as PILImage
from constants import SYSTEM_PROMPT
import pandas as pd


DATASET_PATH = "data/df_labelled_all.pkl"  # TODO update this to your own path


train_columns = [
    "coltsfoot_fruit",
    "wheat_maturing_time",
    "sowtime_wheat",
    "sowtime_barley",
    "liverleaf_fruit",
    "wood_anemone_flowering",
    "oats_maturing_time",
    "barley_maturing_time",
]

test_columns = [
    "coltsfoot_flowering",
    "wheat_ripe_for_harvesting",
    "grey_alder_greenup",
    "hazel_flowering",
]


all_columns = train_columns + test_columns
make_labelled_df(all_columns)


r_value = 16
num_epochs_value = 2
lr_value = 1e-4


model, tokenizer = FastVisionModel.from_pretrained(
    "unsloth/Qwen2.5-VL-7B-Instruct",
    load_in_4bit=False,  # Use 4bit to reduce memory use. False for 16bit LoRA.
    use_gradient_checkpointing="unsloth",  # True or "unsloth" for long context
)


model = FastVisionModel.get_peft_model(
    model,
    finetune_vision_layers=True,
    finetune_language_layers=True,
    finetune_attention_modules=True,
    finetune_mlp_modules=True,
    r=r_value,
    lora_alpha=r_value,  # Recommended alpha == r at least
    # lora_dropout = 0.1, # we are avoiding dropout because we are only nudging the model
    bias="none",
    random_state=3407,
    use_rslora=True,  # if you have a problem with exploding gradients, we support rank stabilized LoRA
    loftq_config=None,  # And LoftQ
)


df = pd.read_pickle(DATASET_PATH)

converted_dataset = prepare_dataset(DATASET_PATH, SYSTEM_PROMPT, train_columns)
converted_dataset_test = prepare_dataset(DATASET_PATH, SYSTEM_PROMPT, test_columns, 1)

print("Train len: ", len(converted_dataset))
print("Test len: ", len(converted_dataset_test))


# ---
# train the model
# ---

FastVisionModel.for_training(model)  # Enable for training!


trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    data_collator=UnslothVisionDataCollator(model, tokenizer),
    train_dataset=converted_dataset,
    eval_dataset=converted_dataset_test,
    args=SFTConfig(
        per_device_train_batch_size=4,
        gradient_accumulation_steps=1,
        num_train_epochs=num_epochs_value,
        learning_rate=lr_value,
        fp16=not is_bf16_supported(),
        bf16=is_bf16_supported(),
        logging_steps=30,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        output_dir="outputs",
        report_to="wandb",
        remove_unused_columns=False,
        dataset_text_field="",
        dataset_kwargs={"skip_prepare_dataset": True},
        dataset_num_proc=4,
        max_seq_length=2048,
    ),
)

trainer_stats = trainer.train()


now = datetime.now().strftime("%Y%m%d_%H%M%S")
model.save_pretrained(f"finetuned_qwen_models/lora_model_{now}")  # Local saving
tokenizer.save_pretrained(f"finetuned_qwen_models/lora_model_{now}")

print(f"Saved model to finetuned_qwen_models/lora_model_{now}")


# ---
# test the model
# ---

print("\nTesting model:\n")
df = pd.read_pickle(DATASET_PATH)


def print_errors(preds, gts, images):
    for i in range(len(preds)):
        pred = preds[i]
        gt = gts[i]
        if pred != gt:
            if pred == "":
                pred = "unknown"
            if gt == "":
                gt = "unknown"
            display_image(images[i])
            print(f"Error: {pred} != {gt}")


accuracies = []

for test_col in test_columns:
    print("Column: ", test_col)
    images = df[test_col + "_image"].values

    ground_truth = df[test_col + "_labels"].values
    base_model_preds = []
    lora_model_preds = []

    for i in tqdm(range(len(images))):
        image_bytes = images[i]
        lora_model_preds.append(inference(model, tokenizer, image_bytes, SYSTEM_PROMPT))

    lora_accuracy = round(np.mean(np.array(lora_model_preds) == ground_truth), 2)
    print(
        f"Finetuned model accuracy: {lora_accuracy} with r={r_value} and lr={lr_value} and num_epochs={num_epochs_value}"
    )
    accuracies.append(lora_accuracy)


# test with base model
from qwen_helper_funcs import load_model, inference

base_model, base_tokenizer = load_model()

for test_col in test_columns:
    print("Column: ", test_col)

    images = df[test_col + "_image"].values

    ground_truth = df[test_col + "_labels"].values

    base_model_preds = []
    for i in tqdm(range(len(images))):
        image_bytes = images[i]
        pred = inference(base_model, base_tokenizer, image_bytes, SYSTEM_PROMPT)
        base_model_preds.append(pred)

    base_model_accuracy = round(np.mean(np.array(base_model_preds) == ground_truth), 2)
    print(f"Base model accuracy: {base_model_accuracy}")


# we can also test easyocr to compare
from easyocr_inference import inference_easyocr

for test_col in test_columns:
    print("Column: ", test_col)

    images = df[test_col + "_image"].values

    ground_truth = df[test_col + "_labels"].values

    easyocr_preds = []
    for i in tqdm(range(len(images))):
        image_bytes = images[i]
        pred = inference_easyocr(image_bytes)
        easyocr_preds.append(pred)

    easyocr_accuracy = round(np.mean(np.array(easyocr_preds) == ground_truth), 2)
    print(f"EasyOCR accuracy: {easyocr_accuracy}")
