from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_ID = "nlptown/bert-base-multilingual-uncased-sentiment"

if __name__ == "__main__":
    print(f"Baixando tokenizador e pesos de '{MODEL_ID}' para o cache local...")
    AutoTokenizer.from_pretrained(MODEL_ID)
    AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
    print("Download concluído com sucesso! O modelo está pronto para execução offline.")