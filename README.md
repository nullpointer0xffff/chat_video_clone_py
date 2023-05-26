# chat_video_clone_py
Python App to summarize and Q&amp;A for video content given URL

Example:

```
(chatvideo) ➜  chat_video_clone_py git:(main) ✗ python app.py        
Loading local transcript took 0.00 seconds
docs lengtb 1
input_variables=['text'] output_parser=None partial_variables={} template='Please write a summary and top 3 questions you think most attractive to public audiance of the following text:\n    ```\n    {text}\n    ```\n    requirements:\n    - less than 5 sentences\n    - use fact from the text only\n    - no opinion\n    - the 3 questions should have attractive_score 0-10 to identify how attractive the question is\n    - output in json format with keys: summary, questions, each question has keys: question, answer, attractive_score\n    ' template_format='f-string' validate_template=True
Summarizing...
Summarizing took 135.31 seconds
Summary: Microsoft is integrating Chat GPT with Bing for improved search experience and introducing interoperability for plugins. Microsoft 365 Copilot will assist users in drafting legal contracts efficiently using plugins like Thompson Reuters. AI Studio is being developed for AI safety, and Microsoft Fabric, a unified data analytics platform, will store and manage data in an open format.
Key questions answered: 
1. What is Microsoft Fabric?:
 Microsoft Fabric is a unified data analytics platform that stores and manages data in an open format, providing a single architecture and experience for data professionals.
2. How is Microsoft integrating Chat GPT and Bing?:
 Microsoft is integrating Chat GPT and Bing by making Bing the default search experience in Chat GPT, providing higher quality and more timely answers.
3. What is the purpose of Microsoft 365 Copilot?:
 Microsoft 365 Copilot aims to help users be more productive at work, such as drafting legal contracts more efficiently with the help of powerful plugins like Thompson Reuters.
Give me a question about this video: What is Microsoft Fabric?

Answer:  Microsoft Fabric is a unified framework for designing and developing user interfaces across various Microsoft platforms and devices.
Answering took 4.90 seconds
Give me a question about this video: ......
```