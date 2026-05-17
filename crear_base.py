import pandas as pd

print("⏳ Iniciando creación de la nueva base de datos unificada...")

# 1. Leer los archivos originales
df_mortalidad = pd.read_excel("NoFetal2019.xlsx", sheet_name="No_Fetales_2019")
df_divipola3 = pd.read_excel("Divipola.xlsx", sheet_name="Hoja3")

print("🧹 Limpiando códigos de texto y coordenadas...")

# 2. Estandarizar los códigos para evitar vacíos
df_mortalidad["COD_DANE"] = df_mortalidad["COD_DANE"].astype(str).str.strip().str.zfill(5)
df_divipola3["codigo municipio"] = df_divipola3["codigo municipio"].astype(str).str.strip().str.zfill(5)

# 3. LIMPIEZA CRÍTICA DE COORDENADAS (Quitar comillas extras y cambiar comas por puntos)
df_divipola3["Latitud"] = df_divipola3["Latitud"].astype(str).str.replace('"', '').str.replace(',', '.').str.strip()
df_divipola3["Longitud"] = df_divipola3["Longitud"].astype(str).str.replace('"', '').str.replace(',', '.').str.strip()

# 4. Convertir a formato numérico puro de Python
df_divipola3["Latitud"] = pd.to_numeric(df_divipola3["Latitud"], errors='coerce')
df_divipola3["Longitud"] = pd.to_numeric(df_divipola3["Longitud"], errors='coerce')

# 5. Crear los diccionarios de mapeo
mapa_deptos = dict(zip(df_divipola3["codigo municipio"], df_divipola3["departamento (nombre)"].astype(str).str.upper().str.strip()))
mapa_munis = dict(zip(df_divipola3["codigo municipio"], df_divipola3["nombre municipio"].astype(str).str.upper().str.strip()))
mapa_lat = dict(zip(df_divipola3["codigo municipio"], df_divipola3["Latitud"]))
mapa_lon = dict(zip(df_divipola3["codigo municipio"], df_divipola3["Longitud"]))

# 6. Mapear de forma segura sin romper la estructura del DataFrame original
df_mortalidad["DEPARTAMENTO_TEXTO"] = df_mortalidad["COD_DANE"].map(mapa_deptos).fillna("DESCONOCIDO")
df_mortalidad["MUNICIPIO_TEXTO"] = df_mortalidad["COD_DANE"].map(mapa_munis).fillna("DESCONOCIDO")
df_mortalidad["LATITUD"] = df_mortalidad["COD_DANE"].map(mapa_lat).fillna(4.5709)
df_mortalidad["LONGITUD"] = df_mortalidad["COD_DANE"].map(mapa_lon).fillna(-74.2973)

# 7. Guardar el nuevo archivo maestro
print("💾 Guardando 'NoFetal2019_Modificado.xlsx'...")
with pd.ExcelWriter("NoFetal2019_Modificado.xlsx") as writer:
    df_mortalidad.to_excel(writer, sheet_name="No_Fetales_2019", index=False)

print("✅ ¡ÉXITO TOTAL! El archivo se creó correctamente sin errores de formato.")