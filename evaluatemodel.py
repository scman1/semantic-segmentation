# code imported from jupiter notebook
#[1] Required libraries
from pathlib import Path
import random

import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
from torch.autograd import Variable
from torchvision import transforms

from segmentation.datasets import Slides, ImageFolder, SemiSupervisedDataLoader
from segmentation.instances import DiscriminativeLoss, mean_shift, visualise_embeddings, visualise_instances
from segmentation.network import SemanticInstanceSegmentation
from segmentation.training import train, evaluateepochs

#[2] create model and clustening function
model = SemanticInstanceSegmentation() #From network
instance_clustering = DiscriminativeLoss() #From instances

#[3] random transforms for pictures
transform = transforms.Compose([ #torchvision
    transforms.RandomRotation(5),
    transforms.RandomCrop((256, 768)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),
    transforms.ToTensor()])

target_transform = transforms.Compose([transform, transforms.Lambda(lambda x: (x * 255).long())])

batch_size = 3

# WARNING: Don't use multiple workers for loading! Doesn't work with setting random seed
# Slides: copies the data if required into the data/raw/[images,
# instances, labels] directories and returns
# import pdb; pdb.set_trace()

test_data_labelled = Slides(download=True, train=False, root='data', transform=transform, target_transform=target_transform)
test_loader_labelled = torch.utils.data.DataLoader(test_data_labelled, batch_size=batch_size, drop_last=True, shuffle=True)
test_data_unlabelled = ImageFolder(root='data/slides', transform=transform)
test_loader_unlabelled = torch.utils.data.DataLoader(test_data_unlabelled, batch_size=batch_size, drop_last=True, shuffle=True)
test_loader = SemiSupervisedDataLoader(test_loader_labelled, test_loader_unlabelled)

#testing
print(test_loader)
#for image, labels, instances in iter(test_loader)
#  print(image, labels, instances)
#[4] Train model
epochs = 50
evaluateepochs(model, instance_clustering, test_loader, 50)


