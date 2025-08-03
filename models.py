import os
import uuid
from sqlalchemy import (
    create_engine, Column, String, Text, Date, DateTime,
    Boolean, DECIMAL, ForeignKey
)
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

def _gen_uuid():
    return str(uuid.uuid4())

class Config(Base):
    __tablename__ = "config"
    key = Column(String, primary_key=True)
    value = Column(Text, nullable=False)

class Client(Base):
    __tablename__ = "clients"
    client_id    = Column(String, primary_key=True, default=_gen_uuid)
    name         = Column(String, nullable=False, unique=True)
    address      = Column(Text)
    contact_info = Column(JSON)
    matters      = relationship("Matter", back_populates="client")
    invoices     = relationship("Invoice", back_populates="client")

class Matter(Base):
    __tablename__ = "matters"
    matter_id    = Column(String, primary_key=True, default=_gen_uuid)
    client_id    = Column(String, ForeignKey("clients.client_id"), nullable=False)
    title        = Column(String, nullable=False)
    description  = Column(Text)
    client       = relationship("Client", back_populates="matters")
    time_entries = relationship("TimeEntry", back_populates="matter")

class Staff(Base):
    __tablename__ = "staff"
    staff_id     = Column(String, primary_key=True, default=_gen_uuid)
    name         = Column(String, nullable=False)
    role         = Column(String)
    hourly_rate  = Column(DECIMAL(10,2), nullable=False)
    time_entries = relationship("TimeEntry", back_populates="staff")

class BillingCode(Base):
    __tablename__ = "billing_codes"
    code_id      = Column(String, primary_key=True, default=_gen_uuid)
    code         = Column(String, nullable=False, unique=True)
    description  = Column(String)
    default_rate = Column(DECIMAL(10,2), nullable=False)
    time_entries = relationship("TimeEntry", back_populates="billing_code")

class TimeEntry(Base):
    __tablename__ = "time_entries"
    entry_id        = Column(String, primary_key=True, default=_gen_uuid)
    datetime        = Column(DateTime, nullable=False)
    staff_id        = Column(String, ForeignKey("staff.staff_id"), nullable=False)
    matter_id       = Column(String, ForeignKey("matters.matter_id"), nullable=False)
    billing_code_id = Column(String, ForeignKey("billing_codes.code_id"), nullable=False)
    duration_hours  = Column(DECIMAL(4,1), nullable=False)
    description     = Column(Text)
    created_by      = Column(String)

    staff        = relationship("Staff", back_populates="time_entries")
    matter       = relationship("Matter", back_populates="time_entries")
    billing_code = relationship("BillingCode", back_populates="time_entries")
    invoice_line = relationship("InvoiceLineItem", back_populates="time_entry", uselist=False)

class Invoice(Base):
    __tablename__ = "invoices"
    invoice_id          = Column(String, primary_key=True, default=_gen_uuid)
    client_id           = Column(String, ForeignKey("clients.client_id"), nullable=False)
    invoice_number      = Column(String, nullable=False, unique=True)
    date_issued         = Column(Date, nullable=False)
    date_start          = Column(Date, nullable=False)
    date_end            = Column(Date, nullable=False)
    include_disbursements = Column(Boolean, default=False)
    subtotal            = Column(DECIMAL(12,2), nullable=False)
    tax_amount          = Column(DECIMAL(12,2), nullable=False)
    total_amount        = Column(DECIMAL(12,2), nullable=False)

    client     = relationship("Client", back_populates="invoices")
    line_items = relationship("InvoiceLineItem", back_populates="invoice")

class InvoiceLineItem(Base):
    __tablename__ = "invoice_line_items"
    line_item_id  = Column(String, primary_key=True, default=_gen_uuid)
    invoice_id     = Column(String, ForeignKey("invoices.invoice_id"), nullable=False)
    time_entry_id  = Column(String, ForeignKey("time_entries.entry_id"), nullable=False)
    line_description = Column(Text)
    hours           = Column(DECIMAL(4,1), nullable=False)
    rate            = Column(DECIMAL(10,2), nullable=False)
    line_total      = Column(DECIMAL(12,2), nullable=False)

    invoice    = relationship("Invoice", back_populates="line_items")
    time_entry = relationship("TimeEntry", back_populates="invoice_line")

# --- DB Init & Config Helpers ---

DB_PATH = os.getenv("TIMETRACKER_DB_PATH", "timetracker.db")
ENGINE  = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=ENGINE)

def init_db():
    Base.metadata.create_all(ENGINE)

def get_config(session, key: str) -> str | None:
    rec = session.query(Config).get(key)
    return rec.value if rec else None

def set_config(session, key: str, value: str):
    rec = session.query(Config).get(key)
    if rec:
        rec.value = value
    else:
        session.add(Config(key=key, value=value))
    session.commit()

if __name__ == "__main__":
    init_db()
    session = SessionLocal()
    # seed firm info if missing
    if not get_config(session, "firm_name"):
        set_config(session, "firm_name", "Tim Harmar Legal and Consult Solutions")
        set_config(session, "address",   "67 Hugill St., Sault Ste. Marie, ON P6A 4E6")
        set_config(session, "emails",    "tharmar@timharmar.com,kburton@timharmar.com")
    print("Database initialized.")
