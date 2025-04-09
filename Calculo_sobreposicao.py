# vamos realizar um cálculo de sobreposição de dois polígonos:
    #realizar um intersect entre as duas camadas, uma principal e outra de sobreposição
    #criar um campo para calcular a área geodésica em metros quadrados
    #summarizar por id unico, pode ser nome do grid, nome do setor, nome do node.
    #realizar um join para levar a área calculada do intersect para o poligono principal
    #criar um campo de área total, calcular a área geodésica em metros quadrados
    #criar um campo de proporção, onde iremos dividir a área do intersect/área total
    #PRONTO! agora temos a relação entre sobreposição e área total

import arcpy
import os

# === Definir ambiente ===
arcpy.env.workspace = r"caminho_gdb" #caminho onde estão todos os seus dados
arcpy.env.overwriteOutput = True  # Permite sobrescrever saídas

# === Nome das camadas dentro da GDB ===
entrada = "GRID_UNI"
sobreposicao = "sobreposicao"
intersect_output = "saida_intersect"
summary_output = "saida_summary"
id_campo = "ID_UNICO"  # Substituir pelo nome do ID da entrada

# === Intersect ===
arcpy.Intersect_analysis([entrada, sobreposicao], intersect_output, "ALL", "", "INPUT")

# === Área do Intersect ===
arcpy.AddField_management(intersect_output, "Area_Intersec", "DOUBLE")
arcpy.CalculateGeometryAttributes_management(
    intersect_output,
    [["Area_Intersec", "AREA_GEODESIC"]],
    area_unit="SQUARE_METERS"
)

# === Summarize por ID ===
arcpy.Statistics_analysis(
    intersect_output,
    summary_output,
    [["Area_Intersec", "SUM"]],
    id_campo
)

# === Join na entrada ===
arcpy.JoinField_management(entrada, id_campo, summary_output, id_campo, ["SUM_Area_Intersec"])

# === Área total da entrada ===
arcpy.AddField_management(entrada, "Area_Total", "DOUBLE")
arcpy.CalculateGeometryAttributes_management(
    entrada,
    [["Area_Total", "AREA_GEODESIC"]],
    area_unit="SQUARE_METERS"
)

# === Proporção da sobreposição ===
arcpy.AddField_management(entrada, "Proporcao", "DOUBLE")
arcpy.CalculateField_management(
    entrada,
    "Proporcao",
    "!SUM_Area_Intersec! / !Area_Total!",
    "PYTHON3"
)

print("✅ Processo finalizado com sucesso.")