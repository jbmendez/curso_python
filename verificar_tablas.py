import sqlite3

# Conectar a la BD existente
conn = sqlite3.connect('sistema_controles.db')
cursor = conn.cursor()

# Obtener todas las tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("📊 Tablas existentes en sistema_controles.db:")
for table in tables:
    table_name = table[0]
    print(f"  - {table_name}")
    
    # Obtener estructura de la tabla
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    for col in columns:
        print(f"    {col[1]} ({col[2]})")
    print()

# Verificar si existe tabla programaciones
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='programaciones'")
prog_table = cursor.fetchone()

if prog_table:
    print("✅ La tabla 'programaciones' ya existe")
    cursor.execute("SELECT COUNT(*) FROM programaciones")
    count = cursor.fetchone()[0]
    print(f"📝 Programaciones existentes: {count}")
else:
    print("❌ La tabla 'programaciones' NO existe")

conn.close()