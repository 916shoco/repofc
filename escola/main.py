import logging
import celular
import re
from utils import enviar_email, email_existe_no_banco_de_dados, gerar_codigo_recuperacao, atualizar_senha_no_banco_de_dados

class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[1;34m",  # Blue
        logging.INFO: "\033[1;32m",   # Green
        logging.WARNING: "\033[1;33m",# Yellow
        logging.ERROR: "\033[1;31m",  # Red
        logging.CRITICAL: "\033[1;41m\033[1;37m"  # White em red (critic)
    }
    RESET = "\033[0m"

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, self.RESET)
        message = super().format(record)
        return f"{log_color}{message}{self.RESET}"

# Basic config of logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# Add a console handler com a formatação colorida personalizada
console_handler = logging.StreamHandler()
console_handler.setFormatter(ColoredFormatter('%(message)s'))
logger.addHandler(console_handler)

def mostrar_mensagem(mensagem):
    logger.info("\033[1;32m" + mensagem + "\033[0m")

def verifica_email(email):
    if not email:
        raise ValueError("\033[1;31mNenhum e-mail fornecido\033[0m")
    
    if email.endswith("@gmail.com" or "@hotmail.com"):
        return True
    else:
        raise ValueError("\033[1;31mE-mail inválido\033[0m")

# def verifica_email(email): 
#     if not email:
#         raise ValueError("\033[1;31mNenhum e-mail fornecido\033[0m")
    
#     if re.match(r"^[^¹²³]*@gmail\.com$", email):
#         return True
#     else:
#         raise ValueError("\033[1;31mE-mail inválido\033[0m")


def cadastrar_novo_usuario():
    email = input("Digite seu email: ")
    senha = input("Digite sua senha: ")
    
    try:
        if verifica_email(email):
            celular.cadastrar_usuario(email, senha)
            mostrar_mensagem("\033[1;32mUsuário cadastrado com sucesso!\033[0m")
    except ValueError as e:
        logger.error(str(e))

def logar_usuario():
    email = input("Digite seu email: ")
    senha = input("Digite sua senha: ")
    usuario = celular.buscar_usuario(email)
    if usuario and usuario[1] == senha:
        mostrar_mensagem("\033[1;34mLogin realizado com sucesso!\033[0m")
    else:
        mostrar_mensagem("\033[1;31mEmail ou senha incorretos.\033[0m")

def recuperar_senha():
    email = input("Digite seu email: ")
    usuario = celular.buscar_usuario(email)
    if usuario:
        codigo = gerar_codigo_recuperacao()
        enviar_email(email, f"Seu código de verificação é: {codigo}")
        codigo_digitado = input("Digite o código de verificação enviado para seu email: ")
        if codigo_digitado == codigo:
            nova_senha = input("Digite sua nova senha: ")
            confirmacao_senha = input("Confirme sua nova senha: ")
            if nova_senha == confirmacao_senha:
                atualizar_senha_no_banco_de_dados(email, nova_senha)
                mostrar_mensagem("\033[1;34mSenha alterada com sucesso!\033[0m")
            else:
                mostrar_mensagem("\033[1;31mAs senhas não coincidem. Tente novamente.\033[0m")
        else:
            mostrar_mensagem("\033[1;31mCódigo incorreto. Tente novamente.\033[0m")
    else:
        mostrar_mensagem("\033[1;41m\033[1;37mEmail não cadastrado.\033[0m")

def main():
    celular.criar_tabela()
    
    while True:
        print("\n1 - Cadastrar novo usuário")
        print("2 - Login")
        print("3 - Recuperar senha")
        print("4 - Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            cadastrar_novo_usuario()
        elif opcao == '2':
            logar_usuario()
        elif opcao == '3':
            recuperar_senha()
        elif opcao == '4':
            break
        else:
            mostrar_mensagem("\033[1;31mOpção inválida.\033[0m")

if __name__ == "__main__":
    main()
