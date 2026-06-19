
from catalog import Catalog
from photo import Photo


p1 = Photo(1, 1, "/home/user/Pictures/1.jpg", ["natureza", "natureza2"], 5)
p2 = Photo(2, 2, "/home/user/Pictures/2.jpg", ["natureza", "natureza2"], 4)
p3 = Photo(3, 3, "/home/user/Pictures/3.jpg", ["natureza", "natureza2"], 3)
p4 = Photo(4, 4, "/home/user/Pictures/4.jpg", ["natureza", "natureza2"], 2)

fotolog = Catalog(p3)

def run():
    fotolog.registerCommands()
    while fotolog.running:
        user_input = input("fotolog> ").lower()
        user_input = user_input.split()
        
        aux = None
        for command in fotolog.commands:
            if user_input[0] == command["command"]:
                aux = True
                # para verificar se o comando precisa de um argumento ou não, e chamar a função correspondente
                if len(user_input) == 1:
                    command["function"]()
                
                if len(user_input) == 2:
                    if command["input_type"] == str:
                        command["function"](user_input[1])
                    elif command["input_type"] == int:
                        command["function"](int(user_input[1]))
                        
                if len(user_input) >= 3:
                    if command["input_type"] == str:
                        command["function"](user_input[1:])
                    elif command["input_type"] == int:
                        command["function"](int(user_input[1]))

        if not aux:
            if user_input[0][0] != ':':
                print("Comandos se iniciam com ':'. Digite ':help' para ver os comandos disponíveis.")
            else:
                print("Comando não reconhecido. Digite ':help' para ver os comandos disponíveis.")

if __name__ == "__main__":
    run()