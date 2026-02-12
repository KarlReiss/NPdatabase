#!/usr/bin/env python3
"""
Import NPASS 3.0 bioactivity data into the bioactivity table.

This script reads NPASS3.0_activities.txt and imports the data into the bioactivity table,
mapping np_id and target_id to their corresponding database IDs.
"""

import psycopg2
import sys
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'npdb',
    'user': 'yfguo',
    'password': ''
}

def connect_db():
    """Connect to PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def load_np_id_mapping(conn):
    """Load mapping of np_id to natural_product id."""
    print("Loading natural product ID mapping...")
    cursor = conn.cursor()
    cursor.execute("SELECT id, np_id FROM natural_products WHERE np_id IS NOT NULL")
    mapping = {row[1]: row[0] for row in cursor.fetchall()}
    cursor.close()
    print(f"Loaded {len(mapping)} natural product mappings")
    return mapping

def load_target_id_mapping(conn):
    """Load mapping of target_id to target id."""
    print("Loading target ID mapping...")
    cursor = conn.cursor()
    cursor.execute("SELECT id, target_id FROM targets WHERE target_id IS NOT NULL")
    mapping = {row[1]: row[0] for row in cursor.fetchall()}
    cursor.close()
    print(f"Loaded {len(mapping)} target mappings")
    return mapping

def parse_value(value_str):
    """Parse activity value, return None for 'n.a.'"""
    if value_str == 'n.a.' or not value_str.strip():
        return None
    try:
        return float(value_str)
    except ValueError:
        return None

def import_bioactivity_data(conn, input_file):
    """Import bioactivity data from NPASS 3.0 activities file."""

    # Load ID mappings
    np_mapping = load_np_id_mapping(conn)
    target_mapping = load_target_id_mapping(conn)

    cursor = conn.cursor()

    # Clear existing data
    print("Clearing existing bioactivity data...")
    cursor.execute("TRUNCATE TABLE bioactivity RESTART IDENTITY CASCADE")
    conn.commit()

    print(f"Reading data from {input_file}...")

    inserted = 0
    skipped_np = 0
    skipped_target = 0
    errors = 0
    batch = []
    batch_size = 5000

    with open(input_file, 'r', encoding='utf-8') as f:
        # Skip header
        header = f.readline()

        for line_num, line in enumerate(f, start=2):
            try:
                fields = line.strip().split('\t')

                if len(fields) != 14:
                    print(f"Warning: Line {line_num} has {len(fields)} fields, expected 14")
                    errors += 1
                    continue

                np_id = fields[0]
                target_id = fields[1]
                activity_type_grouped = fields[2] if fields[2] != 'n.a.' else None
                activity_relation = fields[3] if fields[3] != 'n.a.' else None
                activity_type = fields[4] if fields[4] != 'n.a.' else None
                activity_value = parse_value(fields[5])
                activity_units = fields[6] if fields[6] != 'n.a.' else None
                assay_organism = fields[7] if fields[7] != 'n.a.' else None
                assay_tax_id = fields[8] if fields[8] != 'n.a.' else None
                assay_strain = fields[9] if fields[9] != 'n.a.' else None
                assay_tissue = fields[10] if fields[10] != 'n.a.' else None
                assay_cell_type = fields[11] if fields[11] != 'n.a.' else None
                ref_id = fields[12] if fields[12] != 'n.a.' else None
                ref_id_type = fields[13] if fields[13] != 'n.a.' else None

                # Map IDs
                natural_product_id = np_mapping.get(np_id)
                target_db_id = target_mapping.get(target_id)

                if natural_product_id is None:
                    skipped_np += 1
                    continue

                if target_db_id is None:
                    skipped_target += 1
                    continue

                batch.append((
                    natural_product_id,
                    target_db_id,
                    activity_type,
                    activity_type_grouped,
                    activity_relation,
                    activity_value,
                    activity_units,
                    assay_organism,
                    assay_tax_id,
                    assay_strain,
                    assay_tissue,
                    assay_cell_type,
                    ref_id,
                    ref_id_type
                ))

                # Insert batch
                if len(batch) >= batch_size:
                    cursor.executemany("""
                        INSERT INTO bioactivity (
                            natural_product_id, target_id, activity_type, activity_type_grouped,
                            activity_relation, activity_value, activity_units,
                            assay_organism, assay_tax_id, assay_strain, assay_tissue,
                            assay_cell_type, ref_id, ref_id_type
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, batch)
                    conn.commit()
                    inserted += len(batch)
                    batch = []

                    if inserted % 50000 == 0:
                        print(f"Inserted {inserted} records...")

            except Exception as e:
                print(f"Error processing line {line_num}: {e}")
                errors += 1
                continue

        # Insert remaining batch
        if batch:
            cursor.executemany("""
                INSERT INTO bioactivity (
                    natural_product_id, target_id, activity_type, activity_type_grouped,
                    activity_relation, activity_value, activity_units,
                    assay_organism, assay_tax_id, assay_strain, assay_tissue,
                    assay_cell_type, ref_id, ref_id_type
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, batch)
            conn.commit()
            inserted += len(batch)

    cursor.close()

    print("\n" + "="*60)
    print("Import Summary:")
    print("="*60)
    print(f"Total records inserted: {inserted:,}")
    print(f"Skipped (np_id not found): {skipped_np:,}")
    print(f"Skipped (target_id not found): {skipped_target:,}")
    print(f"Errors: {errors:,}")
    print("="*60)

    return inserted

def main():
    input_file = '/home/yfguo/NPdatabase/data/NPASS/NPASS3.0_activities.txt'

    print("="*60)
    print("NPASS 3.0 Bioactivity Data Import")
    print("="*60)
    print(f"Input file: {input_file}")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    conn = connect_db()

    try:
        inserted = import_bioactivity_data(conn, input_file)

        # Verify import
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM bioactivity")
        count = cursor.fetchone()[0]
        cursor.close()

        print(f"\nVerification: {count:,} records in bioactivity table")
        print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        print(f"Error during import: {e}")
        conn.rollback()
        sys.exit(1)
    finally:
        conn.close()

if __name__ == '__main__':
    main()
