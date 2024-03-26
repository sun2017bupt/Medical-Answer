from question_classifier import *
from question_parser import *
from answer_search import *

from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，我是阿枫医药智能助理，希望可以帮到您。如果没答上来，可联系sun2017@bupt.edu.cn。祝您身体棒棒！'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # 解析URL和参数
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # 构建会话机器人
        handler = ChatBotGraph()
        # 检查是否存在名为 "input" 的参数
        if 'input' in query_params:
            # 获取输入字符串
            user_input = query_params['input'][0]
            
            # while 1:
            question = user_input # 前端传来的问题
            answer = handler.chat_main(question)
            
            # 设置HTTP响应头
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin','*')
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            
            # 发送倒序后的字符串作为响应
            self.wfile.write(answer.encode('utf-8'))
        else:
            # 如果未提供输入字符串参数，则返回错误响应
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("缺少输入参数 'input'".encode('utf-8'))

def run_server():
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, MyHandler)
    print('服务器正在运行...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()

