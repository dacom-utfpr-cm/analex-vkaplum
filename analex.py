import sys, os

from myerror import MyError

error_handler = MyError('LexerErrors')

global check_cm
global check_key

def main():
    check_cm = False
    check_key = False
    idx_cm = 1
    # python analex.py file.cm

    numargs = len(sys.argv)
    if "-k" in sys.argv:
        numargs-=1
        check_key = True

    if(numargs < 2):
        raise TypeError(error_handler.newError(check_key, 'ERR-LEX-USE'))
    
    arq_fonte = sys.argv[1]
    if arq_fonte.split(".")[-1] == "cm":
        check_cm = True

    if not check_cm:
        raise IOError(error_handler.newError(check_key, 'ERR-LEX-NOT-CM'))  

    if not os.path.exists(sys.argv[idx_cm]):
        raise IOError(error_handler.newError(check_key, 'ERR-LEX-FILE-NOT-EXISTS'))  

    from lexer import Lexer, MooreMachine
    from cm_moore import moore_transitions, moore_recover, moore_output

    moore = MooreMachine(moore_transitions, moore_recover, moore_output)
    cmlexer = Lexer(moore, quiet=check_key)

    data = open(sys.argv[idx_cm])
    source_file = data.read()

    if not check_key:
        print("Definição da Máquina")
        print(moore)
        print("Entrada:")
        print(source_file)
        print("Lista de Tokens:")
    
    _ = cmlexer.run(source_file, print_output=True)
    

if __name__ == "__main__":

    try:
        main()
    except (ValueError, TypeError, IOError) as e:
        print(e)