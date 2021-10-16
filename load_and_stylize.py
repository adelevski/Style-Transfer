import re
import io
import threading

from PIL import Image
import streamlit as st

import torch
from torchvision import transforms

from transformer_net import TransformerNet


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

@st.cache
def load_model(model_path):
    print(f'Loading model {model_path}')
    with torch.no_grad():
        style_model = TransformerNet()
        state_dict = torch.load(model_path)
        # remove saved deprecated running_* keys in InstanceNorm from the checkpoint
        for k in list(state_dict.keys()):
            if re.search(r'in\d+\.running_(mean|var)$', k):
                del state_dict[k]
        style_model.load_state_dict(state_dict)
        style_model.to(device)
        style_model.eval()
        return style_model


@st.cache
def stylize(style_model, content_image, size):
    content_image = io.BytesIO(content_image)
    content_image = Image.open(content_image)
    content_transform = transforms.Compose([
        transforms.Resize(size),
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.mul(255))
    ])
    content_image = content_transform(content_image)
    content_image = content_image.unsqueeze(0).to(device)
    with torch.no_grad():
        output = style_model(content_image).cpu()
            
    img = output[0].clone().clamp(0, 255).numpy()
    img = img.transpose(1, 2, 0).astype("uint8")
    img = Image.fromarray(img)
    return img
