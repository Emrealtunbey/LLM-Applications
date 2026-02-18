from datasets import load_dataset
from transformers import AutoTokenizer, DataCollatorWithPadding, AutoModelForSequenceClassification, get_scheduler
from torch.utils.data import DataLoader
from torch.optim import AdamW
import torch
from tqdm.auto import tqdm
import evaluate

dataset = load_dataset("glue", "mrpc")
checkpoint = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)
optimizer = AdamW(model.parameters(), lr=5e-5, weight_decay=0.01)


def tokenize_function(example):
    return tokenizer(example["sentence1"], example["sentence2"], truncation=True)


tokenizedDataset = dataset.map(tokenize_function, batched=True)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

tokenizedDataset = tokenizedDataset.remove_columns(["sentence1", "sentence2", "idx"])
tokenizedDataset = tokenizedDataset.rename_column("label", "labels")
tokenizedDataset.set_format("torch")  # remove unnecessary columns,correct labels and set to format to PyTorch tensors

train_dataloader = DataLoader(tokenizedDataset["train"],shuffle = True, batch_size=8,collate_fn=data_collator)
eval_dataloader = DataLoader(tokenizedDataset["validation"],batch_size=8,collate_fn=data_collator)  # Preprocessing for training

num_epochs = 3
num_training_steps = num_epochs * len(train_dataloader)
lr_scheduler = get_scheduler("linear",optimizer=optimizer,num_warmup_steps=0,num_training_steps=num_training_steps)

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model.to(device)

progress_bar = tqdm(range(num_training_steps))

model.train()
for epoch in range(num_epochs):
    for batch in train_dataloader:
        batch = {k: v.to(device) for k,v in batch.items()}
        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()

        optimizer.step()
        lr_scheduler.step()
        optimizer.zero_grad()
        progress_bar.update(1)
metric = evaluate.load("glue","mrpc")
model.eval()
for batch in eval_dataloader:
    batch = {k: v.to(device) for k,v in batch.items()}
    with torch.no_grad():
        outputs = model(**batch)
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=-1)
    metric.add_batch(predictions=predictions,references=batch["labels"])
metric.compute()
