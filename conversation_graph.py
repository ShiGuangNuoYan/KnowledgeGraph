# -*- coding: gbk -*-
import ahocorasick
import os
class QuestionClassifier():
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #特征词路径
        self.poem_path=os.path.join(cur_dir,'dictionary/poem.txt')
        self.dynasty_path=os.path.join(cur_dir,'dictionary/dynasty.txt')
        self.category_path=os.path.join(cur_dir,'dictionary/category.txt')
        self.author_path=os.path.join(cur_dir,'dictionary/author.txt')

        #加载特征词
        self.poem_wds=[i.strip() for i in open(self.poem_path,encoding="gbk") if i.strip()]
        self.dynasty_wds=[i.strip() for i in open(self.dynasty_path,encoding="gbk") if i.strip()]
        self.category_wds=[i.strip() for i in open(self.category_path,encoding="gbk") if i.strip()]
        self.author_wds=[i.strip() for i in open(self.author_path,encoding="gbk") if i.strip()]
        self.field_words=set(self.poem_wds+self.dynasty_wds+self.category_wds+self.author_wds)
        #构建领域actree,可以将文本流输入自动机，自动机会在文本中寻找所有预先定义的关键词，并且能够告诉你每个关键词的出现位置。这种方法比逐一查找每个关键词要高效得多，特别是在关键词集合很大或文本很长的情况下。
        self.field_tree=self.build_actree(list(self.field_words))
        #构建词典
        self.wdtype_dict=self.build_wdtype_dict()
        #问句疑问句
        self.author_qwd=['作者','谁写的','诗人','词人','出自谁笔']
        self.dynasty_qwd=['朝代','年代','哪个时期']
        self.content_qwd=['内容是什么','怎么写的','咋写的','怎么背','请你背写','默写','补全']
        self.category_qwd=['体裁','形式']
        self.appreciation_qwd=['赏析','鉴赏','品鉴','分析','解析','意义','目的是']
        self.background_qwd=['历史背景','创作背景','背景是','历史环境','当时','那时','写作缘由','写作原因']
        self.trans_qwd=['翻译','这首诗的解释','通俗','释义','人话','解释']
        self.annotation_qwd=['注释','关键知识点','常见词语','知识点']
        #print('model init finished ......')
        return

    #分类主函数
    def classify(self,question):
        data={}
        poem_dict=self.check_poems(question)#过滤一下问题
        if not poem_dict:#如果为空
            return {}
        data['args']=poem_dict
        #收集问题当中的实体类型
        types=[]
        for type_ in poem_dict.values():
            types+=type_
        question_type='others'#无意义
        question_types=[]

        if self.check_words(self.author_qwd,question) and ('poem' in types):#这首诗的作者是谁
            question_type='poem_author'
            question_types.append(question_type)

        if self.check_words(self.dynasty_qwd,question) and 'poem' in types:#这首诗的朝代是什么
            question_type='poem_dynasty'
            question_types.append(question_type)

        if self.check_words(self.dynasty_qwd,question) and 'author' in types:#作者朝代是什么
            question_type='author_dynasty'
            question_types.append(question_type)

        if self.check_words(self.content_qwd,question) and 'poem' in types:#这首诗的内容是什么?
            question_type='poem_content'
            question_types.append(question_type)

        if self.check_words(self.category_qwd,question) and 'poem' in types:#这首诗的体裁是什么
            question_type='poem_category'
            question_types.append(question_type)

        if self.check_words(self.trans_qwd,question) and 'poem' in types:#这首诗的翻译是什么
            question_type='poem_trans'
            question_types.append(question_type)

        if self.check_words(self.annotation_qwd,question) and 'poem' in types:#这首诗的常见注释是什么
            question_type='poem_annotation'
            question_types.append(question_type)

        if self.check_words(self.appreciation_qwd,question): #鉴赏是什么
            question_type='appreciation'
            question_types.append(question_type)

        if self.check_words(self.background_qwd,question): #背景是什么
            question_type='background'
            question_types.append(question_type)

        data['question_types']=question_types

        return data

    #构建actree加速过滤
    def build_actree(self,wordlist):
        actree=ahocorasick.Automaton()
        for index,word in enumerate(wordlist):
            actree.add_word(word,(index,word))
        actree.make_automaton()
        return actree

    def build_wdtype_dict(self):#构造词类型
        wd_dict=dict()
        for wd in self.field_words:#找到用户输入的词是什么范围的
            wd_dict[wd]=[]
            if wd in self.poem_wds:
                wd_dict[wd].append('poem')
            if wd in self.author_wds:
                wd_dict[wd].append('author')
            if wd in self.dynasty_wds:
                wd_dict[wd].append('dynasty')
            if wd in self.category_wds:
                wd_dict[wd].append('category')
        return wd_dict

    #问句过滤
    def check_poems(self,question):
        field_wds=[]
        for i in self.field_tree.iter(question):# ahocorasick库 匹配问题  iter返回一个元组，i的形式如(3, (23192, '杜甫'))
            wd=i[1][1]#匹配到的词
            field_wds.append(wd)
        stop_wds=[]
        for wd1 in field_wds:
            for wd2 in field_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1) #stopword取重复且较短的词语
        final_wds = [i for i in field_wds if i not in stop_wds]  # final_wds取长词,也就是最后返回的是长词
        final_dict= {i:self.wdtype_dict.get(i) for i in final_wds}#来自于构造词典，# 获取词和词所对应的实体类型
        return final_dict

    #基于特征词进行分类
    def check_words(self,wds,sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler=QuestionClassifier()
    while True:
        question=input('请输入您的问题:')
        data = handler.classify(question)
        print(data)
