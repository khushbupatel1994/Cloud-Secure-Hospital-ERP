"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Database
Version : 3.0
===========================================================
"""

import sqlite3
import os


class Database:

    def __init__(self):

        # Store writable application data in LOCALAPPDATA.
        # The bundled database is used only as a first-run seed.
        from config.paths import DATABASE_DIR, resource_path
        import shutil

        os.makedirs(DATABASE_DIR, exist_ok=True)
        self.db_path = os.getenv(
    "HOSPITAL_DB",
    os.path.join(DATABASE_DIR, "hospital.db")
)

self.db_path = os.path.abspath(self.db_path)

os.makedirs(
    os.path.dirname(self.db_path),
    exist_ok=True
)

        bundled_db = resource_path("database", "hospital.db")
        if not os.path.exists(self.db_path) and os.path.exists(bundled_db):
            try:
                shutil.copy2(bundled_db, self.db_path)
            except Exception as e:
                print("Database seed warning:", e)

        self.conn = None
        self.cursor = None

    # ==========================================
    # Connect Database
    # ==========================================

    def connect(self):

        if self.conn is not None:
            return self.conn

        self.conn = sqlite3.connect(
            self.db_path
        )

        self.conn.execute(
            "PRAGMA foreign_keys = ON"
        )

        self.cursor = self.conn.cursor()

        print("✅ Database Connected")

        # Initialize tables
        self.initialize_database()

        return self.conn

    # ==========================================
    # Initialize Database
    # ==========================================

    def initialize_database(self):

        if self.cursor is None:
            return

        # ==========================================
        # DOCTORS
        # ==========================================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            doctor_id TEXT UNIQUE,

            doctor_code TEXT UNIQUE,

            full_name TEXT,

            name TEXT,

            gender TEXT,

            department TEXT,

            specialization TEXT,

            qualification TEXT,

            experience INTEGER DEFAULT 0,

            mobile TEXT,

            phone TEXT,

            email TEXT,

            consultation_fee REAL DEFAULT 0,

            opd_timing TEXT,

            available_days TEXT,

            available_time TEXT,

            joining_date TEXT,

            status TEXT DEFAULT 'Active',

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # ==========================================
        # PATIENTS
        # ==========================================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_id TEXT UNIQUE,

            registration_no TEXT UNIQUE,

            patient_code TEXT UNIQUE,

            patient_name TEXT,

            name TEXT,

            gender TEXT,

            dob TEXT,

            age INTEGER,

            blood_group TEXT,

            mobile TEXT,

            phone TEXT,

            email TEXT,

            address TEXT,

            city TEXT,

            state TEXT,

            pin_code TEXT,

            pincode TEXT,

            aadhaar TEXT,

            disease TEXT,

            emergency_contact TEXT,

            doctor TEXT,

            department TEXT,

            patient_type TEXT,

            assigned_doctor INTEGER,

            registration_date TEXT,

            registration_time TEXT,

            registration_day TEXT,

            status TEXT DEFAULT 'Active',

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # ==========================================
        # APPOINTMENTS
        # ==========================================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            appointment_id TEXT UNIQUE,

            patient_id INTEGER,

            doctor_id INTEGER,

            patient_name TEXT,

            doctor_name TEXT,

            department TEXT,

            appointment_date TEXT,

            appointment_time TEXT,

            visit_type TEXT,

            token_no TEXT,

            token_number INTEGER,

            purpose TEXT,

            status TEXT DEFAULT 'Pending',

            remarks TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # ==========================================
        # BILLING
        # ==========================================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS billing(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            bill_id TEXT UNIQUE,

            bill_no TEXT UNIQUE,

            patient TEXT,

            patient_name TEXT,

            doctor TEXT,

            doctor_name TEXT,

            bill_date TEXT,

            consultation_fee REAL DEFAULT 0,

            consultation REAL DEFAULT 0,

            medicine_charges REAL DEFAULT 0,

            medicine_charge REAL DEFAULT 0,

            lab_charges REAL DEFAULT 0,

            lab_charge REAL DEFAULT 0,

            room_charge REAL DEFAULT 0,

            other_charges REAL DEFAULT 0,

            other_charge REAL DEFAULT 0,

            discount REAL DEFAULT 0,

            tax REAL DEFAULT 0,

            gst REAL DEFAULT 0,

            total_amount REAL DEFAULT 0,

            total REAL DEFAULT 0,

            payment_mode TEXT,

            payment_method TEXT,

            bill_status TEXT,

            payment_status TEXT,

            advance REAL DEFAULT 0,

            due REAL DEFAULT 0,

            remarks TEXT,

            created_by TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # ==========================================
        # PHARMACY
        # ==========================================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS pharmacy(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            medicine_code TEXT UNIQUE,

            medicine_name TEXT,

            category TEXT,

            batch_number TEXT,

            supplier TEXT,

            quantity INTEGER DEFAULT 0,

            minimum_stock INTEGER DEFAULT 10,

            price REAL DEFAULT 0,

            expiry_date TEXT,

            status TEXT DEFAULT 'Available',

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # ==========================================
        # LABORATORY
        # ==========================================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS lab_tests(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_id INTEGER,

            doctor_id INTEGER,

            appointment_id INTEGER,

            test_name TEXT,

            result TEXT,

            remarks TEXT,

            report_date TEXT,

            status TEXT DEFAULT 'Pending',

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # ==========================================
        # INVENTORY
        # ==========================================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            item_id TEXT UNIQUE,

            item_name TEXT,

            category TEXT,

            supplier TEXT,

            batch_no TEXT,

            purchase_price REAL DEFAULT 0,

            selling_price REAL DEFAULT 0,

            stock_quantity INTEGER DEFAULT 0,

            minimum_stock INTEGER DEFAULT 0,

            unit TEXT,

            gst REAL DEFAULT 0,

            expiry_date TEXT,

            remarks TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # ==========================================
        # ACCOUNTS
        # ==========================================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            transaction_id TEXT UNIQUE,

            transaction_date TEXT,

            transaction_type TEXT,

            category TEXT,

            amount REAL DEFAULT 0,

            payment_mode TEXT,

            description TEXT,

            remarks TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # ==========================================
        # EMPLOYEES
        # ==========================================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            employee_id TEXT UNIQUE,

            full_name TEXT,

            father_name TEXT,

            gender TEXT,

            dob TEXT,

            blood_group TEXT,

            marital_status TEXT,

            mobile TEXT,

            email TEXT,

            address TEXT,

            city TEXT,

            state TEXT,

            pincode TEXT,

            department TEXT,

            designation TEXT,

            joining_date TEXT,

            employment_type TEXT,

            basic_salary REAL DEFAULT 0,

            shift TEXT,

            status TEXT DEFAULT 'Active',

            aadhaar_no TEXT,

            pan_no TEXT,

            qualification TEXT,

            experience TEXT,

            photo TEXT,

            remarks TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # =====================================================
        # SAFE DATABASE MIGRATION
        # =====================================================

        try:
            # -----------------------------------------
            # PATIENTS TABLE
            # -----------------------------------------
            self.cursor.execute(
                "PRAGMA table_info(patients)"
            )

            patient_columns = [
                row[1]
                for row in self.cursor.fetchall()
            ]

            if "father_husband_name" not in patient_columns:
                self.cursor.execute("""
                    ALTER TABLE patients
                    ADD COLUMN father_husband_name TEXT
                """)

                print(
                    "✅ Added patients.father_husband_name"
                )

            # -----------------------------------------
            # APPOINTMENTS TABLE
            # -----------------------------------------
            self.cursor.execute(
                "PRAGMA table_info(appointments)"
            )

            appointment_columns = [
                row[1]
                for row in self.cursor.fetchall()
            ]

            if "father_husband_name" not in appointment_columns:
                self.cursor.execute("""
                    ALTER TABLE appointments
                    ADD COLUMN father_husband_name TEXT
                """)

                print(
                    "✅ Added appointments.father_husband_name"
                )

            if "disease" not in appointment_columns:
                self.cursor.execute("""
                    ALTER TABLE appointments
                    ADD COLUMN disease TEXT
                """)

                print(
                    "✅ Added appointments.disease"
                )

            self.conn.commit()

            print(
                "✅ Patient/Appointment Migration Completed"
            )

        except Exception as e:
            print(
                "⚠ Database Migration Warning:",
                e
            )


        # ==========================================
        # ==========================================
        # OPD TABLE
        # ==========================================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS opd(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            opd_id TEXT UNIQUE,
            patient TEXT NOT NULL,
            doctor TEXT NOT NULL,
            department TEXT,
            visit_date TEXT,
            visit_time TEXT,
            chief_complaint TEXT,
            diagnosis TEXT,
            prescription TEXT,
            followup_date TEXT,
            notes TEXT,
            status TEXT DEFAULT 'Open',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # ==========================================
        # IPD TABLE
        # ==========================================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ipd(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admission_id TEXT UNIQUE,
            patient TEXT NOT NULL,
            doctor TEXT NOT NULL,
            ward TEXT,
            bed_no TEXT,
            admission_date TEXT,
            discharge_date TEXT,
            diagnosis TEXT,
            treatment TEXT,
            daily_charges REAL,
            status TEXT,
            remarks TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # COMMIT
        # ==========================================

        self.conn.commit()

        print("✅ ERP Core Tables Verified")

    
    # ==========================================
    # Save Changes
    # ==========================================

    def commit(self):

        if self.conn:

            self.conn.commit()

    # ==========================================
    # Close Database
    # ==========================================

    def close(self):

        if self.conn:

            self.conn.close()

            self.conn = None

            self.cursor = None
