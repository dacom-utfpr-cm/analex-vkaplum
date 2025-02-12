from myerror import MyError
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element
import xml.dom.minidom
import random
import sys
import string
from myerror import MyError

wspace_to_ascii = { 
    k : hex(ord(k)) for k in [' ', '\t', '\n', '\r', '\f', '\v'] 
}

class Lexer:
    def __init__(self, moore, quiet=False):
        self.moore = moore
        self.quiet = quiet
        self.line = 1
        self.column = 1

    def run(self, input_string, print_output=False):
        self.moore.reset()
        tokens = []

        i = 0
        entrada = input_string + " "
        while i < len(entrada):

            char = entrada[i]

            if char == "\n":
                self.line+=1
                self.column = 0

            if char not in self.moore.alfabeto_entrada:
                # print("ERRO! Caractere inválido: %s" % char)
                # sys.exit(1)
                e = MyError("LexerErrors")
                raise ValueError(e.newError(self.quiet, 
                                            'ERR-LEX-INV-CHAR', 
                                            line=self.line, 
                                            column=self.column,
                                            **{"" : char}))

            self.moore.transition(char)
            output = self.moore.get_output()

            if output:  # Token recognized
                if output != "COMMENT" and print_output:
                    print(output, end="\n")

                tokens.append(output)
                self.moore.reset()

                if self.moore.reprocess:
                    self.moore.reprocess = False
                    i-=1
                    self.column-=1
            i+=1
            self.column+=1

        return [t for t in tokens if t != "COMMENT"]    

class MooreMachine:
    def __init__(self, transitions, recover, output, initial_state="START"):
        self.initial_state = initial_state
        self.state = self.initial_state
        self.buffer = ""  # To store characters for identifiers
        self.transitions = transitions
        self.recover = recover
        self.output = output
        self.reprocess = False
        self.alfabeto_entrada = self.coletar_alfabeto()
        #print(self.alfabeto_entrada)

    def __str__(self):
        saida = "\nMáquina de Moore\n"
        saida += "Estados: " + str(len(sorted(list(self.coletar_estados())))) + "\n"
        saida += "Alfabeto de entrada: " + str(sorted(self.coletar_alfabeto())) + "\n"
        saida += "Alfabeto de saída: " + str(sorted(self.output.values())) + "\n"
        saida += "Transições: " + str(self.contar_transicoes()) + "\n"
        saida += "Estado Inicial: " + self.initial_state + "\n"
        saida += "Tabela de saída: " + str(self.output) + "\n"
        return saida

    def coletar_alfabeto(self):
        alfabeto = set()
        # Get all second-level keys
        for _, dic_interno in self.transitions.items():
            if isinstance(dic_interno, dict):
                alfabeto.update(dic_interno.keys())
        return alfabeto
    
    def coletar_estados(self):
        estados = set()
        for _, dic_interno in self.transitions.items():
            estados.update(dic_interno.values())
        for estado_rec in self.recover.values():
            estados.add(estado_rec)
        return estados
    
    def contar_transicoes(self):
        n_transicoes = 0
        for _, transicoes in self.transitions.items():
            for _, _ in transicoes.items():
                n_transicoes+=1
        for _, _ in self.recover.items():
            n_transicoes+=1
        return n_transicoes
        
    def transition(self, char):
        self.buffer += char
        try:
            self.state = self.transitions[self.state][char]
        except KeyError:
            #print("Transição não encontrada: (%s,%s)" % (self.state, char))
            try:
                self.state = self.recover[self.state]
                self.reprocess = True
            except KeyError:
                print("Não foi possível recuperar a transição a partir do estado %s" % (self.state))
                sys.exit(1)
                
    def get_output(self):
        try:
            return self.output[self.state]
        except KeyError:
            return None

    def reset(self):
        self.state = self.initial_state
        self.buffer = ""

    def to_jff(self, nome_arquivo, estado_inicial="START", machine_type="moore"):
        estados = self.coletar_estados()
        estados = { s : i for i, s in enumerate(estados) }
        #print(len(estados))
        n_transicoes = 0
        
        root = Element("structure")
        typetag = ET.SubElement(root, "type")
        typetag.text = machine_type

        automaton = ET.SubElement(root, "automaton")
        for estado in estados.keys():
            stateattrib = { 
                "id" : str(estados[estado]), 
                "name" : estado
            }
            statetag = ET.SubElement(automaton, "state", stateattrib)
            xtag = ET.SubElement(statetag, "x")
            xtag.text = str(random.randint(1, 10) * 100)
            ytag = ET.SubElement(statetag, "y")
            ytag.text = str(random.randint(1, 10) * 100)

            if estado == estado_inicial:
                ET.SubElement(statetag, "initial")
                xtag.text = str(0)
                ytag.text = str(0)

            if machine_type == "moore":
                if estado in self.output:
                    output_tag = ET.SubElement(statetag, "output")
                    output_tag.text = str(self.output[estado])
                    
        for estado_from, transicoes in self.transitions.items():
            simbolos = set(transicoes.keys())
            merged_symbols = set()

            #"juntar" grande número de transições em uma única transição 
            for charset, groupname in [
                (string.ascii_lowercase, "alpha"),
                ( [ str(i) for i in range(10)], "num"),
                ( [' ', '\t', '\n', '\r', '\f', '\v'] , "whitespace")
            ]:
                if simbolos.intersection(charset) == set(charset):
                    charset_transitions = {}
                    for k in charset:
                        to = transicoes[k]
                        if to not in charset_transitions:
                            charset_transitions[to] = []
                        charset_transitions[to].append(k)
                    charset_transitions_count = [ (k, len(v)) for k, v in charset_transitions.items() ]
                    charset_transitions_count = sorted(charset_transitions_count, key=lambda x: x[1], reverse=True)
                    most_charset_trans = set(charset_transitions[charset_transitions_count[0][0]])
                    least_charset_trans = set(charset).difference(most_charset_trans)
                    
                    n_transicoes+=len(most_charset_trans)

                    trans = ET.SubElement(automaton, "transition")
                    fromtag = ET.SubElement(trans, "from")
                    fromtag.text = str(estados[estado_from])
                    totag = ET.SubElement(trans, "to")
                    totag.text = str(estados[charset_transitions_count[0][0]])
                    readtag = ET.SubElement(trans, "read")
                    if len(least_charset_trans) > 0:
                        readtag.text = str("{%s}-{%s}" % (groupname, ",".join(sorted(least_charset_trans))))
                    else:
                        readtag.text = str("{%s}" % (groupname))
                
                    if(charset_transitions_count[0][0] in self.output):
                        transouttag = ET.SubElement(trans, "transout")
                        transouttag.text = self.output[charset_transitions_count[0][0]]
                    
                    merged_symbols.update(most_charset_trans)

            for simbolo, estado_to in transicoes.items():
                if simbolo not in merged_symbols:
                    n_transicoes+=1
                    trans = ET.SubElement(automaton, "transition")
                    fromtag = ET.SubElement(trans, "from")
                    fromtag.text = str(estados[estado_from])
                    totag = ET.SubElement(trans, "to")
                    totag.text = str(estados[estado_to])
                    readtag = ET.SubElement(trans, "read")
                    if simbolo in wspace_to_ascii:
                        readtag.text = wspace_to_ascii[simbolo]
                    else:
                        readtag.text = str(simbolo)

                    if(estado_to in self.output):
                        transouttag = ET.SubElement(trans, "transout")
                        transouttag.text = self.output[estado_to]                        
                        
        for estado_from, estado_recuperacao in self.recover.items():
            n_transicoes+=1
            trans = ET.SubElement(automaton, "transition")
            fromtag = ET.SubElement(trans, "from")
            fromtag.text = str(estados[estado_from])
            totag = ET.SubElement(trans, "to")
            totag.text = str(estados[estado_recuperacao])
            readtag = ET.SubElement(trans, "read")
            readtag.text = "[qualquer]"

            if(estado_recuperacao in self.output):
                transouttag = ET.SubElement(trans, "transout")
                transouttag.text = self.output[estado_recuperacao]     

        #print(n_transicoes)

        # jff = ET.ElementTree(root)
        xml_str = ET.tostring(root, encoding="unicode")
        pretty_xml = xml.dom.minidom.parseString(xml_str)
        pretty_xml = pretty_xml.toprettyxml(indent="  ")

        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(pretty_xml)

if __name__ == "__main__":
    input_string = "<<= i if < <= else() else item elsewhere ifem< e8 _8"
    #input_string = "if (i ) if(i) if ( i ) if( i) z()"
    #input_string = "())(<<="
    #input_string = "("
    #input_string = "+ < ++<=<  <+- --* *   * / / // / "
    #input_string = "[] [i] {[()]} {} { { } }} if (i) { }"
    #input_string = "= == <== a = b == <="
    #input_string = "int x(int a, int b) { a = b; };;;"
    #input_string = "a < b; a <=b; b >a; b>=a-b;"
    #input_string = "!!!=!if(!a != b) { a = b; }"
    #input_string = "if((a > b) || (b>c)) { d = c; }"
    #input_string = "1 1000 01 f(1,2,3,10) a10 b20 2a"
    #input_string = "i in int integer inte"
    #input_string = "f fl flo floa float floating floate"
    #input_string = "r re ret retu retur return returni retorna rei reto retun returo"
    #input_string = "v vi vo vod voi voix void voide avoid"
    #input_string = "w wi wh whl whi whio whil whilp while whilex0 while1"
    #input_string = "w wi wh whl whi whio whil whilp while whilex0 while1_ while_"
    #input_string = "if(/* a + b */a>b) { a = b; }"
    input_string = "&&"
#     input_string = """
# int gcd (int u, int v){
#   if (v == 0) return u;
#   else return gcd(v,u-u/v*v);
#   /* u-u/v*v == u mod v */
# }
# """

#     input_string = """
# int a;
# int b[10];

# int input(void){
#   return;
# }"""

    from cm_moore import moore_recover, moore_transitions, moore_output

    moore = MooreMachine(moore_transitions, moore_recover, moore_output)
    lexer = Lexer(moore)

    print("Input: %s" % (input_string))
    tokens = lexer.run(input_string)
    tokens = [t for t in tokens if t != "COMMENT"]

    for t in tokens:
        print (t)

    #l = eval(str(sorted(list(moore.coletar_alfabeto()))))
    #print(l)

    moore.to_jff("cm_moore.jff", "START", "moore")

