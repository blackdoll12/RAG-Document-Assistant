from function_lib import preprocess_document
import argparse
def answer_question(qa, question):
    """
    Answers a given question using the preprocessed QA pipeline.

    Args:
        qa (obj): The QA pipeline.
        question (str): The question to answer.
    """
    response = qa.invoke({"query": question}) 
    print("\nQuestion:\n"+question)
    
    if "I don't know" in response["result"]:
        print("\nAnswer:\nI couldn't find the answer in the provided context.")
        
    else:
        print("\nAnswer:\n"+response["result"])
        
    
    
    
   

if __name__ == "__main__":
    

        parser = argparse.ArgumentParser(description="QA Pipeline Argument Parser")
        parser.add_argument(
            "--default", 
            action="store_true", 
            help="Use default settings with 'LinearAlgebra.txt' and 'questions.txt'."
        )
        parser.add_argument(
            "--file_path", 
            type=str, 
            help="Path to the input PDF file (required if --default is not set)."
        )
        parser.add_argument(
            "--question", 
            type=str, 
            help="The question to ask the QA system (used only if --default is not set)."
        )
        
        # Parse the arguments
        args = parser.parse_args()

        if args.default:
            # Default behavior
            qa = preprocess_document("data/LinearAlgebra.txt")
            with open("questions.txt", "r") as file:
                questions = file.readlines()
            for question in questions:
                if not question:  # Skip empty lines
                    continue
                answer_question(qa=qa, question=question)
        else:
            # Custom behavior
            if not args.file_path or not args.question:
                raise ValueError("Both --file_path and --question must be provided if --default is not set.")
            
            qa = preprocess_document(args.file_path)
            answer_question(qa=qa, question=args.question)

         