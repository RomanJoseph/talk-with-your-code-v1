import sys
from utils.query import query_codebase

def main():
    if len(sys.argv) < 2:
        print("Por favor, forneça uma pergunta")
        return
    question = sys.argv[1]
    answer = query_codebase(question)
    print("Resposta:\n", answer)

if __name__ == "__main__":
    main()
