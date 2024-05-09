import ray
from sentence_transformers import SentenceTransformer


@ray.remote
class ModelActor:
    def __init__(self):
        # Load pre-trained Sentence Transformer model
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.model = SentenceTransformer(self.model_name)

    def encode_sentences(self, sentences):
        # Encode sentences using the loaded model
        embeddings = self.model.encode(sentences)
        return embeddings
