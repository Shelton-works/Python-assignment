"""
ASSIGNMENT 2
Total Marks: 100

This file contains solutions to all 6 questions.
Uncommon / Shona variable names are used throughout the solutions.
Every concept is explained in clear, non-technical comments.
"""

import sqlite3
import random
import socket
import threading
import time
import os
from abc import ABC, abstractmethod


# ==============================================================================
# QUESTION 1: SQLite Database Connection, Table Creation, Insertion & Retrieval
# ==============================================================================
"""
Question 1 Explanation:
Think of SQLite like a compact digital notebook stored directly inside a file on your computer.
- First, we open the notebook by connecting to it (sqlite3.connect).
- Second, we create a 'cursor', which is like our pen that writes and reads instructions.
- Third, we draw our table format (CREATE TABLE) with column headings like ID, Name, Grade, and City.
- Fourth, we insert records into the table rows (INSERT INTO).
- Finally, we ask the database to fetch and display all rows (SELECT *), and then we close the notebook.
"""

def mubvunzo_wekutanga():
    print("\n" + "=" * 60)
    print("QUESTION 1: SQLite Database Demonstration")
    print("=" * 60)

    dura_zita = "vadzidzi_database.db"

    try:
        # Step 1: Connect to the SQLite database
        tinashe_kubatana = sqlite3.connect(dura_zita)
        chipo_cursor = tinashe_kubatana.cursor()

        # Step 2: Create a table for students (vadzidzi)
        chipo_cursor.execute("""
            CREATE TABLE IF NOT EXISTS vadzidzi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                zita TEXT NOT NULL,
                giredhi INTEGER NOT NULL,
                guta TEXT NOT NULL
            )
        """)

        # Clear any previous run's data for a clean demonstration
        chipo_cursor.execute("DELETE FROM vadzidzi")

        # Step 3: Insert student data into the table
        farai_dhata = [
            ("Farai Mutasa", 5, "Harare"),
            ("Rutendo Moyo", 4, "Bulawayo"),
            ("Kudzai Gava", 6, "Gweru"),
            ("Nyasha Chimuka", 5, "Mutare")
        ]

        chipo_cursor.executemany("""
            INSERT INTO vadzidzi (zita, giredhi, guta)
            VALUES (?, ?, ?)
        """, farai_dhata)

        # Commit (save) the changes
        tinashe_kubatana.commit()
        print(f"Successfully inserted {len(farai_dhata)} student records into 'vadzidzi' table.")

        # Step 4: Retrieve and display the data from the table
        chipo_cursor.execute("SELECT id, zita, giredhi, guta FROM vadzidzi")
        zvakawanikwa_mudura = chipo_cursor.fetchall()

        print("\nRetrieved Data from Database:")
        print(f"{'ID':<5} {'Zita (Name)':<20} {'Giredhi (Grade)':<18} {'Guta (City)':<15}")
        print("-" * 58)
        for mudzidzi in zvakawanikwa_mudura:
            id_nhamba, zita_remudzidzi, giredhi_remudzidzi, guta_remudzidzi = mudzidzi
            print(f"{id_nhamba:<5} {zita_remudzidzi:<20} {giredhi_remudzidzi:<18} {guta_remudzidzi:<15}")

        # Clean up database connection
        chipo_cursor.close()
        tinashe_kubatana.close()

    except sqlite3.Error as chikanganiso:
        print(f"Database error occurred: {chikanganiso}")

    finally:
        # Remove temporary demo database file to keep workspace clean
        if os.path.exists(dura_zita):
            try:
                os.remove(dura_zita)
            except Exception:
                pass


# ==============================================================================
# QUESTION 2: Encapsulation & BankAccount Class
# ==============================================================================
"""
Question 2 Explanation:
What is Encapsulation?
Think of encapsulation like keeping your money safely tucked inside your wallet or pocket (chikwama).
If anyone on the street wants money, they cannot just reach into your pocket and take it directly!
Instead, your money is private and hidden.
If someone wants to add money (deposit) or request money (withdraw), they have to ask you nicely.
You then verify whether the amount is valid (e.g. they can't withdraw more than you have, or deposit negative money).

In Python:
- We make an attribute private by starting its name with two underscores (like `__mari_yese`).
- This stops outside code from modifying the balance directly without our permission.
- We provide controlled methods (deposit, withdraw, display_balance) to manage the money safely.
"""

class BankAccount:
    def __init__(self, muridzi_we_akaundi, mari_yokutanga=0.0):
        # Public attribute: anyone can see who owns this account
        self.muridzi_we_akaundi = muridzi_we_akaundi
        
        # Private attribute (encapsulation):
        # The double underscore '__' protects this balance from direct outside modification
        self.__mari_yese = float(mari_yokutanga) if mari_yokutanga >= 0 else 0.0

    def deposit(self, mari_inopinda):
        """Safely deposit money into the account"""
        if mari_inopinda > 0:
            self.__mari_yese += mari_inopinda
            print(f"[{self.muridzi_we_akaundi}] Deposited: ${mari_inopinda:.2f}")
        else:
            print(f"[{self.muridzi_we_akaundi}] Deposit failed: Amount must be greater than 0.")

    def withdraw(self, mari_inobuda):
        """Safely withdraw money after checking if sufficient funds exist"""
        if mari_inobuda <= 0:
            print(f"[{self.muridzi_we_akaundi}] Withdrawal failed: Amount must be greater than 0.")
        elif mari_inobuda > self.__mari_yese:
            print(f"[{self.muridzi_we_akaundi}] Withdrawal denied: Insufficient balance! Current balance is ${self.__mari_yese:.2f}")
        else:
            self.__mari_yese -= mari_inobuda
            print(f"[{self.muridzi_we_akaundi}] Successfully withdrew: ${mari_inobuda:.2f}")

    def display_balance(self):
        """Method to view the current protected balance"""
        print(f"[{self.muridzi_we_akaundi}] Current Balance: ${self.__mari_yese:.2f}")
        return self.__mari_yese


def mubvunzo_wechipiri():
    print("\n" + "=" * 60)
    print("QUESTION 2: Encapsulation Demonstration")
    print("=" * 60)

    # Create an account for Ruvimbo with an initial balance of $250
    ruvimbo_akaundi = BankAccount("Ruvimbo", 250.0)
    ruvimbo_akaundi.display_balance()

    # Perform legitimate transactions
    tatenda_deposit = 150.0
    ruvimbo_akaundi.deposit(tatenda_deposit)

    kumbirai_mari = 80.0
    ruvimbo_akaundi.withdraw(kumbirai_mari)

    # Attempting to overdraw money
    muchaneta_overdraw = 500.0
    ruvimbo_akaundi.withdraw(muchaneta_overdraw)

    # Display balance after operations
    ruvimbo_akaundi.display_balance()

    # Demonstrating Encapsulation protection:
    print("\nDemonstrating that the private attribute '__mari_yese' cannot be directly accessed:")
    try:
        # Trying to access the private balance directly from outside the class
        print(ruvimbo_akaundi.__mari_yese)
    except AttributeError as chikanganiso_che_private:
        print(f"BLOCKED BY PYTHON: Cannot access '__mari_yese' directly -> {chikanganiso_che_private}")
        print("Encapsulation successfully prevents outside code from tampering with the balance directly!")


# ==============================================================================
# QUESTION 3: Socket Client-Server Program with Basic Error Handling
# ==============================================================================
"""
Question 3 Explanation:
Think of a client and server like making a telephone call.
- The Server is a receptionist sitting by a telephone with a known phone number (Host IP and Port).
  The server sets up a socket, binds to that number, and listens for calls.
- The Client is a customer dialing the server's number.
  Once connected, the client says "Hello from client!".
- The Server picks up, receives the message, and prints it out to the console.
- Basic error handling (try-except) ensures that if the phone is busy, unreachable, or disconnected,
  the program catches the error gracefully instead of crashing abruptly.
"""

def maseva_anoshanda(host, port, server_ready_event):
    """Server function running on a background thread"""
    tawanda_server_sock = None
    try:
        tawanda_server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow reusing address immediately if restarted
        tawanda_server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tawanda_server_sock.bind((host, port))
        tawanda_server_sock.listen(1)
        tawanda_server_sock.settimeout(5.0)  # Stop waiting after 5 seconds to prevent hanging
        
        # Signal that the server is ready to accept connections
        server_ready_event.set()

        chikwata_chinobatana, kero_ye_client = tawanda_server_sock.accept()
        try:
            mashoko_akagamuchirwa = chikwata_chinobatana.recv(1024).decode("utf-8")
            print(f"[Server Console] Received message from client ({kero_ye_client}): {mashoko_akagamuchirwa}")
        finally:
            chikwata_chinobatana.close()

    except socket.timeout:
        print("[Server] Listening timed out waiting for connection.")
    except socket.error as chikanganiso_che_server:
        print(f"[Server Network Error]: {chikanganiso_che_server}")
    finally:
        if tawanda_server_sock:
            tawanda_server_sock.close()


def mutengi_anoshanda(host, port):
    """Client function connecting to the server"""
    chengetai_client_sock = None
    try:
        chengetai_client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        chengetai_client_sock.settimeout(5.0)
        chengetai_client_sock.connect((host, port))

        shoko_rekutumira = "Hello from client!"
        chengetai_client_sock.sendall(shoko_rekutumira.encode("utf-8"))
        print(f"[Client Console] Successfully sent: '{shoko_rekutumira}'")

    except socket.error as chikanganiso_che_client:
        print(f"[Client Network Error]: Failed to communicate with server: {chikanganiso_che_client}")
    finally:
        if chengetai_client_sock:
            chengetai_client_sock.close()


def mubvunzo_wechitatu():
    print("\n" + "=" * 60)
    print("QUESTION 3: Socket Client-Server Demonstration")
    print("=" * 60)

    munashe_host = "127.0.0.1"
    # Choose a high port for local socket communication
    tsitsi_port = 55432

    server_wagadzirira = threading.Event()

    # Run the server on a separate thread so it listens while the client sends
    server_shinda = threading.Thread(
        target=maseva_anoshanda,
        args=(munashe_host, tsitsi_port, server_ready_event:=server_wagadzirira)
    )
    server_shinda.daemon = True
    server_shinda.start()

    # Wait until the server is actively listening
    server_wagadzirira.wait(timeout=2.0)
    time.sleep(0.1)

    # Now execute the client
    mutengi_anoshanda(munashe_host, tsitsi_port)

    # Wait for the server thread to finish cleanly
    server_shinda.join(timeout=3.0)


# ==============================================================================
# QUESTION 4: Random Floating-Point Numbers & Min / Max Calculation
# ==============================================================================
"""
Question 4 Explanation:
We use Python's 'random' module, which works like rolling digital dice.
- `random.uniform(0.0, 10.0)` produces a random decimal number between 0 and 10.
- We generate a list of 5 such random numbers.
- Then, we use Python's built-in functions `min()` and `max()` to effortlessly find
  the lowest and highest numbers in the list without needing custom loops.
"""

def mubvunzo_wechina():
    print("\n" + "=" * 60)
    print("QUESTION 4: Random Floats, Min and Max Demonstration")
    print("=" * 60)

    # Generate a list of 5 random floating-point numbers between 0 and 10
    nhamba_dzerombo = [random.uniform(0.0, 10.0) for _ in range(5)]

    # Use Python's built-in functions min() and max()
    nhamba_yakaderera = min(nhamba_dzerombo)
    nhamba_yakakurisa = max(nhamba_dzerombo)

    print("Generated list of 5 random float numbers:")
    for chiratidzo_index, nhamba in enumerate(nhamba_dzerombo, start=1):
        print(f"  {chiratidzo_index}. {nhamba:.4f}")

    print(f"\nMinimum value (using min()): {nhamba_yakaderera:.4f}")
    print(f"Maximum value (using max()): {nhamba_yakakurisa:.4f}")


# ==============================================================================
# QUESTION 5: Abstract Base Class (ABC) FileHandler Hierarchy
# ==============================================================================
"""
Question 5 Explanation:
What is an Abstract Base Class (ABC)?
Think of `FileHandler` as an official architectural blueprint or a legal contract.
It tells us: 'Any class that wants to handle files MUST know how to read() and write().'
You cannot build a house directly out of the paper blueprint (you cannot instantiate an ABC).
Instead, actual concrete builders (like `TextFileHandler` and `BinaryFileHandler`) follow the blueprint
and write the real code for reading and writing plain text or raw binary files.
"""

class FileHandler(ABC):
    """Abstract base class defining the required contract for all file handlers"""

    @abstractmethod
    def read(self, zita_refaira):
        """Abstract method to read from a file"""
        pass

    @abstractmethod
    def write(self, zita_refaira, zviri_mukati):
        """Abstract method to write content into a file"""
        pass


class TextFileHandler(FileHandler):
    """Concrete handler for reading and writing normal human-readable text files"""

    def read(self, zita_refaira):
        try:
            with open(zita_refaira, "r", encoding="utf-8") as rugwaro_file:
                mashoko = rugwaro_file.read()
                print(f"[TextFileHandler] Read content from '{zita_refaira}':\n  -> \"{mashoko.strip()}\"")
                return mashoko
        except FileNotFoundError:
            print(f"[TextFileHandler Error]: File '{zita_refaira}' was not found.")
            return None

    def write(self, zita_refaira, zviri_mukati):
        with open(zita_refaira, "w", encoding="utf-8") as rugwaro_file:
            rugwaro_file.write(str(zviri_mukati))
            print(f"[TextFileHandler] Successfully wrote text to '{zita_refaira}'")


class BinaryFileHandler(FileHandler):
    """Concrete handler for reading and writing binary files (e.g. images, audio, raw bytes)"""

    def read(self, zita_refaira):
        try:
            with open(zita_refaira, "rb") as bhinari_file:
                data_remabhinari = bhinari_file.read()
                print(f"[BinaryFileHandler] Read {len(data_remabhinari)} bytes from '{zita_refaira}':\n  -> {data_remabhinari}")
                return data_remabhinari
        except FileNotFoundError:
            print(f"[BinaryFileHandler Error]: Binary file '{zita_refaira}' was not found.")
            return None

    def write(self, zita_refaira, zviri_mukati):
        # Convert string to bytes if passed as string, otherwise write bytes directly
        bytes_data = zviri_mukati.encode("utf-8") if isinstance(zviri_mukati, str) else zviri_mukati
        with open(zita_refaira, "wb") as bhinari_file:
            bhinari_file.write(bytes_data)
            print(f"[BinaryFileHandler] Successfully wrote {len(bytes_data)} bytes to '{zita_refaira}'")


def mubvunzo_wechishanu():
    print("\n" + "=" * 60)
    print("QUESTION 5: Abstract Base Class FileHandler Demonstration")
    print("=" * 60)

    sekai_text_handler = TextFileHandler()
    fungai_binary_handler = BinaryFileHandler()

    rugwaro_zita = "mufaro_rugwaro.txt"
    bhinari_zita = "mufaro_dhata.bin"

    try:
        # Testing TextFileHandler
        mashoko_emufaro = "Kudzidza Python kwakanakisa! (Learning Python is great!)"
        sekai_text_handler.write(rugwaro_zita, mashoko_emufaro)
        sekai_text_handler.read(rugwaro_zita)

        print()

        # Testing BinaryFileHandler
        raw_bhinari_mashoko = b"Raw binary payload: \x00\x01\x02\xFF"
        fungai_binary_handler.write(bhinari_zita, raw_bhinari_mashoko)
        fungai_binary_handler.read(bhinari_zita)

        # Demonstrating that the abstract class itself cannot be directly instantiated:
        print("\nDemonstrating that the Abstract Base Class FileHandler cannot be instantiated directly:")
        try:
            _ = FileHandler()
        except TypeError as chikanganiso_che_abc:
            print(f"BLOCKED BY PYTHON: Cannot instantiate FileHandler directly -> {chikanganiso_che_abc}")

    finally:
        # Clean up created demo files
        for faira in [rugwaro_zita, bhinari_zita]:
            if os.path.exists(faira):
                try:
                    os.remove(faira)
                except Exception:
                    pass


# ==============================================================================
# QUESTION 6: Class Hierarchy and Method Overriding (Vehicle, Car, Bike)
# ==============================================================================
"""
Question 6 Explanation:
What is a Class Hierarchy and Method Overriding?
A class hierarchy is like a family tree.
- `Vehicle` is the parent (base class).
- `Car` and `Bike` are the children (subclasses).
The parent has a general method called `move()`.
When a child class inherits from the parent, it can either use the parent's generic `move()`
or provide its own custom version of `move()`.
Replacing the parent's method with a custom version in the child class is called 'Method Overriding'.
A car moves with a roaring engine on 4 wheels, while a bike moves by pedaling on 2 wheels.
"""

class Vehicle:
    """Base class representing any generic vehicle"""

    def __init__(self, mhando_yemudziyo, muridzi):
        self.mhando_yemudziyo = mhando_yemudziyo  # Model / make
        self.muridzi = muridzi                  # Owner's name

    def move(self):
        """Base method: Generic movement behavior for all vehicles"""
        print(f"[Vehicle] {self.muridzi}'s {self.mhando_yemudziyo} is moving forward along the road.")


class Car(Vehicle):
    """Subclass representing a car, inheriting from Vehicle"""

    def __init__(self, mhando_yemudziyo, muridzi, mawhiri=4):
        super().__init__(mhando_yemudziyo, muridzi)
        self.mawhiri = mawhiri

    def move(self):
        """Overriding the move() method specifically for a car"""
        print(f"[Car] {self.muridzi}'s car ({self.mhando_yemudziyo}) revs its engine and cruises smoothly on {self.mawhiri} wheels!")


class Bike(Vehicle):
    """Subclass representing a bicycle, inheriting from Vehicle"""

    def __init__(self, mhando_yemudziyo, muridzi, ine_bhero=True):
        super().__init__(mhando_yemudziyo, muridzi)
        self.ine_bhero = ine_bhero

    def move(self):
        """Overriding the move() method specifically for a bicycle"""
        kurira = "ringing its bell (karing-ring!)" if self.ine_bhero else "gliding silently"
        print(f"[Bike] {self.muridzi}'s bicycle ({self.mhando_yemudziyo}) pedals down the pathway, {kurira} on 2 wheels!")


def mubvunzo_wechitanhatu():
    print("\n" + "=" * 60)
    print("QUESTION 6: Class Hierarchy and Method Overriding")
    print("=" * 60)

    # Instantiate base class and both subclasses
    simbarashe_mudziyo = Vehicle("Generic Transporter", "Simbarashe")
    takudzwa_mota = Car("Toyota Hilux", "Takudzwa", mawhiri=4)
    anopa_bhasikoro = Bike("Mountain Bike", "Anopa", ine_bhero=True)

    # Demonstrate polymorphic method calls (overriding in action)
    print("Calling move() on each object to demonstrate method overriding:")
    zvifambiso = [simbarashe_mudziyo, takudzwa_mota, anopa_bhasikoro]

    for mudziyo in zvifambiso:
        mudziyo.move()


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("     STARTING ASSIGNMENT 2 DEMONSTRATIONS (100 MARKS)")
    print("#" * 60)

    mubvunzo_wekutanga()
    mubvunzo_wechipiri()
    mubvunzo_wechitatu()
    mubvunzo_wechina()
    mubvunzo_wechishanu()
    mubvunzo_wechitanhatu()

    print("\n" + "#" * 60)
    print("     ALL ASSIGNMENT 2 QUESTIONS COMPLETED SUCCESSFULLY!")
    print("#" * 60 + "\n")
