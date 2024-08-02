import sagemaker
from sagemaker.model import Model
import numpy as np
from sagemaker.pytorch import PyTorchModel


# Initialize SageMaker session
sagemaker_session = sagemaker.Session()

# Define the PyTorch model
model = PyTorchModel(
    model_data='s3://scisketch-dataset/regression-model-flan-t5-base',
    role='arn:aws:iam::975050348274:role/service-role/AmazonSageMaker-ExecutionRole-20240715T150476',
    entry_point='inference.py',  # Your inference script
    framework_version='1.10.0',
    py_version='py38'
)

# Deploy the model
predictor = model.deploy(
    initial_instance_count=1,
    instance_type='ml.p3.2xlarge',
    endpoint_name='flan-t5-regression-base-2'
)   