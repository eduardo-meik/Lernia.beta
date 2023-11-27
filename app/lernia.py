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
    api_key= st.secrets["openai"]["openai_api_key"],
)

def download_file_from_url(url, local_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_path, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(f"Failed to download file: HTTP {response.status_code}")

def create_word_document(text, nombre_asignatura, campo_amplio, campo_especifico, campo_detallado, topico):
    # Create a new Document
    doc = Document()

    # Add Title
    title = doc.add_heading(level=1)
    title_run = title.add_run('Planificación proceso de enseñanza y aprendizaje')
    title_run.bold = True
    title_run.font.size = Pt(14)

    # Add Introduction Text
    intro_text = (f"A continuación, encontrará la planificación del proceso de enseñanza y aprendizaje diseñado "
                  f"por la Learnia para la asignatura {nombre_asignatura}, dentro del campo de conocimiento "
                  f"{campo_especifico}, {campo_detallado}, para los siguientes Resultados de Aprendizaje del contenido "
                  f"{topico}:")
    doc.add_paragraph(intro_text)

    # Add Custom Text
    doc.add_paragraph(text)

    # Add References
    references = (
        "Referencias\n\n"
        "- Biggs J.B., & Collis K.F. (1982). Evaluating the Quality of Learning: The SOLO Taxonomy. New York: Academic Press.\n"
        "- Campos de educación y capacitación 2013 de la CINE (ISCED-F 2013). Extraído desde https://uis.unesco.org/sites/default/files/documents/isced-fields-of-education-and-training-2013-sp.pdf\n"
        "- Quality Matters, sitio web https://www.qualitymatters.org/\n"
    )
    doc.add_paragraph(references)

    # Save the document to a BytesIO object
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Function to get chat response from GPT-4
def get_chat_response(nombre_asignatura, topico, campo_amplio, campo_especifico, campo_detallado, seed=None):
    try:
        system_message = f"Actúa como un analista experto en desarrollo y evaluación de currículos educativos con enfoque en '{campo_amplio}', '{campo_especifico}' y '{campo_detallado}'"
        user_request = f"Considerando la asignatura '{nombre_asignatura}', propone tres resultados de aprendizaje para cada nivel de la taxonomía SOLO para el tema '{topico}' utilizando la estructura Verbo+Objeto+Contexto.Make sure you provide Resultados de aprendizaje for each of the 5 levels of SOLO taxonomy, Genera 3 indicadores de logro para cada uno de los siguientes resultados de aprendizajes según estándares de calidad Quality Matters. Luego, señala las metodologías de aprendizaje activo más pertinentes  para recoger cada uno de esos indicadores de logro. Format the response as a numbered multilevel lists.Format the response as a numbered multilevel lists, avoid ###. Remove from the answer: <Verbo>: Los estudiantes podrán"

        prompt = (
            f"{system_message}. For the request: {user_request} "
             "Genera 3 indicadores de logro para cada uno de los siguientes resultados de aprendizajes según estándares de calidad Quality Matters. Luego, señala las metodologías de aprendizaje activo más pertinentes  para recoger cada uno de esos indicadores de logro. Format the response as a numbered multilevel lists"
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

def display():
    #st.title("Generador de Resultados de Aprendizaje")

    if 'selected_items' not in st.session_state:
        st.session_state.selected_items = []

    if 'response' not in st.session_state:
        st.session_state.response = None

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
            # Get the response from the chatbot
            response_text = get_chat_response(
                nombre_asignatura, topico, campo_amplio_seleccionado,
                campo_especifico_seleccionado, campo_detallado_seleccionado
            )

            # Ensure response_text is not None before proceeding
            if response_text:
                # Display the response text
                st.write(response_text)

                template_path = 'template.docx'

                # Use the selected values directly
                campo_amplio_value = campo_amplio_seleccionado
                campo_especifico_value = campo_especifico_seleccionado
                campo_detallado_value = campo_detallado_seleccionado

                # Create the Word document
                word_file = create_word_document(
                    response_text,  # Use the response text here
                    nombre_asignatura,
                    campo_amplio_value,
                    campo_especifico_value,
                    campo_detallado_value,
                    topico,
                    template_path
                )
            
            st.download_button(
                label="Descargar Resultados en Word",
                data=word_file,
                file_name="resultados_de_aprendizaje.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )







