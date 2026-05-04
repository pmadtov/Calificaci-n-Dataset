import pandas as pd
import os

def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
    
    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if ext == ".csv":
            return pd.read_csv(
                file_path,
                sep=",",
                engine="python",
                on_bad_lines="warn"
            )

        elif ext == ".txt":
            return pd.read_csv(
                file_path,
                sep=",",
                engine="python",
                on_bad_lines="warn"
            )

        elif ext in [".xlsx", ".xls"]:
            return pd.read_excel(file_path)

        else:
            raise ValueError(f"Formato de archivo no soportado: {ext}. Usa CSV, Excel o TXT.")

    except Exception as e:
        raise RuntimeError(f"Error al cargar el archivo: {e}")

def score_completeness(df):
    total_cells = df.shape[0] * df.shape[1]
    if total_cells == 0:
        return 0, 100
        
    total_nulls = df.isnull().sum().sum()
    null_percentage = total_nulls / total_cells
    
    score = 40 * (1 - null_percentage)
    return round(score, 2), null_percentage * 100

def score_uniqueness(df):
    total_rows = df.shape[0]
    if total_rows == 0:
        return 0, 100
        
    duplicate_rows = df.duplicated().sum()
    duplicate_percentage = duplicate_rows / total_rows
    
    score = 20 * (1 - duplicate_percentage)
    return round(score, 2), duplicate_percentage * 100

def score_consistency(df):
    total_columns = df.shape[1]
    if total_columns == 0:
        return 0, 0
        
    zero_variance_cols = 0

    for col in df.columns:
        if df[col].nunique(dropna=True) <= 1:
            zero_variance_cols += 1
            
    bad_cols_percentage = zero_variance_cols / total_columns
    
    score = 20 * (1 - bad_cols_percentage)
    return round(score, 2), zero_variance_cols

def score_volume(df, min_rows=50, min_cols=3):
    rows, cols = df.shape
    
    row_score = min(rows / min_rows, 1.0) * 10
    col_score = min(cols / min_cols, 1.0) * 10
    
    score = row_score + col_score
    return round(score, 2), rows, cols

def evaluate_database(file_path):
    print(f"\n--- Evaluando Base de Datos: {os.path.basename(file_path)} ---")
    
    try:
        df = load_data(file_path)
    except Exception as e:
        print(f"ERROR: {e}")
        return
        
    if df.empty:
        print("El archivo está completamente vacío.")
        print("Calificación Final: 0 / 100")
        return
        
    print(f"Dimensiones cargadas: {df.shape[0]} filas x {df.shape[1]} columnas")
    print("-" * 50)
    
    comp_score, null_pct = score_completeness(df)
    print(f"1. Completitud: {comp_score}/40 pts (Valores Nulos: {null_pct:.2f}%)")
    
    uniq_score, dup_pct = score_uniqueness(df)
    print(f"2. Unicidad: {uniq_score}/20 pts (Filas Duplicadas: {dup_pct:.2f}%)")
    
    cons_score, bad_cols = score_consistency(df)
    print(f"3. Consistencia: {cons_score}/20 pts (Columnas con 1 solo valor: {bad_cols})")
    
    vol_score, rows, cols = score_volume(df)
    print(f"4. Volumen: {vol_score}/20 pts (Filas: {rows}, Columnas: {cols})")
    
    print("-" * 50)
    
    total_score = comp_score + uniq_score + cons_score + vol_score
    print(f"CALIFICACIÓN FINAL: {total_score:.2f} / 100")
    
    if total_score >= 80:
        print("Veredicto: EXCELENTE. La base de datos es altamente utilizable.")
    elif total_score >= 60:
        print("Veredicto: ACEPTABLE. Se puede usar, pero requiere limpieza.")
    elif total_score >= 40:
        print("Veredicto: DEFICIENTE. Faltan muchos datos o hay mucha redundancia.")
    else:
        print("Veredicto: NO RECOMENDADA. La base de datos tiene graves problemas de calidad.")
        
    print("\n")

if __name__ == "__main__":
    archivo = r"C:\Users\pablo\OneDrive\Documents\ANAHUAC QRO\BAKERTILLY\gemini-code-1777416686152.txt"
    evaluate_database(archivo)
