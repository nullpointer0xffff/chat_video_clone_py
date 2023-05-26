from langchain.text_splitter import TokenTextSplitter

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from codetiming import Timer
import openai
import argparse
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from youtube import download_transcribe
import json

text_splitter = TokenTextSplitter(chunk_size=2500)

OPENAI_API_KEY = <YOUR_API_KEY>
openai.api_key = OPENAI_API_KEY

# MODEL_NAME="gpt-3.5-turbo"
MODEL_NAME="gpt-4"


def summarize(transcribe):
    # 2. Summarization part
    # - split the transcribe into chunks
    # - use langchain summarize each chunk/whole via GPT-4
    # - use langchain to get top 1 most attactive question from this chunk and the answer to it, add to question list
    # - display the summary, questions and answers to the user
    transcribe_text = "\n".join([d['text'] for d in transcribe])
    texts = text_splitter.split_text(transcribe_text)
    docs = [Document(page_content=t) for t in texts]
    print("docs lengtb", len(docs))
    llm = ChatOpenAI(temperature=0, model_name=MODEL_NAME, openai_api_key=OPENAI_API_KEY)

    prompt_template = """Please write a summary and top 3 questions you think most attractive to public audiance of the following text:
    ```
    {text}
    ```
    requirements:
    - less than 5 sentences
    - use fact from the text only
    - no opinion
    - the 3 questions should have attractive_score 0-10 to identify how attractive the question is
    - output in json format with keys: summary, questions, each question has keys: question, answer, attractive_score
    """
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
    print(PROMPT)
    chain = load_summarize_chain(llm, chain_type="map_reduce", return_intermediate_steps=True, map_prompt=PROMPT, combine_prompt=PROMPT)
    
    # chain = load_summarize_chain(llm, chain_type="map_reduce", prompt=PROMPT)
    print("Summarizing...")
    with Timer(text="Summarizing took {:.2f} seconds"):
        result = chain({"input_documents": docs})['output_text']
    
    result = json.loads(result)
    overall_summary = result['summary']
    
    questions_answers_list = result['questions']
    
    # TODO: use the following code to get top 5 questions from map logic in intermediate steps
    # for qa in result['map_steps']:
    #     question = qa["questions"][0]['question']
    #     answer = qa["questions"][0]['answer']
    #     score = qa["questions"][0]['attractive_score']
    #     questions_answers_list.append({"question": question, "answer": answer, "score": score})
    
    top5_questions = sorted(questions_answers_list, key=lambda x: x['attractive_score'], reverse=True)[:5]
    
    _summary = f"Summary: {overall_summary}\nKey questions answered: \n" + "\n".join([f"{i+1}. {qa['question']}:\n {qa['answer']}" for i, qa in enumerate(top5_questions)])
    
    return _summary

    
def load_memory(transcribe):
    texts = []
    for d in transcribe:
        text = d['text']
        texts.append(text)
    
    docs = [Document(page_content=t) for t in texts]
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    
    db = FAISS.from_documents(docs, embeddings)
    return db


def run_chatbot(memory: FAISS, output_path: str):
    # 3. Q&A part (Chatbot)
    # - while loop, user can ask question
    # - find 20 most similar sentences to the question
    # - feed the sentences together with question to GPT-4 and get the answer asynchorously
    # - display the answer to the user    
    while True:
        user_input = input("Give me a question about this video: ")
        context = memory.similarity_search(user_input, k=5)
        qa_lists = []
        with Timer(text="Answering took {:.2f} seconds"):
            prompt=f"""Given the context:
            ```
                {context}\n
            ```
            , answer the question: 
            ```
                {user_input}\n
            ```
            Answer:"""
            message=[{"role": "user", "content": prompt}]
            answer = openai.ChatCompletion.create(
                model="gpt-4",
                messages=message,
                temperature=0.8,
                max_tokens=1000,
                n=1,
                stop=None,
                top_p=1,
                frequency_penalty=0,  # Penalizes new tokens based on their frequency
                presence_penalty=0,  # Penalizes new tokens based on their presence in the prompt
            )
            answer = str(answer.choices[0].message.content)
            # answer = llm.generate_text(prompt=question, context=_contexts[0].page_content, max_tokens=100, temperature=0.9)
            print("\nAnswer: ", str(answer))
            # ['choices'][0]['delta'].get('content', '')
            qa_lists.append({"question": user_input, "answer": answer})
            
            # append to result
            with open(output_path, "a") as f:
                f.write(str(qa_lists))


def run(video_url, output_path="result.json"):
    # 1. download youtube transcribe from the video url
    transcribe = download_transcribe(video_url)
    
    # 2. Summarization part
    summary = summarize(transcribe)
    print(summary)
    
    # Load each sentence of transcript into vector store
    memory = load_memory(transcribe)
    
    # 3. Q&A part (Chatbot)
    # Load each sentence of transcript into vector store
    # - while loop, user can ask question
    # - find 20 most similar sentences to the question
    # - feed the sentences together with question to GPT-4 and get the answer asynchorously
    # - display the answer to the user
    run_chatbot(memory, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--video_url', type=str, default="https://www.youtube.com/watch?v=6PRiAexITSs",
                        help='video url')
    parser.add_argument('--output_path', type=str, default="result.json",
                        help='output path')
    args = parser.parse_args()
    run(args.video_url, args.output_path)
    