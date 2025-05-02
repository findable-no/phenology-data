import pandas as pd
from PIL import Image as PILImage
from io import BytesIO
import random
from datasets import Dataset

RANDOM_STATE = 42

random.seed(RANDOM_STATE)


def make_labelled_df(
    dataset_path="data/phenology_df.pkl", labeled_columns=["blueberry_flowering"]
):
    assert len(set(labeled_columns)) == len(
        labeled_columns
    ), "labeled_columns must be unique"
    df = pd.read_pickle(dataset_path)

    df_labelled = df.copy()

    for col in labeled_columns:
        print(col)
        with open(f"labels/label_{col}.txt", "r") as f:
            label_col = f.readlines()
        label_col = [row.replace("\n", "") for row in label_col]

        df[col + "_labels"] = label_col

    with open("labels/label_location.txt", "r") as f:
        label_location = f.readlines()
    label_location = [row.replace("\n", "") for row in label_location]
    with open("labels/label_position_new.txt", "r") as f:
        label_position = f.readlines()
    label_position = [row.replace("\n", "") for row in label_position]
    df_labelled["location_labels"] = label_location
    df_labelled["position_labels"] = (
        label_position  # NOTE not using these for training, different labels basically
    )

    all_columns = [col + "_labels" for col in labeled_columns] + [
        col + "_image" for col in labeled_columns
    ]

    df_labelled = df[all_columns]

    df_labelled.to_pickle("data/df_labelled_all.pkl")


def _convert_to_conversation(sample, system_prompt):
    conversation = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": system_prompt},
                {"type": "image", "image": sample["image"]},
            ],
        },
        {"role": "assistant", "content": [{"type": "text", "text": sample["text"]}]},
    ]
    return {"messages": conversation}


def prep_image(image_bytes):
    return PILImage.open(BytesIO(image_bytes))


def prepare_inference_sample(instruction):
    return [
        {
            "role": "user",
            "content": [{"type": "image"}, {"type": "text", "text": instruction}],
        }
    ]


def prepare_dataset(
    dataset_path, system_prompt, labeled_columns, accepted_blank_percentage=0.3
):
    """percentage blank accepted is % of labels you accept to be empty string"""

    image_and_label_columns = [
        (col + "_image", col + "_labels") for col in labeled_columns
    ]

    df_labelled = pd.read_pickle(dataset_path)
    # now prepare data for qwen

    # Prepare the data in the format expected by Dataset
    dataset_dict = {
        "image": [],
        "text": [],
        "category": [],  # To keep track of which category (flowering or fruit)
    }

    # make a 2d list of all images and labels
    all_images = []
    all_labels = []
    for img_col, label_col in image_and_label_columns:
        all_images.extend(df_labelled[img_col].tolist())
        all_labels.extend(df_labelled[label_col].tolist())

    tot_num_labels = len(all_labels)
    num_blank_labels = sum(1 for label in all_labels if label == "")

    accepted_num_blank_labels = int(accepted_blank_percentage * tot_num_labels)

    # select blank images to ignore (since we don't want too many blank labels)
    blank_labeled_images_indices = [
        i for i, label in enumerate(all_labels) if label == "" or label == "%"
    ]
    num_indices_to_ignore = (
        len(blank_labeled_images_indices) - accepted_num_blank_labels
    )
    if num_indices_to_ignore > 0:
        indices_to_ignore = random.sample(
            blank_labeled_images_indices, num_indices_to_ignore
        )
    else:
        indices_to_ignore = []

    all_images = [img for i, img in enumerate(all_images) if i not in indices_to_ignore]
    all_labels = [
        label for i, label in enumerate(all_labels) if i not in indices_to_ignore
    ]

    # set empty labels to unknown
    all_labels = ["unknown" if label == "" else label for label in all_labels]

    # Extract image-label pairs from the DataFrame
    for img, label in zip(all_images, all_labels):
        # Convert bytes to PIL Image
        pil_image = prep_image(img)

        # Add to dataset dictionary
        dataset_dict["image"].append(pil_image)
        dataset_dict["text"].append(label)
        dataset_dict["category"].append(img_col.replace("_image", ""))

    # Create the Dataset
    dataset = Dataset.from_dict(dataset_dict)

    converted_dataset = [
        _convert_to_conversation(sample, system_prompt) for sample in dataset
    ]

    return converted_dataset
