import torch
from transformers import PreTrainedModel

def get_gradients(model: PreTrainedModel, batch, device: str) -> dict[str, torch.Tensor]:
    gradients = {}

    # set gradients to zero, so that gradients to not accumulate for each iteration
    model.zero_grad()

    output = model(input_ids=batch["input_ids"].to(device), labels=batch["labels"].to(device), attention_mask=batch["attention_mask"].to(device), use_cache=False)
    loss = output.loss

    loss.backward()

    for name, param in model.named_parameters():
        if param.grad is not None:
            gradients[name] = param.grad.clone().detach().cpu()

    return gradients


def get_flattened_weight_vector(weight_dict: dict[str, torch.Tensor]) -> torch.Tensor:
    flattened_weights = []
    for weights in weight_dict.values():
        flattened_weights.append(weights.cpu().flatten())

    return torch.cat(flattened_weights)