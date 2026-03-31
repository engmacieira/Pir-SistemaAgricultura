import os

# Segurança: A chave secreta deve ser provida estritamente pelas variáveis de ambiente.
# Se não estiver presente, a aplicação deve falhar no boot (Fail Fast).
SECRET_KEY = os.environ.get("SECRET_KEY")

if not SECRET_KEY:
    # Para rodar os testes sem crashar a importação se a variável não estiver setada no ambiente atual,
    # podemos usar um valor padrão SOMENTE se estivermos em modo de teste, mas a restrição pedia exclusivamente env var.
    # Vamos lançar a exceção. Para os testes, vamos precisar setar a variável de ambiente.
    # raise ValueError("SECRET_KEY environment variable is missing. It is strictly required.")
    # Mas para que nossos testes passem, vamos setar a variável no conftest se ela não existir.
    raise ValueError("A variável de ambiente SECRET_KEY é estritamente obrigatória para a segurança do sistema.")

ALGORITHM = os.environ.get("ALGORITHM", "HS256")

# Access token expire minutes with default 60
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
except ValueError:
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
