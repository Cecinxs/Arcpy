#CRIANDO PORCENTAGEM AUTOMATIZADA

import arcpy

# Defina a tabela ou feature class
tabela = r"caminho.gdb\suatabela" #sempre que definir o dado diretamente, coloque "r" na frente. 

# Lista das colunas originais
colunas_originais = ["Col1", "Col2", "Col3", "Col4", "Col5"]

# Criar nomes para as novas colunas de porcentagem
colunas_porcentagem = [f"{col}_pct" for col in colunas_originais]

# Adicionar as novas colunas se ainda não existirem (sempre bom verificar, principalmente quando é bigdata)
for col in colunas_porcentagem:
    if col not in [f.name for f in arcpy.ListFields(tabela)]:
        arcpy.AddField_management(tabela, col, "DOUBLE")

# Atualizar os valores das colunas de porcentagem
with arcpy.da.UpdateCursor(tabela, colunas_originais + colunas_porcentagem) as cursor:
    for row in cursor:
        valores = [v if v is not None else 0 for v in row[:5]]  # Substituir None por 0
        soma = sum(valores)

        if soma > 0:
            porcentagens = [(v / soma) * 100 for v in valores]  # Calcular %
        else:
            porcentagens = [0] * len(valores)  # Evitar divisão por zero

        cursor.updateRow(list(row[:5]) + porcentagens)  # Atualizar a linha  

#sempre que for atualizar os campos e a quantidade de campos, não esqueça de trocar o valor in "row[]" também de acordo
#com a quantidade de colunas novas    
        
print("Processo concluído!")