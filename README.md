# chat_video_clone_py
Python App to summarize and Q&amp;A for video content given URL

Example:

```
✗ python summarize_utils.py --video_url https://www.youtube.com/watch\?v\=_L39rN6gz7Y
Downloading transcript took 0.99 seconds
docs lengtb 2
input_variables=['text'] output_parser=None partial_variables={} template='Please write a summary and top 3 questions you think most attractive to public audiance of the following text:\n    ```\n    {text}\n    ```\n    requirements:\n    - use whatever language the text is in\n    - less than 5 sentences\n    - use fact from the text only\n    - no opinion\n    - the 3 questions should have attractive_score 0-10 to identify how attractive the question is\n    - output in json format with keys: summary, questions, each question has keys: question, answer, attractive_score\n    ' template_format='f-string' validate_template=True
Summarizing...
Summarizing took 176.27 seconds
Summary: The text explains decision trees, specifically classification trees, and their construction using raw data. It highlights the use of genie impurity to quantify differences between features and addresses overfitting and impure leaves through pruning and limiting tree growth, with cross-validation for testing different values.
Key questions answered: 
1. What is the purpose of genie impurity in decision trees?:
 Genie impurity quantifies the impurity of leaves in a decision tree, helping to decide which feature should be at the top of the tree.
2. What are two methods to address overfitting and impure leaves in classification trees?:
 Pruning and limiting tree growth.
3. What technique is suggested for testing different values in tree growth limitations?:
 Cross-validation.
 
# Q&A
Give me a question about this video: 
Give me a question about this video: what's the advantage of using genie impurity in decition tree?
Answer:  The provided context does not give information about the advantages of using genie impurity in decision trees.
Answering took 4.44 seconds

Give me a question about this video: 
what's the advantage of using genie impurity in decition tree? if not show in the content, can you still tell?
Answer:  The content provided does not explicitly mention the advantages of using genie impurity in decision trees. However, I can still tell you that genie impurity is a measure used to determine the best split in decision trees by evaluating the purity of a node. The lower the genie impurity, the better the split. It helps to create more accurate and efficient decision trees.
Answering took 30.99 seconds
```
