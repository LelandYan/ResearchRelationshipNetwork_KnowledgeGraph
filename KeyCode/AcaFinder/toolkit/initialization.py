# *_*coding:utf-8 *_*


import sys
import os
from Model.neo4j_models import Neo4jTool
from toolkit.embedding.vec_sim import EmbeddingModel
import fasttext

neo_con = Neo4jTool()  # Load neo4j
neo_con.connect2neo4j()
print('Neo4j has connected...')
# Load author embedding
author_emb = EmbeddingModel()
author_emb.read_vec(os.path.dirname(os.path.abspath(__file__)) + r'\embedding\entity_embeddings.tsv', 'author')
print("Embedding has load from " + os.path.dirname(os.path.abspath(__file__)) + r'\embedding\entity_embeddings.tsv')

# classifier = fasttext.load_model(os.path.dirname(os.path.abspath(__file__)) + r"\fasttextModel\model_file.bin")
# print("load fasttext model from " + os.path.dirname(os.path.abspath(__file__)) + r"\fasttextModel\model_file.bin")
