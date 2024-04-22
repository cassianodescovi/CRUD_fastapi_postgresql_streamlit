
import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")

st.image("logo.jpg", width=200)

st.title("Product Management")


# Helper function to display detailed error messages
def show_response_message(response):
    if response.status_code == 200:
        st.success("Operation carried out successfully!")
    else:
        try:
            data = response.json()
            if "detail" in data:
                # If the error is a list, extract the messages from each error
                if isinstance(data["detail"], list):
                    errors = "\n".join([error["msg"] for error in data["detail"]])
                    st.error(f"Erro: {errors}")
                else:
                    # Otherwise, show the error message directly
                    st.error(f"Erro: {data['detail']}")
        except ValueError:
            st.error("Unknown error. Unable to decode the response.")


# Add Product
with st.expander("Add a New Product"):
    with st.form("new_product"):
        name = st.text_input("Product's name")
        description = st.text_area("Product Description")
        price = st.number_input("Price", min_value=0.01, format="%f")
        category = st.selectbox(
            "Category",
            ["Electronic", "Household appliance", "Furniture", "Clothes", "Shoes"],
        )
        email_supplier = st.text_input("Supplier Email")
        submit_button = st.form_submit_button("Add Product")

        if submit_button:
            response = requests.post(
                "http://backend:8000/products/",
                json={
                    "name": name,
                    "description": description,
                    "price": price,
                    "category": category,
                    "email_supplier": email_supplier,
                },
            )
            show_response_message(response)
# View Products
with st.expander("# View Products"):
    if st.button("View All Products"):
        response = requests.get("http://backend:8000/products/")
        if response.status_code == 200:
            product = response.json()
            df = pd.DataFrame(product)

            df = df[
                [
                    "id",
                    "name",
                    "description",
                    "price",
                    "categoria",
                    "email_supplier",
                    "created_at",
                ]
            ]

            # Display the DataFrame without the index
            st.write(df.to_html(index=False), unsafe_allow_html=True)
        else:
            show_response_message(response)

with st.expander("Get Details of a Product"):
    get_id = st.number_input("Product ID", min_value=1, format="%d")
    if st.button("Search Product"):
        response = requests.get(f"http://backend:8000/products/{get_id}")
        if response.status_code == 200:
            product = response.json()
            df = pd.DataFrame([product])

            df = df[
                [
                    "id",
                    "name",
                    "description",
                    "price",
                    "categoria",
                    "email_supplier",
                    "created_at",
                ]
            ]

            st.write(df.to_html(index=False), unsafe_allow_html=True)
        else:
            show_response_message(response)

# Delete Product
with st.expander("Delete Product"):
    delete_id = st.number_input("Product ID to Delete", min_value=1, format="%d")
    if st.button("Delete Product"):
        response = requests.delete(f"http://backend:8000/products/{delete_id}")
        show_response_message(response)

# Update Product
with st.expander("Update Product"):
    with st.form("update_product"):
        update_id = st.number_input("Product ID", min_value=1, format="%d")
        new_name = st.text_input("New Product Name")
        new_description = st.text_area("New Product Description")
        new_price = st.number_input(
            "New Price",
            min_value=0.01,
            format="%f",
        )
        new_categoria = st.selectbox(
            "New Category",
            ["Electronic", "Household appliance", "Furniture", "Clothes", "Shoes"],
        )
        new_email = st.text_input("New Supplier Email")

        update_button = st.form_submit_button("Update Product")

        if update_button:
            update_data = {}
            if new_name:
                update_data["name"] = new_name
            if new_description:
                update_data["description"] = new_description
            if new_price > 0:
                update_data["price"] = new_price
            if new_email:
                update_data["email_supplier"] = new_email
            if new_categoria:
                update_data["categoria"] = new_categoria

            if update_data:
                response = requests.put(
                    f"http://backend:8000/products/{update_id}", json=update_data
                )
                show_response_message(response)
            else:
                st.error("No information provided for update")
