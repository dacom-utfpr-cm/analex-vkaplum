[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/6ZHtfd4V)
# template-projeto-analex-bcc5003
Este repositório contém o código inicial de referência para o desenvolvimento da fase de Análise Léxica do Projeto do Compilador para a linguagem C-.

# Análise Léxica

A __Análise Léxica__ é a fase do compilador que lê o código-fonte do arquivo de entrada como um fluxo de caracteres, e nesse processo de varredura reconhece os _tokens_ ou marcas da linguagem. As denominações Sistema de Varredura, Analisador Léxico e _Scanner_ são equivalentes.

Devem ser reconhecidas as marcas presentes na linguagem `C-`, como `if`, `else`, `while`, que são palavras chave da linguagem ou palavras reservadas. Precisam ser reconhecidos os nomes de variáveis e funções que são os _identificadores_, símbolos e operadores aritméticos, lógicos e relacionais.

O processo de reconhecimento das marcas, a identificação de padrões pode ser feito de duas formas: utilizando-se __expressões regulares__ ou implementando o analisador com a teoria de __autômatos finitos__.

Neste projeto serão utilizados autômatos para o reconhecimentos das marcas.

Para um código simples em `C-` igual o Código 1.

```c
int main(void){
  return(0);
}
```
_Código 1: Programa em C-_


A lista de marcas que precisam ser identificadas é:
```
INT
ID
LPAREN
VOID
RPAREN
LBRACE
RETURN
LPAREN
NUMBER
RPAREN
SEMICOLON
RBRACE
```

## Preparação do Ambiente

Para a implementação da fase de __Análise Léxica__ é necessário instalar ferramentas, como o `pytest` e a biblioteca para implementação do autômato. Os pré-requisitos podem ser instalados utilizando o arquivo de `requirements.txt`.

```bash
$ pip install  -r requirements.txt
```

```bash
$ cat requirements.txt
pytest
```

Se em seu sistema operacional não for possível instalar a biblioteca `automata_python` crie um ambiente para isolar.

```bash
$ python -m venv automata
$ source automata/bin/activate
```

## Execução de Testes

No projeto está sendo disponibilizado arquivos de exemplos em `C-` para testes. Os testes estão no diretório `tests` do raiz do projeto.

Para executar um teste em específico a implementação do analisador léxico `analex.py` pode ser chamada, o parâmetro `-k` pode ser utilizado para que somente _tokens_ e _chaves de erros_ sejam impressas.

```bash
$ python analex.py prog-002.cm -k
INT
ID
LPAREN
VOID
RPAREN
LBRACE
RETURN
LPAREN
NUMBER
RPAREN
SEMICOLON
RBRACE
```

Todos os testes podem ser executados via `pytest`.

```
PS C:\Users\vanes\Desktop\UTFPR_CC\2024.2\Teoria da Computacao\Trabalho_01\analex-vkaplum> python -m pytest
============================================================================ test session starts ============================================================================
platform win32 -- Python 3.13.2, pytest-8.3.4, pluggy-1.5.0
rootdir: C:\Users\vanes\Desktop\UTFPR_CC\2024.2\Teoria da Computacao\Trabalho_01\analex-vkaplum
configfile: pytest.ini
collected 11 items                                                                                                                                                           

analex_test.py ...........                                                                                                                                             [100%]

============================================================================ 11 passed in 2.04s =============================================================================

```

## Leitura Recomendada

1. __Capítulo 2:__ _Varredura_

    LOUDEN, Kenneth C. Compiladores: princípios e práticas. São Paulo, SP: Thomson, c2004. xiv, 569 p. ISBN 8522104220.

2. __Capítulo 3:__ _Análise Léxica_

    AHO, Alfred V. et al. Compiladores: princípios, técnicas e ferramentas. 2. ed. São Paulo, SP: Pearson Addison-Wesley, 2008. x, 634 p. ISBN 9788588639249.