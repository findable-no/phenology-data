from prepare_data_qwen import prep_image, prepare_inference_sample
from unsloth import FastVisionModel
from tqdm import tqdm

from constants import TEMPERATURE, MIN_P, MAX_NEW_TOKENS


def load_model(LORA_MODEL_PATH=None):
    model_path = (
        "unsloth/Qwen2.5-VL-7B-Instruct" if LORA_MODEL_PATH is None else LORA_MODEL_PATH
    )

    print("Loading model from: ", model_path)
    model, tokenizer = FastVisionModel.from_pretrained(
        model_path,
        load_in_4bit=False,
        use_gradient_checkpointing="unsloth",
    )

    FastVisionModel.for_inference(model)

    return model, tokenizer


def inference(model, tokenizer, image_bytes, system_prompt):

    image = prep_image(image_bytes)
    messages = prepare_inference_sample(system_prompt)
    input_text = tokenizer.apply_chat_template(messages, add_generation_prompt=True)
    inputs = tokenizer(
        image,
        input_text,
        add_special_tokens=False,
        return_tensors="pt",
    ).to("cuda")

    response = model.generate(
        **inputs,
        max_new_tokens=MAX_NEW_TOKENS,
        use_cache=True,
        temperature=TEMPERATURE,
        min_p=MIN_P
    )

    # Get only the generated tokens by finding where assistant response starts
    response_text = tokenizer.decode(response[0], skip_special_tokens=True)
    # Check for different possible formats of assistant marker
    assistant_idx = -1
    for marker in ["assistant\n", "assistant: ", "assistant : "]:
        idx = response_text.find(marker)
        if idx != -1:
            assistant_idx = idx
            assistant_marker = marker
            break
    if assistant_idx != -1:
        response_text = response_text[assistant_idx + len(assistant_marker) :].strip()

    if response_text == "unknown":
        response_text = ""
    response_text = response_text.replace("\n", "")  # Remove newlines
    return response_text
