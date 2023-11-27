import re
import os
import streamlit as st
from openai import OpenAI
import requests
from docx import Document
from io import BytesIO
from . import cine2013

# Initialize OpenAI client
client = OpenAI(
    api_key=st.secrets["openai"]["openai_api_key"],
)

# Function to download a file from a URL
def download_file_from_url(url, local_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_path, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(f"Failed to download file: HTTP {response.status_code}")

# Function to create a Word document
def create_word_document(text, nombre_asignatura, campo_amplio, campo_especifico, campo_detallado, topico, firebase_url):
    local_template_path = 'local_template.docx'
    download_file_from_url(firebase_url, local_template_path)

    doc = Document(local_template_path)

    # Replace placeholders in the document
    for paragraph in doc.paragraphs:
        if '{nombre_asignatura}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{nombre_asignatura}', nombre_asignatura)
        if '{campo_amplio}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{campo_amplio}', campo_amplio)
        if '{campo_especifico}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{campo_especifico}', campo_especifico)
        if '{campo_detallado}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{campo_detallado}', campo_detallado)
        if '{topico}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{topico}', topico)

    doc.add_paragraph(text)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Function to get chat response from GPT-4
def get_chat_response(nombre_asignatura, topico, campo_amplio, campo_especifico, campo_detallado, seed=None):
    try:
        system_message = f"Actúa como un analista experto en desarrollo y evaluación de currículos educativos con enfoque en '{campo_amplio}', '{campo_especifico}' y '{campo_detallado}'"
        user_request = f"Considerando la asignatura '{nombre_asignatura}', propone tres resultados de aprendizaje para cada nivel de la taxonomía SOLO para el tema '{topico}' utilizando la estructura Verbo+Objeto+Contexto. Make sure you provide Resultados de aprendizaje for each of the 5 levels of SOLO taxonomy, Genera 3 indicadores de logro para cada uno de los siguientes resultados de aprendizajes según estándares de calidad Quality Matters. Luego, señala las metodologías de aprendizaje activo más pertinentes para recoger cada uno de esos indicadores de logro. Format the response as a numbered multilevel lists."

        prompt = (
            f"{system_message}. For the request: {user_request} "
             "Genera 3 indicadores de logro para cada uno de los siguientes resultados de aprendizajes según estándares de calidad Quality Matters. Luego, señala las metodologías de aprendizaje activo más pertinentes para recoger cada uno de esos indicadores de logro. Format the response as a numbered multilevel lists"
        )

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_request},
        ]

        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
            seed=123,
            max_tokens=4000,
            temperature=0.7,
        )

        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Main display function
def display():
    st.title("Generador de Resultados de Aprendizaje")

    nombre_asignatura = st.text_input("Nombre de la Asignatura", key="nombre_asignatura_key")
    topico = st.text_input("Introduce un Contenido", key="topico_key")
    
    campos_amplios = list(cine2013.cine2013.keys())
    campo_amplio_seleccionado = st.selectbox("Selecciona un Campo Amplio", campos_amplios)
    campos_especificos = list(cine2013.cine2013[campo_amplio_seleccionado].keys())
    campo_especifico_seleccionado = st.selectbox("Selecciona un Campo Específico", campos_especificos)
    campos_detallados = cine2013.cine2013[campo_amplio_seleccionado][campo_especifico_seleccionado]
    campo_detallado_seleccionado = st.selectbox("Selecciona un Campo Detallado", campos_detallados)

     if st.button("Generar Resultados de Aprendizaje"):
        with st.spinner('Generando resultados de aprendizaje para el tópico seleccionado...'):
            response_text = get_chat_response(
                nombre_asignatura, topico, campo_amplio_seleccionado,
                campo_especifico_seleccionado, campo_detallado_seleccionado
            )

            if response_text:
                # Firebase URL for the template
                firebase_url = "https://firebasestorage.googleapis.com/v0/b/lernia-8c0f1.appspot.com/o/template.docx?alt=media&token=2cd8e366-29c8-4699-815e-8bb5b8270d7a"
                
                word_file = create_word_document(
                    response_text,
                    nombre_asignatura,
                    campo_amplio_seleccionado,
                    campo_especifico_seleccionado,
                    campo_detallado_seleccionado,
                    topico,
                    firebase_url
                )

                st.download_button(
                    label="Descargar Resultados en Word",
                    data=word_file,
                    file_name="resultados_de_aprendizaje.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

# Running the display function
if __name__ == "__main__":
    display()







