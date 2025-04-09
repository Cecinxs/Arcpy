#PREDOMINANCIA DE INDICADOR

#Imagine que você tem uma série de colunas numéricas, como A, B, C, D, E. Você quer criar uma coluna de predominância
#dessa série, ou seja, se o valor em B for maior, a predominância deve retornar B.

import arcpy

# Caminho para sua feature class
fc = r"seucaminho.gdb\suatabela"

# Lista com os nomes das colunas que representam seus dados comparativos
classe_fields = ['Col_A', 'Col_B', 'Col_C', 'Col_D', 'Col_E']

# Nome da coluna onde será armazenada a predominância
coluna_saida = 'Col_Predo'

# Certifique-se de que a coluna de saída existe; se não, crie
field_names = [f.name for f in arcpy.ListFields(fc)]
if coluna_saida not in field_names:
    arcpy.AddField_management(fc, coluna_saida, 'TEXT', field_length=10)

# Atualiza cada linha com a coluna predominante
with arcpy.da.UpdateCursor(fc, classe_fields + [coluna_saida]) as cursor:
    for row in cursor:
        valores = [v if v is not None else 0 for v in row[:len(classe_fields)]]  # trata None como 0
        max_index = valores.index(max(valores))
        row[-1] = classe_fields[max_index].replace('Col_', '')  # remove prefixo se quiser
        cursor.updateRow(row)

print("Coluna 'classe_social_predominante' preenchida com sucesso!")