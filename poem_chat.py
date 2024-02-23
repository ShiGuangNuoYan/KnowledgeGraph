# -*- coding: gbk -*-
from question_parser import *
from conversation_graph import *
from answer_search import *

class ChatPoemGraph:
    def __init__(self):
        self.classifier=QuestionClassifier()
        self.parser=QuestionParser()
        self.seacher=AnswerSearcher()

    def chat_main(self,sent):
        answer='很抱歉没能理解你的问题，您也许可以换个问法再问一次'
        res_classify=self.classifier.classify(sent)#对问题进行分类

        if not res_classify:#如果没有找到合适的分类就返回初始answer
            return answer
        res_sql=self.parser.parser_main(res_classify)
        final_answers=self.seacher.search_main(res_sql)
        if not final_answers: #最终未找到合适的答案
            return answer
        else:
            return '\n'.join(final_answers)
if __name__ == '__main__':
    handler=ChatPoemGraph()
    while True:
        question=input('请输入您的问题:')
        answer=handler.chat_main(question)
        print('小星的回答:',answer)

