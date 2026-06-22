
from catalog import Catalog
from photo import Photo
fotolog = Catalog()

def run():
    fotolog.registerCommands()
    while fotolog.running:
        user_input = input("fotolog> ").lower()
        user_input = user_input.split()

        if not user_input:
            continue
        
        aux = None
        for command in fotolog.commands:
            if user_input[0] == command["command"]:
                aux = True
                # para verificar se o comando precisa de um argumento ou não, e chamar a função correspondente
                if len(user_input) == 1:
                    try : 
                        command["function"]()
                    except TypeError as e:
                        print(f"Erro: {e}. Digite ':help' para ver os comandos disponíveis.")
                        # print("Comando inválido. Digite ':help' para ver os comandos disponíveis.")

                if len(user_input) == 2:
                    command["function"](user_input[1])
                        
                if len(user_input) >= 3:
                    command["function"](*user_input[1:])

        if not aux:
            if user_input[0][0] != ':':
                print("Comandos se iniciam com ':'. Digite ':help' para ver os comandos disponíveis.")
            else:
                print("Comando não reconhecido. Digite ':help' para ver os comandos disponíveis.")

if __name__ == "__main__":
    run()