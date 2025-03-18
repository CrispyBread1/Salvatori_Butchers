import socket
import psycopg2

DB_HOST = "db.qebranyoffuyctlpemxx.supabase.co"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "KQz9Q0PP8vjCpaDR"

def test_dns_resolution():
    """ Check if the server can resolve the database hostname. """
    try:
        ip = socket.gethostbyname(DB_HOST)
        print(f"✅ DNS Resolution Successful: {DB_HOST} -> {ip}")
    except socket.gaierror:
        print(f"❌ Failed to resolve hostname: {DB_HOST}. Check DNS settings.")

def test_database_connection():
    """ Attempt to connect to the database and check for any errors. """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("✅ Successfully connected to the database!")
        conn.close()
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

if __name__ == "__main__":
    print("🔹 Running Network & Database Connection Tests...")
    test_dns_resolution()
    test_database_connection()
