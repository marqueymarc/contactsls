import importlib.machinery
import importlib.util
import sqlite3
import sys
import unittest
import datetime as dt
from dataclasses import replace
from unittest.mock import patch
from types import SimpleNamespace
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "contactsls"
loader = importlib.machinery.SourceFileLoader("contactsls_module", str(path))
spec = importlib.util.spec_from_loader(loader.name, loader)
module = importlib.util.module_from_spec(spec)
sys.modules[loader.name] = module
loader.exec_module(module)


class RelationshipTests(unittest.TestCase):
    def test_earliest_date_requires_unambiguous_identifier_and_name(self):
        early = dt.datetime(2020, 1, 1, tzinfo=dt.timezone.utc)
        late = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
        current = module.Contact('Leonor Blum', late, late, '', (), ('mobile: (410) 591-0547',), '', 'new', record_created=late, creation_source='new')
        old = replace(current, name='Leonore Blum', created=early, phones=('mobile: +1 (410) 591-0547',), source='old')
        result = module.apply_earliest_dates([current], [current, old])[0]
        self.assertEqual(result.created, early)
        self.assertEqual(result.record_created, late)
        self.assertEqual(result.creation_source, 'old')
        shared = replace(old, name='Other Person')
        self.assertEqual(module.apply_earliest_dates([current], [current, old, shared])[0].created, late)
        self.assertEqual(module.apply_earliest_dates([replace(current, phones=())], [old])[0].created, late)

    def test_active_source_filter_and_historical_override(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for source in ('ACTIVE', 'OLD'):
                (root / source).mkdir()
                (root / source / 'AddressBook-v22.abcddb').touch()
            with patch.object(module, 'CONTACTS_ROOT', root), patch.object(module.subprocess, 'run', return_value=SimpleNamespace(stdout='ACTIVE:ABAccount\n')):
                self.assertEqual([p.parent.name for p in module.database_paths(None)], ['ACTIVE'])
                self.assertEqual({p.parent.name for p in module.database_paths(None, True)}, {'ACTIVE', 'OLD'})

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
