import streamlit as st
import pandas as pd
from db import SessionLocal, engine, Base
from models import Chemical

Base.metadata.create_all(bind=engine)
session = SessionLocal()

st.title("Chemical Inventory Tracker")

st.sidebar.header("Add / Update item")
name = st.sidebar.text_input("Name")
formula = st.sidebar.text_input("Formula")
quantity = st.sidebar.number_input("Quantity (units)", 0.0, 1e6, 0.0)
location = st.sidebar.text_input("Location")
hazard = st.sidebar.text_input("Hazard info")
if st.sidebar.button("Add item"):
    item = Chemical(name=name, formula=formula, quantity=quantity, location=location, hazard=hazard)
    session.add(item); session.commit()
    st.sidebar.success("Added")

st.header("Inventory")
items = session.query(Chemical).all()
if items:
    df = pd.DataFrame([{"id":i.id,"name":i.name,"formula":i.formula,"quantity":i.quantity,"location":i.location,"hazard":i.hazard} for i in items])
    st.dataframe(df)
    to_delete = st.number_input("Enter id to delete (or 0)", 0, 10**9, 0)
    if st.button("Delete"):
        if to_delete > 0:
            obj = session.query(Chemical).filter_by(id=int(to_delete)).first()
            if obj:
                session.delete(obj); session.commit()
                st.success("Deleted")
            else:
                st.error("Not found")
else:
    st.write("No items yet.")
