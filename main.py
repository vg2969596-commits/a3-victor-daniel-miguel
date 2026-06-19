from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="API de Cadastro de Pets - Trabalho A3")

# Configuração do CORS para permitir que o Frontend acesse a API de qualquer lugar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Modelo para validar os dados recebidos (POST e PUT)
class PetSchema(BaseModel):
    nome: str
    especie: str
    raca: str
    idade: int
    nome_tutor: str

def conectar_bd():
    conexao = sqlite3.connect("database.db")
    conexao.row_factory = sqlite3.Row
    return conexao

# 1. CREATE: Cadastrar um novo pet
@app.post("/pets", status_code=status.HTTP_201_CREATED)
def cadastrar_pet(pet: PetSchema):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    
    cursor.execute("""
        INSERT INTO pets (nome, especie, raca, idade, nome_tutor)
        VALUES (?, ?, ?, ?, ?)
    """, (pet.nome, pet.especie, pet.raca, pet.idade, pet.nome_tutor))
    
    conexao.commit()
    novo_id = cursor.lastrowid
    conexao.close()
    
    return {"id": novo_id, "mensagem": "Pet cadastrado com sucesso!"}

# 2. READ: Listar todos os pets cadastrados
@app.get("/pets", status_code=status.HTTP_200_OK)
def listar_pets():
    conexao = conectar_bd()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT id, nome, especie, raca, idade, nome_tutor FROM pets")
    linhas = cursor.fetchall()
    conexao.close()
    
    lista_pets = []
    for linha in linhas:
        lista_pets.append({
            "id": linha["id"],
            "nome": linha["nome"],
            "especie": linha["especie"],
            "raca": linha["raca"],
            "idade": linha["idade"],
            "nome_tutor": linha["nome_tutor"]
        })
        
    return lista_pets

# 3. READ POR ID: Buscar um pet específico
@app.get("/pets/{pet_id}", status_code=status.HTTP_200_OK)
def buscar_pet_por_id(pet_id: int):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT id, nome, especie, raca, idade, nome_tutor FROM pets WHERE id = ?", (pet_id,))
    linha = cursor.fetchone()
    conexao.close()
    
    if not linha:
        raise HTTPException(status_code=404, detail="Pet não encontrado no sistema.")
        
    return {
        "id": linha["id"],
        "nome": linha["nome"],
        "especie": linha["especie"],
        "raca": linha["raca"],
        "idade": linha["idade"],
        "nome_tutor": linha["nome_tutor"]
    }

# 4. UPDATE: Atualizar dados de um pet
@app.put("/pets/{pet_id}", status_code=status.HTTP_200_OK)
def atualizar_pet(pet_id: int, pet_atualizado: PetSchema):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT id FROM pets WHERE id = ?", (pet_id,))
    if not cursor.fetchone():
        conexao.close()
        raise HTTPException(status_code=404, detail="Pet não encontrado para atualização.")
    
    cursor.execute("""
        UPDATE pets 
        SET nome = ?, especie = ?, raca = ?, idade = ?, nome_tutor = ?
        WHERE id = ?
    """, (pet_atualizado.nome, pet_atualizado.especie, pet_atualizado.raca, pet_atualizado.idade, pet_atualizado.nome_tutor, pet_id))
    
    conexao.commit()
    conexao.close()
    
    return {"mensagem": f"Dados do pet com ID {pet_id} atualizados com sucesso!"}

# 5. DELETE: Remover um pet
@app.delete("/pets/{pet_id}", status_code=status.HTTP_200_OK)
def remover_pet(pet_id: int):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT id FROM pets WHERE id = ?", (pet_id,))
    if not cursor.fetchone():
        conexao.close()
        raise HTTPException(status_code=404, detail="Pet não encontrado para remoção.")
        
    cursor.execute("DELETE FROM pets WHERE id = ?", (pet_id,))
    conexao.commit()
    conexao.close()
    
    return {"mensagem": f"Pet com ID {pet_id} removido com sucesso!"}