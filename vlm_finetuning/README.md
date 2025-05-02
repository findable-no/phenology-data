# Overview

This folder contains the files used to create a dataset, and fine-tune Qwen2.5 VL 7B

To use the repo, first create a virtual env, and install required packages with 
´´´python
pip install -r qwen_requirements.txt
´´´




## Description of files

### constants.py
Hyperparameters for LLM generation. Also contains the system prompt

### easyocr_inference.py
Run inference with EasyOCR. This is used to create a benchmark for performance

### finetune_qwen.py
Finetune qwen. The model is stored based on current date and time to create a unique save

### geo_plotting.py
Plot data points to have extracted onto a map of Norway using the H3 library from Uber (https://www.uber.com/en-NO/blog/h3/)
TODO also update the file

### helper_funcs.py
Helper functions to plot images. Used by the labeling pipeline to easily display images along with their labels

### inference_qwen.py
Input the path to a fine-tuned Qwen model and run inference with it.

### labeling.ipynb
Notebook used to review and correct labels. Contains 2 main aspects:
1. Normal labeling: Print out predictions for a file and the images, so you can easily correct mistakes
2. Grouping: Group samples by their labels (for example: only blank labels, only lables with "7" in them ...)

### prepare_data_qwen.py
Prepare dataset for fine-tuning. This includes loading labels from txt files and converting to expected format for LLM with image + text

### qwen_helper_funcs.py
Includes functions to load the Qwen 2.5 VL model (you can specify the path to an adapter, else it will load the base model), and run inference with a model + tokenizer.



## References:
- [Qwen 2.5 VL paper](https://arxiv.org/abs/2502.13923)
- [H3 by Uber](https://www.uber.com/en-NO/blog/h3/)
- [Unsloth for fine-tuning](https://docs.unsloth.ai/)