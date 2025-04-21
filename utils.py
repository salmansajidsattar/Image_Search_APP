import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import requests
import json
import os
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Subset
import config

# Load the CLIP model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
# Directory to save the dataset
dataset_dir = "./data"
# Function to preprocess images and extract features

def index_image(image, label, image_id):
    features = extract_features(image)
    document = {
        "name": f"image_{image_id}",
        "label": label,
        "vector": features
    }
    response = requests.post(
        f"{config.ES_HOST}/{config.ES_INDEX}/_doc/{image_id}",
        headers={"Content-Type": "application/json"},
        auth=(config.ES_USER, config.ES_PASS),
        data=json.dumps(document)
    )
    return response.json()
def extract_features(image):
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)
    image_features = image_features / image_features.norm(dim=-1, keepdim=True)
    return image_features.squeeze().tolist()

# Function to search for similar images
def search_similar_images(query_image_path, k=5):
    # query_image = Image.open(query_image_path)
    query_features = extract_features(query_image_path)
    search_query = {
        "knn": {
            "field": "vector",
            "query_vector": query_features,
            "k": k,
            "num_candidates": 100
        }
    }
    response = requests.post(
        f"{config.ES_HOST}/{config.ES_INDEX}/_knn_search",
        headers={"Content-Type": "application/json"},
        auth=(config.ES_USER, config.ES_PASS),
        data=json.dumps(search_query)
    )
    list=[]
    for hit in response.json()['hits']['hits']:
        image_id = hit['_id']
        label = hit['_source']['name']
        list.append(str(label+'.jpg'))
    return list

def main():
    # Download and prepare the dataset (using Oxford Pets for demo)
    
    transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])
    dataset=datasets.ImageFolder(root=dataset_dir,transform=transform)

    # Take a subset of 100 images
    subset_indices = list(range(100))
    subset = Subset(dataset, subset_indices)
    data_loader = DataLoader(subset, batch_size=1, shuffle=False)

    # Ensure there are at least 100 images
    assert len(subset) >= 100, "Dataset should contain at least 100 images."


    # Index the images with labels
    for i, (image, label) in enumerate(data_loader):
        # Convert tensor to PIL image
        image = transforms.ToPILImage()(image[0])
        label = dataset.classes[label]
        result = index_image(image, label, i)
        image_path = os.path.join(dataset_dir, f"image_{i}.jpg")
        image.save(image_path)  # Save the image for later retrieval
        print(f"Indexed image {i} with label '{label}': {result}")

if __name__ == "__main__":
    # main()
    # res=search_similar_images('./data/image_1.jpg')
    # image_id = res['hits']['hits'][0]['_id']
    # label = res['hits']['hits'][0]['_source']['name']
    # print(f"Retrieved image {image_id} with label '{label}'")
    # print(res)
    pass
