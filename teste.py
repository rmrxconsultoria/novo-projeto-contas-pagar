import os
import pyodbc

db_path = r"\\10.1.8.253\dados\Financeiro\BancoDados\BancoDDA.accdb"

if not os.path.exists(db_path):
    raise FileNotFoundError(f"O banco de dados não foi encontrado no caminho especificado: {db_path}")  

else:
    print("O banco de dados foi encontrado com sucesso.")
    
    
print(pyodbc.drivers())