from PyPDF2 import PdfReader

import os

import pandas as pd

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.cache import InMemoryCache
import langchain

from ocr.ocr import process_pdf
from docs.search import doc_search
from extract.extract import knowledge_graph
from data.processing import rowify
from edi.edi_formatter import pandas_to_edi

from openai.error import InvalidRequestError


langchain.llm_cache = InMemoryCache()
llm = OpenAI(temperature=0)

embeddings = OpenAIEmbeddings()

chain = load_qa_chain(llm, chain_type="stuff")

pdf_inputs = []

key_ids = ""

query = f"""
Using the unique count of {key_ids} in this document, do the following:
    For each {key_ids}, extract the following information corresponding to the {key_ids}:
    """

rules_template = f"""Just give me the answer with {key_ids} line separated and nothing else."""

pdf_data = []

pdf_dir = '/pdfs/'
fils = os.listdir(pdf_dir)

for fil in fils:
    print("processing: " + fil)
    try:
        pdf_file = pdf_dir + fil
        texts = process_pdf(pdf_file)
        docsearch = doc_search(texts, embeddings)
        hwb_data = knowledge_graph(
            key_id="",
            docsearch=docsearch,
            pdf_inputs=pdf_inputs,
            query=query,
            rules_template=rules_template,
            chain=chain
        )

        mwb = fil.split('-')[1]
        rows = rowify(hwb_data, extra=[mwb])

        pdf_data.extend(rows)
    except InvalidRequestError:
        print(fil, "File needs handler.")

cols = []
df = pd.DataFrame(columns=cols, data=pdf_data)

edi_data = pandas_to_edi(
    edi_type='211',
    df=df,
    edi_key_col="",
    edi_data_col="",
)