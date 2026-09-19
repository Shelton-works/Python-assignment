"""
ASSIGNMENT 2
All the answers to all 6 questions are in this file.

"""

import sqlite3
import random
import socket
import threading
import time
import os
from abc import ABC, abstractmethod

# QUESTION 1: SQLite Database Connection, Table Creation, Insertion & Retrieval

"""
Question 1 Explanation:
SQLite like a compact digital notebook stored directly inside a file on your computer.
- First, we open the notebook by connecting to it (sqlite3.connect).
- Second, we create a 'cursor', which is like our fountain pen that writes and reads instructions.
- Third, we draw our table format (CREATE TABLE) with column headings like ID, Name, Rank, and Sanctuary City.
- Fourth, we insert apprentice records into the table rows (INSERT INTO).
- Finally, we ask the database to fetch and display all rows (SELECT *), and then we close the notebook.
"""

def run_question_one():
    print("\n" + "=" * 60)
    print("QUESTION 1: SQLite Database Demonstration")
    print("=" * 60)

    labyrinth_db_name = "scholars_repository.db"

    try:
        # Step 1: Connect to the SQLite database
        peregrine_db_conn = sqlite3.connect(labyrinth_db_name)
        theophilus_cursor = peregrine_db_conn.cursor()

        # Step 2: Create a table for scholars/apprentices
        theophilus_cursor.execute("""
            CREATE TABLE IF NOT EXISTS apprentices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                apprentice_name TEXT NOT NULL,
                scholastic_rank INTEGER NOT NULL,
                sanctuary_city TEXT NOT NULL
            )
        """)

        # Clear any prior run's records for a pristine demonstration
        theophilus_cursor.execute("DELETE FROM apprentices")

        # Step 3: Insert records using uncommon names into the table
        cornelius_records = [
            ("Bartholomew Sterling", 5, "Edinburgh"),
            ("Gwendolyn Vance", 4, "Canterbury"),
            ("Algernon Blackwood", 6, "Oxford"),
            ("Clementine Frost", 5, "Cambridge")
        ]

        theophilus_cursor.executemany("""
            INSERT INTO apprentices (apprentice_name, scholastic_rank, sanctuary_city)
            VALUES (?, ?, ?)
        """, cornelius_records)

        # Commit (save) the changes
        peregrine_db_conn.commit()
        print(f"Successfully inserted {len(cornelius_records)} apprentice records into 'apprentices' table.")

        # Step 4: Retrieve and display the data from the table
        theophilus_cursor.execute("SELECT id, apprentice_name, scholastic_rank, sanctuary_city FROM apprentices")
        retrieved_chronicles = theophilus_cursor.fetchall()

        print("\nRetrieved Data from Database:")
        print(f"{'ID':<5} {'Apprentice Name':<25} {'Scholastic Rank':<18} {'Sanctuary City':<15}")
        print("-" * 65)
        for scholar_entry in retrieved_chronicles:
            id_num, full_name, rank_val, city_loc = scholar_entry
            print(f"{id_num:<5} {full_name:<25} {rank_val:<18} {city_loc:<15}")

        # Clean up database connection
        theophilus_cursor.close()
        peregrine_db_conn.close()

    except sqlite3.Error as sqlite_glitch:
        print(f"Database error occurred: {sqlite_glitch}")

    finally:
        # Remove temporary demo database file to keep the workspace tidy
        if os.path.exists(labyrinth_db_name):
            try:
                os.remove(labyrinth_db_name)
            except Exception:
                pass

# QUESTION 2: Encapsulation & BankAccount Class

"""
Question 2 Explanation:
What is Encapsulation?
Encapsulation like keeping your valuables locked inside a heavy personal vault.
Passersby on the street cannot simply reach into your pockets or pry open the vault door directly!
Instead, your money is private and concealed behind locked doors.
If anyone wishes to add funds (deposit) or withdraw funds, they must ask the vault keeper through official slots.
The vault keeper checks whether the request is valid (e.g. you cannot withdraw more money than exists,
or deposit negative sums).

In Python:
- We make an attribute private by starting its name with two underscores (like `__quicksilver_balance`).
- This prevents external code from modifying or tampering with the balance directly.
- We provide controlled public methods (deposit, withdraw, display_balance) to manage funds safely.
"""

class BankAccount:
    def __init__(self, vault_custodian, initial_treasure=0.0):
        # Public attribute: the visible owner of the vault
        self.vault_custodian = vault_custodian
        
        # Private attribute (encapsulation):
        # The double underscore '__' shields this balance from direct outside modification
        self.__quicksilver_balance = float(initial_treasure) if initial_treasure >= 0 else 0.0

    def deposit(self, incoming_tribute):
        """Safely deposit money into the account"""
        if incoming_tribute > 0:
            self.__quicksilver_balance += incoming_tribute
            print(f"[{self.vault_custodian}] Deposited: ${incoming_tribute:.2f}")
        else:
            print(f"[{self.vault_custodian}] Deposit failed: Amount must be strictly greater than 0.")

    def withdraw(self, outgoing_tribute):
        """Safely withdraw money after verifying sufficient funds exist"""
        if outgoing_tribute <= 0:
            print(f"[{self.vault_custodian}] Withdrawal failed: Amount must be strictly greater than 0.")
        elif outgoing_tribute > self.__quicksilver_balance:
            print(f"[{self.vault_custodian}] Withdrawal denied: Insufficient reserves! Current balance is ${self.__quicksilver_balance:.2f}")
        else:
            self.__quicksilver_balance -= outgoing_tribute
            print(f"[{self.vault_custodian}] Successfully withdrew: ${outgoing_tribute:.2f}")

    def display_balance(self):
        """Method to view the current protected balance"""
        print(f"[{self.vault_custodian}] Current Balance: ${self.__quicksilver_balance:.2f}")
        return self.__quicksilver_balance


def run_question_two():
    print("\n" + "=" * 60)
    print("QUESTION 2: Encapsulation Demonstration")
    print("=" * 60)

    # Instantiate an account for Wilhelmina with an initial balance of $250
    wilhelmina_vault = BankAccount("Wilhelmina", 250.0)
    wilhelmina_vault.display_balance()

    # Perform legitimate transactions
    ignatius_deposit = 150.0
    wilhelmina_vault.deposit(ignatius_deposit)

    leopold_withdrawal = 80.0
    wilhelmina_vault.withdraw(leopold_withdrawal)

    # Attempt to overdraw beyond available funds
    barnaby_overdraft = 500.0
    wilhelmina_vault.withdraw(barnaby_overdraft)

    # Display balance after operations
    wilhelmina_vault.display_balance()

    # Demonstrating Encapsulation protection:
    print("\nDemonstrating that the private attribute '__quicksilver_balance' cannot be accessed directly:")
    try:
        # Attempting direct access to the private balance attribute from outside the class
        print(wilhelmina_vault.__quicksilver_balance)
    except AttributeError as clandestine_access_error:
        print(f"BLOCKED BY PYTHON: Cannot access '__quicksilver_balance' directly -> {clandestine_access_error}")
        print("Encapsulation successfully prevents outside code from altering the balance directly!")

# QUESTION 3: Socket Client-Server Program with Basic Error Handling

"""
Question 3 Explanation:
Think of a client and server like making a telephone call.
- The Server is a sentinel station waiting by a desk telephone with a known number (Host IP and Port).
  The server creates a socket, binds to that number, and listens for incoming calls.
- The Client is an emissary dialing the sentinel station's number.
  Once connected, the emissary speaks: "Hello from client!".
- The Server receives the message and prints it clearly to the console.
- Basic error handling (try-except) guarantees that if the connection drops, times out,
  or fails to connect, the application catches the error gracefully instead of crashing.
"""

def sentinel_server_worker(host, port, sentinel_ready_beacon):
    """Server function running on a background thread"""
    horatio_server_socket = None
    try:
        horatio_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow address reuse immediately in case of rapid restarts
        horatio_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        horatio_server_socket.bind((host, port))
        horatio_server_socket.listen(1)
        horatio_server_socket.settimeout(5.0)  # Prevent indefinite hanging
        
        # Signal that the sentinel server is listening and ready
        sentinel_ready_beacon.set()

        rendezvous_connection, emissary_address = horatio_server_socket.accept()
        try:
            intercepted_dispatch = rendezvous_connection.recv(1024).decode("utf-8")
            print(f"[Server Console] Received message from client ({emissary_address}): {intercepted_dispatch}")
        finally:
            rendezvous_connection.close()

    except socket.timeout:
        print("[Server] Listening timed out waiting for connection.")
    except socket.error as sentinel_network_anomaly:
        print(f"[Server Network Error]: {sentinel_network_anomaly}")
    finally:
        if horatio_server_socket:
            horatio_server_socket.close()


def emissary_client_worker(host, port):
    """Client function connecting to the server"""
    thaddeus_client_socket = None
    try:
        thaddeus_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        thaddeus_client_socket.settimeout(5.0)
        thaddeus_client_socket.connect((host, port))

        ephemeral_transmission = "Hello from client!"
        thaddeus_client_socket.sendall(ephemeral_transmission.encode("utf-8"))
        print(f"[Client Console] Successfully sent: '{ephemeral_transmission}'")

    except socket.error as emissary_network_anomaly:
        print(f"[Client Network Error]: Failed to communicate with server: {emissary_network_anomaly}")
    finally:
        if thaddeus_client_socket:
            thaddeus_client_socket.close()


def run_question_three():
    print("\n" + "=" * 60)
    print("QUESTION 3: Socket Client-Server Demonstration")
    print("=" * 60)

    cynosure_host = "127.0.0.1"
    solstice_port = 55432

    sentinel_ready_beacon = threading.Event()

    # Launch server worker in a background thread so it listens while client connects
    sentinel_thread = threading.Thread(
        target=sentinel_server_worker,
        args=(cynosure_host, solstice_port, sentinel_ready_beacon)
    )
    sentinel_thread.daemon = True
    sentinel_thread.start()

    # Await confirmation that server is actively listening
    sentinel_ready_beacon.wait(timeout=2.0)
    time.sleep(0.1)

    # Trigger client dispatch
    emissary_client_worker(cynosure_host, solstice_port)

    # Await server completion
    sentinel_thread.join(timeout=3.0)

# QUESTION 4: Random Floating-Point Numbers & Min / Max Calculation

"""
Question 4 Explanation:
We use Python's 'random' module, which functions like rolling digital polyhedral dice.
- `random.uniform(0.0, 10.0)` produces a random decimal number between 0 and 10.
- We generate a collection of 5 such random numbers into a list.
- Then, we employ Python's built-in tools `min()` and `max()` to effortlessly identify
  the nadir (minimum) and zenith (maximum) values without manual sorting loops.
"""

def run_question_four():
    print("\n" + "=" * 60)
    print("QUESTION 4: Random Floats, Min and Max Demonstration")
    print("=" * 60)

    # Generate a list of 5 random floating-point numbers between 0 and 10
    kaleidoscope_floats = [random.uniform(0.0, 10.0) for _ in range(5)]

    # Use Python's built-in functions min() and max()
    nadir_value = min(kaleidoscope_floats)
    zenith_value = max(kaleidoscope_floats)

    print("Generated list of 5 random float numbers:")
    for tally_marker, floating_val in enumerate(kaleidoscope_floats, start=1):
        print(f"  {tally_marker}. {floating_val:.4f}")

    print(f"\nMinimum value (using min()): {nadir_value:.4f}")
    print(f"Maximum value (using max()): {zenith_value:.4f}")

# QUESTION 5: Abstract Base Class (ABC) FileHandler Hierarchy

"""
Question 5 Explanation:
What is an Abstract Base Class (ABC)?
Think of `FileHandler` as an architectural charter or blueprint.
It mandates: 'Any class that claims to handle files MUST know how to read() and write().'
You cannot build a physical residence out of paper blueprints alone (you cannot instantiate an ABC).
Instead, concrete builders (like `TextFileHandler` and `BinaryFileHandler`) adhere to the charter
and supply the actual operational logic for reading and writing plain text or raw computer bytes.
"""

class FileHandler(ABC):
    """Abstract base class defining the mandatory contract for all file handlers"""

    @abstractmethod
    def read(self, parchment_identifier):
        """Abstract method to read from a file"""
        pass

    @abstractmethod
    def write(self, parchment_identifier, manuscript_payload):
        """Abstract method to write content into a file"""
        pass


class TextFileHandler(FileHandler):
    """Concrete handler for reading and writing normal human-readable text files"""

    def read(self, parchment_identifier):
        try:
            with open(parchment_identifier, "r", encoding="utf-8") as vellum_file:
                prose_content = vellum_file.read()
                print(f"[TextFileHandler] Read content from '{parchment_identifier}':\n  -> \"{prose_content.strip()}\"")
                return prose_content
        except FileNotFoundError:
            print(f"[TextFileHandler Error]: File '{parchment_identifier}' was not found.")
            return None

    def write(self, parchment_identifier, manuscript_payload):
        with open(parchment_identifier, "w", encoding="utf-8") as vellum_file:
            vellum_file.write(str(manuscript_payload))
            print(f"[TextFileHandler] Successfully wrote text to '{parchment_identifier}'")


class BinaryFileHandler(FileHandler):
    """Concrete handler for reading and writing raw binary files (images, audio, bytes)"""

    def read(self, parchment_identifier):
        try:
            with open(parchment_identifier, "rb") as chrysalis_file:
                raw_bytes = chrysalis_file.read()
                print(f"[BinaryFileHandler] Read {len(raw_bytes)} bytes from '{parchment_identifier}':\n  -> {raw_bytes}")
                return raw_bytes
        except FileNotFoundError:
            print(f"[BinaryFileHandler Error]: Binary file '{parchment_identifier}' was not found.")
            return None

    def write(self, parchment_identifier, manuscript_payload):
        # Convert string to bytes if passed as string, otherwise write bytes directly
        byte_data = manuscript_payload.encode("utf-8") if isinstance(manuscript_payload, str) else manuscript_payload
        with open(parchment_identifier, "wb") as chrysalis_file:
            chrysalis_file.write(byte_data)
            print(f"[BinaryFileHandler] Successfully wrote {len(byte_data)} bytes to '{parchment_identifier}'")


def run_question_five():
    print("\n" + "=" * 60)
    print("QUESTION 5: Abstract Base Class FileHandler Demonstration")
    print("=" * 60)

    vellum_text_handler = TextFileHandler()
    chrysalis_binary_handler = BinaryFileHandler()

    parchment_text_file = "whimsical_prose.txt"
    effervescent_binary_file = "quicksilver_bytes.bin"

    try:
        # Testing TextFileHandler
        talisman_text_data = "Exploring Python with uncommon curiosity and elegance!"
        vellum_text_handler.write(parchment_text_file, talisman_text_data)
        vellum_text_handler.read(parchment_text_file)

        print()

        # Testing BinaryFileHandler
        panoply_binary_data = b"Raw binary payload: \x00\x01\x02\xFF"
        chrysalis_binary_handler.write(effervescent_binary_file, panoply_binary_data)
        chrysalis_binary_handler.read(effervescent_binary_file)

        # Demonstrating that the abstract class itself cannot be directly instantiated:
        print("\nDemonstrating that the Abstract Base Class FileHandler cannot be instantiated directly:")
        try:
            _ = FileHandler()
        except TypeError as abstract_instantiation_error:
            print(f"BLOCKED BY PYTHON: Cannot instantiate FileHandler directly -> {abstract_instantiation_error}")

    finally:
        # Clean up created demo files
        for ephemeral_path in [parchment_text_file, effervescent_binary_file]:
            if os.path.exists(ephemeral_path):
                try:
                    os.remove(ephemeral_path)
                except Exception:
                    pass

# QUESTION 6: Class Hierarchy and Method Overriding (Vehicle, Car, Bike)

"""
Question 6 Explanation:
What is a Class Hierarchy and Method Overriding?
A class hierarchy is like a family tree.
- `Vehicle` is the ancestor (base class).
- `Car` and `Bike` are the progeny (subclasses).
The base class defines a general behavior called `move()`.
When a subclass inherits from the base class, it can either keep the generic `move()`
or provide its own customized version of `move()`.
Replacing the base class's method with a custom version in the subclass is called 'Method Overriding'.
A car moves with a roaring internal combustion engine on 4 wheels, whereas a bike moves by pedal cadence on 2 wheels.
"""

class Vehicle:
    """Base class representing any generic conveyance"""

    def __init__(self, conveyance_archetype, navigator_name):
        self.conveyance_archetype = conveyance_archetype  # Model / category
        self.navigator_name = navigator_name              # Operator / owner name

    def move(self):
        """Base method: Generic movement behavior for all vehicles"""
        print(f"[Vehicle] {self.navigator_name}'s {self.conveyance_archetype} is progressing forward along the roadway.")


class Car(Vehicle):
    """Subclass representing a car, inheriting from Vehicle"""

    def __init__(self, conveyance_archetype, navigator_name, wheel_assemblies=4):
        super().__init__(conveyance_archetype, navigator_name)
        self.wheel_assemblies = wheel_assemblies

    def move(self):
        """Overriding the move() method specifically for a car"""
        print(f"[Car] {self.navigator_name}'s car ({self.conveyance_archetype}) revs its combustion engine and cruises on {self.wheel_assemblies} wheels!")


class Bike(Vehicle):
    """Subclass representing a bicycle, inheriting from Vehicle"""

    def __init__(self, conveyance_archetype, navigator_name, has_tinkling_chime=True):
        super().__init__(conveyance_archetype, navigator_name)
        self.has_tinkling_chime = has_tinkling_chime

    def move(self):
        """Overriding the move() method specifically for a bicycle"""
        auditory_flair = "ringing its handlebar chime (karing-ring!)" if self.has_tinkling_chime else "gliding along quietly"
        print(f"[Bike] {self.navigator_name}'s bicycle ({self.conveyance_archetype}) pedals rhythmically, {auditory_flair} on 2 wheels!")


def run_question_six():
    print("\n" + "=" * 60)
    print("QUESTION 6: Class Hierarchy and Method Overriding")
    print("=" * 60)

    # Instantiate base class and both subclasses
    peregrine_conveyance = Vehicle("Vintage Locomotive", "Peregrine")
    montgomery_chariot = Car("Aston Martin DB5", "Montgomery", wheel_assemblies=4)
    gwendolyn_velocipede = Bike("Penny-Farthing", "Gwendolyn", has_tinkling_chime=True)

    # Demonstrate polymorphic method calls (overriding in action)
    print("Calling move() on each object to demonstrate method overriding:")
    fleet_of_conveyances = [peregrine_conveyance, montgomery_chariot, gwendolyn_velocipede]

    for conveyance_unit in fleet_of_conveyances:
        conveyance_unit.move()

# MAIN EXECUTION

if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("     STARTING ASSIGNMENT 2 DEMONSTRATIONS (100 MARKS)")
    print("#" * 60)

    run_question_one()
    run_question_two()
    run_question_three()
    run_question_four()
    run_question_five()
    run_question_six()

    print("\n" + "#" * 60)
    print("     ALL ASSIGNMENT 2 QUESTIONS COMPLETED SUCCESSFULLY!")
    print("#" * 60 + "\n")
