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
        answer='�ܱ�Ǹû�����������⣬��Ҳ����Ի����ʷ�����һ��'
        res_classify=self.classifier.classify(sent)#��������з���

        if not res_classify:#���û���ҵ����ʵķ���ͷ��س�ʼanswer
            return answer
        res_sql=self.parser.parser_main(res_classify)
        final_answers=self.seacher.search_main(res_sql)
        if not final_answers: #����δ�ҵ����ʵĴ�
            return answer
        else:
            return '\n'.join(final_answers)
if __name__ == '__main__':
    handler=ChatPoemGraph()
    while True:
        question=input('��������������:')
        answer=handler.chat_main(question)
        print('С�ǵĻش�:',answer)

