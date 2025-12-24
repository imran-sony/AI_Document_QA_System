from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"    # all-MiniLM-L6-v2      # all-mpnet-base-v2
)
