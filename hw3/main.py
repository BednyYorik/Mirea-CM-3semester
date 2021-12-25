from sly import Lexer, Parser


class ConfLexer(Lexer):
    tokens = {'STRING', 'DOT2', 'LSQR', 'RSQR', 'INT', 'COMMA', 'LFIG', 'RFIG'}

    ignore_comments = r'#.*'
    ignore_spaces = r'\ '
    ignore_newline = r'\n'
    STRING = r'\".*\"'
    DOT2 = r'\:'
    LSQR = r'\['
    RSQR = r'\]'
    LFIG = r'\{'
    RFIG = r'\}'
    INT = r'\d+'
    COMMA = r'\,'


class ConfParser(Parser):
    tokens = ConfLexer.tokens

    @_('s_exp_list')
    def program(self, p):
        return str(p.s_exp_list)

    @_('s_exp COMMA s_exp_list')
    def s_exp_list(self, p):
        return str(p.s_exp) + ',\n' + str(p.s_exp_list)

    @_('s_exp')
    def s_exp_list(self, p):
        return str(p.s_exp)

    @_('LFIG s_exp_list RFIG')
    def s_exp(self, p):
        ans = '{\n' + str(p.s_exp_list) + '\n}'

        return ans

    @_('var')
    def s_exp(self, p):
        return str(p.var)

    @_('STRING')
    def s_exp(self, p):
        return str(p.STRING)

    @_('INT')
    def s_exp(self, p):
        return str(p.INT)

    @_('STRING DOT2 info')
    def var(self, p):
        return str(p.STRING) + ':' + str(p.info)

    @_('STRING')
    def info(self, p):
        return str(p.STRING)

    @_('INT')
    def info(self, p):
        return str(p.INT)

    @_('LSQR arr_comp_list RSQR')
    def info(self, p):
        ans = '[\n' + str(p.arr_comp_list) + '\n]'

        return ans

    @_('arr_comp COMMA arr_comp_list')
    def arr_comp_list(self, p):
        return str(p.arr_comp) + ',\n' + str(p.arr_comp_list)

    @_('arr_comp')
    def arr_comp_list(self, p):
        return str(p.arr_comp)

    @_('STRING')
    def arr_comp(self, p):
        return str(p.STRING)

    @_('INT')
    def arr_comp(self, p):
        return str(p.INT)

    @_('s_exp')
    def arr_comp(self, p):
        return str(p.s_exp)


inp_file = open('test.conf', 'r', encoding='UTF-8')
text = inp_file.read()

lexer = ConfLexer()
parser = ConfParser()
out = parser.parse(lexer.tokenize(text))
#  print(out)

out_file = open('out.json', 'w')
out_file.write(out)

inp_file.close()
out_file.close()
