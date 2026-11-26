import importlib.machinery
import importlib.util
import sqlite3
import sys
import unittest
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "contactsls"
loader = importlib.machinery.SourceFileLoader("contactsls_module", str(path))
spec = importlib.util.spec_from_loader(loader.name, loader)
module = importlib.util.module_from_spec(spec)
sys.modules[loader.name] = module
loader.exec_module(module)


class RelationshipTests(unittest.TestCase):
    def test_entity_discriminator_is_not_contact_id(self):
        db = sqlite3.connect(":memory:")
        db.execute("CREATE TABLE ZABCDEMAILADDRESS (Z_PK INTEGER, ZOWNER INTEGER, Z22_OWNER INTEGER, ZADDRESS TEXT)")
        db.execute("CREATE TABLE ZABCDPHONENUMBER (Z_PK INTEGER, ZOWNER INTEGER, Z22_OWNER INTEGER, ZFULLNUMBER TEXT)")
        db.execute("CREATE TABLE ZABCDNOTE (ZCONTACT INTEGER, Z22_CONTACT INTEGER, ZTEXT TEXT)")
        for table, value in (("ZABCDEMAILADDRESS", "email"), ("ZABCDPHONENUMBER", "phone")):
            db.execute(f"INSERT INTO {table} VALUES (1, 22, 22, ?)", (value,))
            db.execute(f"INSERT INTO {table} VALUES (2, 35, 22, 'other')")
        db.executemany("INSERT INTO ZABCDNOTE VALUES (?, 22, ?)", [(22, "note"), (35, "other")])
        self.assertEqual(module.labelled_values(db, "ZABCDEMAILADDRESS", "ZADDRESS", 22), ("email",))
        self.assertEqual(module.labelled_values(db, "ZABCDPHONENUMBER", "ZFULLNUMBER", 22), ("phone",))
        self.assertEqual(module.contact_notes(db, 22), "note")


if __name__ == "__main__":
    unittest.main()
