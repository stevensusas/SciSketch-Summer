# SciSketch
SciSketch is the world's first life science illustrator -- You can think about it as the AI-powered BioRender. Creating complex molecular and biochemical illustrations for research manuscripts can be a tedious and time-consuming task. Existing tools, like BioRender, require users to manually select, arrange, and annotate icons on a digital canvas, which can be frustrating and redundant. This process often leads to scientists spending significant time on creating visuals instead of focusing on their research.

SciSketch addresses these challenges by offering a streamlined and automated solution for generating professional science figures. By leveraging advanced algorithms, SciSketch transforms detailed textual information into clear, concise, and visually appealing diagrams in seconds. This innovative tool not only saves time but also ensures that scientific illustrations are accurate and high-quality.

With SciSketch, researchers can efficiently create the necessary visuals for their manuscripts, grant proposals, and presentations, allowing them to dedicate more time to their scientific discoveries and advancements.

Watch the first iteration of SciSketch's prototype, built solely with React, Flask, and the OpenAI API at the 2024 Penn Generative AI Hackathon:


I am currently actively working on building the second iteration of SciSketch's prototype. It involves the following smaller parts, some already complete and other still being works in progress, given the immensity of the project's scale:

## BioIllustra: The Training Dataset

Check out the dataset itself on Hugging Face!

To create SciSketch, I created BioIllustra, a the dataset consisting of 30,000+ biomedical text abstracts and their corresponding graphical abstracts. To create BioIllustra, I utilized the ScienceDirect API to collect data from more than 50,000 published research articles in Cell Press. Then, I used OCR and DBSCAN clustering to extract the text entities in the graphical abstracts, as well as their coordinates and width, height in the graphic. The extracted information is presented in JSON format to accomodate downstream model training purposes.

The data processing and feature engineering was a computationally expensive process due to the large datasize. To reduce computation time and cost, I utilized Dask for parallel computing, AWS S3 for data storage, and AWS EC2, Spark, and Databricks to create a distributed computing environment.

## IconIllustra: The Icons Dataset

The model need icons it can call in order to convert the json output from inference into graphics. This step involve an important feature that maps biomedical texts to graphical icons with similar semantic meaning. To do this, I decided to utilize embedding similarity search. By converting the icons' descriptive file name to vector embeddings with ChatGPT4-Turbo and storing the vector embeddings as well as the icon images as key-value pairings in a vector database (ChromaDB), each outpyut text from model inference can be quickly and accurately mapped to icon images.

To further improve the icon-text semantic mapping accuracy, I designed a decision tree based data structure to empower the vector embedding search with RAG. To construct the decision tree, I utilized BioCypher--a framework that allows efficient creation of ontology-based knowledge graph consisted of biomedical entities. Each text query for the optimal icon match to this data structure traverses the knowledge graph into more and more specific ontologies until a the best fit have been found.

## Model Finetuning

![Graphical Abstract Generator Diagram (1)](https://github.com/stevensusas/SciSketch-Summer/assets/113653645/2e7551ae-e833-4b53-ad92-543c279d370b)

I chose BERT-T5 (11b) as the foundational, pretrained model for the finetuning process. T5 uses an encoder-decoder architecture, enabling it with both deep, bidirectional contextual understanding of input text and text generation abilities. To construct a GPU-enabled computing environment with relatively low cost, I utilized Google Cloud's Compute Engine to instantiate a Linux virtual machine with 1x NVIDIA A100.

Then, I used PyTorch to modify T5 for specific finetuning tasks:

1. Predicting tokens that are present in output images: This task is relatively straightforward. It does not require modifying the model architecture, as it simply generates new tokens from input abstract text based on examples in the BioIllustra dataset.
2. Predicting tokens' width, height, x and y coordinates in output images: This task requires adding a regression head to T5, so that it outputs numeric values indicating these 4 parameters of output text upon finetuning.

## Model Deployment

To deploy the model quickly and scalably in a MVP beta testing version to quickly gain user feedback and iterate & improve, we will be hosting the finetuned model on cloud servers for inference and the frontend in Google Workspace Add-on so people can use it as a plug-in for Google Docs. However, we are also building a full-stack webapp with the MERN-stack, with the graphic editting view built with Fabric.js and the text editting view built with Quill.js, so that in the long-term we can have our own webapp for developing more features. 



