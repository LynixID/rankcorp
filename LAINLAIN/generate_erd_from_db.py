"""
Script untuk generate visualisasi ERD dari database SQLite
Menggunakan graphviz untuk membuat diagram relasi
"""
import sqlite3
import os
from pathlib import Path

try:
    from graphviz import Digraph
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
    print("Graphviz tidak terinstall. Install dengan: pip install graphviz")
    print("Dan install graphviz binary: https://graphviz.org/download/")

def get_database_path():
    """Mencari lokasi db.sqlite3"""
    base_dir = Path(__file__).parent
    db_path = base_dir / 'db.sqlite3'
    
    if not db_path.exists():
        # Coba cari di subdirectory
        for path in base_dir.rglob('db.sqlite3'):
            return path
    
    return db_path

def get_tables_and_relations(db_path):
    """Mengambil informasi tabel dan relasi dari database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Ambil semua tabel
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [row[0] for row in cursor.fetchall()]
    
    # Ambil informasi kolom dan foreign key untuk setiap tabel
    table_info = {}
    relations = []
    
    for table in tables:
        # Ambil struktur tabel
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        
        # Ambil foreign keys
        cursor.execute(f"PRAGMA foreign_key_list({table})")
        foreign_keys = cursor.fetchall()
        
        # Format: (id, seq, table, from, to, on_update, on_delete, match)
        table_info[table] = {
            'columns': columns,
            'foreign_keys': foreign_keys
        }
        
        # Simpan relasi
        for fk in foreign_keys:
            relations.append({
                'from_table': table,
                'from_column': fk[3],  # 'from' column
                'to_table': fk[2],     # 'table' (referenced table)
                'to_column': fk[4],    # 'to' column
                'on_delete': fk[6]     # on_delete action
            })
    
    conn.close()
    return tables, table_info, relations

def generate_erd_html(tables, table_info, relations):
    """Generate ERD dalam format HTML"""
    html = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ERD - Database SQLite</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .table-box {
            border: 2px solid #333;
            border-radius: 5px;
            margin: 20px;
            display: inline-block;
            vertical-align: top;
            background: white;
            min-width: 200px;
        }
        .table-header {
            background: #667eea;
            color: white;
            padding: 10px;
            font-weight: bold;
            text-align: center;
        }
        .table-body {
            padding: 5px;
        }
        .column {
            padding: 5px 10px;
            border-bottom: 1px solid #eee;
            font-size: 0.9em;
        }
        .column:last-child {
            border-bottom: none;
        }
        .pk {
            color: #d32f2f;
            font-weight: bold;
        }
        .pk::before {
            content: "🔑 ";
        }
        .fk {
            color: #1976d2;
            font-style: italic;
        }
        .fk::after {
            content: " →";
        }
        .diagram-area {
            text-align: center;
            padding: 20px;
            min-height: 600px;
            position: relative;
        }
        .relation-line {
            position: absolute;
            border: 2px solid #ff9800;
            z-index: 1;
        }
        .stats {
            margin-top: 30px;
            padding: 20px;
            background: #f0f0f0;
            border-radius: 8px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .stat-item {
            background: white;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>ERD - Database SQLite</h1>
        <div class="diagram-area">
"""
    
    # Generate table boxes
    for table in tables:
        html += f"""
            <div class="table-box" id="table-{table}">
                <div class="table-header">{table}</div>
                <div class="table-body">
"""
        for col in table_info[table]['columns']:
            col_id, col_name, col_type, not_null, default_val, is_pk = col
            
            # Cek apakah ini foreign key
            is_fk = any(fk[3] == col_name for fk in table_info[table]['foreign_keys'])
            
            class_name = ""
            if is_pk:
                class_name = "pk"
            elif is_fk:
                class_name = "fk"
            
            html += f'                    <div class="column {class_name}">{col_name} ({col_type})</div>\n'
        
        html += """                </div>
            </div>
"""
    
    html += """        </div>
        
        <div class="stats">
            <h3>Statistik</h3>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number">""" + str(len(tables)) + """</div>
                    <div>Total Tabel</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">""" + str(len(relations)) + """</div>
                    <div>Total Relasi</div>
                </div>
            </div>
        </div>
        
        <div style="margin-top: 30px; padding: 20px; background: #f9f9f9; border-radius: 8px;">
            <h3>Relasi Database</h3>
            <ul>
"""
    
    for rel in relations:
        html += f'                <li><strong>{rel["from_table"]}</strong>.{rel["from_column"]} → <strong>{rel["to_table"]}</strong>.{rel["to_column"]} (on_delete: {rel["on_delete"]})</li>\n'
    
    html += """            </ul>
        </div>
    </div>
</body>
</html>"""
    
    return html

def main():
    db_path = get_database_path()
    
    if not db_path.exists():
        print(f"❌ Database tidak ditemukan di: {db_path}")
        print("Pastikan file db.sqlite3 ada di root project")
        return
    
    print(f"📂 Membaca database: {db_path}")
    
    try:
        tables, table_info, relations = get_tables_and_relations(db_path)
        
        print(f"✅ Ditemukan {len(tables)} tabel")
        print(f"✅ Ditemukan {len(relations)} relasi")
        
        # Generate HTML
        html_content = generate_erd_html(tables, table_info, relations)
        
        output_file = Path(__file__).parent / 'ERD_FROM_DATABASE.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ ERD berhasil di-generate: {output_file}")
        print(f"📖 Buka file di browser untuk melihat visualisasi")
        
        # Print summary
        print("\n📊 Daftar Tabel:")
        for table in tables:
            col_count = len(table_info[table]['columns'])
            fk_count = len(table_info[table]['foreign_keys'])
            print(f"  - {table} ({col_count} kolom, {fk_count} foreign key)")
        
        if relations:
            print("\n🔗 Daftar Relasi:")
            for rel in relations:
                print(f"  - {rel['from_table']}.{rel['from_column']} → {rel['to_table']}.{rel['to_column']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


