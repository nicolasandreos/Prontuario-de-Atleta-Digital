from spfcproject import app, database
from spfcproject.models import Usuario

# Executar esse codigo abaixo para criar um usuário
with app.app_context():
  database.create_all()
  print("Banco de Dados criado com sucesso!")
  temp_user = Usuario(username="Temp User", email="teste@empresa.com" , senha="12345")
  database.session.add(temp_user)
  database.session.commit()
  print("Usuário criado com sucesso!")
  print(f"Email: {temp_user.email}")
  print(f"Senha: {temp_user.senha}")
