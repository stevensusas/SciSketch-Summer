## Class: ScienceDirectScraper

### scrape_search_api():
scrapes the search_api results into a pandas df

### get_graphical_abstract()
    use ObjectRetrieval API to find graphical abstracts for the search_api doi results
    only keep rows where graphical abstracts are found, populate grpahical abstract row with base name
    populate AWS S3 object bucket with the found graphical abstracts

### get_abstract()
    use ObjectRetrievel API to find abstract for the search_Api doi results. only keep rows where abstracts are found.

### persist()
    persist the resulting dataframe to a MySQL table labelled with current date

## Class: MySQL
    MySQL housekeeping functionalities (create table, update table, get table, populate table, connect to database, etc...)

## Class: Flan-T5 Finetuner

### ExtractJSON_()
    Use OCR to extract JSON objects from S3 object storage. Then combine JSON objects with the abstract and title, prepare training dataset, prepare LLM finetuning and regression finetuning model

### Finetune_LLM()
    load FlanT5 pretrained model and finetune LLM model, enable loss monitoring and etc. through tensor board

### Finetune_regression()
    load FlanT5 pretrained model and finetune regression model, enable loss monitoring and etc. through tensor board

### deploy_language_model()
    deploy the langauge model to Huggingface Inference API

### deploy_regression_model()
    deploy the regression model to Flask backend inference usage
