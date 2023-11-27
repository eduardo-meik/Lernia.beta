import streamlit as st
from openai import OpenAI

# Initialize OpenAI client only once, not inside a function
client = OpenAI(api_key=st.secrets["openai"]["openai_api_key"])

def create_document(nombre_asignatura, campo_especifico, campo_detallado, topico, response_text):
    # Create a new Document
    doc = Document()
    
    # Title
    doc.add_heading('Planificación proceso de enseñanza y aprendizaje', 0)
    
    p = doc.add_paragraph(
        f"A continuación, encontrará la planificación del proceso de enseñanza y aprendizaje diseñado por "
        f"la Learnia para la asignatura {nombre_asignatura}, dentro del campo de conocimiento {campo_especifico}, "
        f"{campo_detallado}, para los siguientes Resultados de Aprendizaje del contenido {topico}:\n\n"
        f"Resultados de Aprendizaje, Indicadores de Logro y Metodologías de Aprendizaje Activo\n\n"
        f"A continuación, la se presenta la propuesta de indicadores de logro y metodologías de aprendizaje activo sugeridas "
        f"para alcanzar los resultados de aprendizajes definidos:\n"
        f"{response_text}\n\n"
    )
    
    # Set the font size for the paragraph
    for run in p.runs:
        run.font.size = Pt(12)
    
    # References Section
    doc.add_heading('Referencias', level=1)
    doc.add_paragraph(
        "- Biggs J.B., & Collis K.F. (1982). Evaluating the Quality of Learning: The SOLO Taxonomy. "
        "New York: Academic Press.\n"
        "- Campos de educación y capacitación 2013 de la CINE (ISCED-F 2013). Extraído desde "
        "https://uis.unesco.org/sites/default/files/documents/isced-fields-of-education-and-training-2013-sp.pdf\n"
        "- Quality Matters, sitio web https://www.qualitymatters.org/\n"
    )
    
    return doc

# Function to get chat response from GPT-4
def get_chat_response(nombre_asignatura, topico, campo_amplio, campo_especifico, campo_detallado):
    system_message = (
        f"Act as an expert analyst in the development and evaluation of educational curricula "
        f"focused on '{campo_amplio}', '{campo_especifico}', and '{campo_detallado}'."
    )
    user_request = (
        f"Considering the subject '{nombre_asignatura}', propose three learning outcomes for "
        f"each level of the SOLO taxonomy for the topic '{topico}' using the structure Verb + Object + Context. "
        f"Ensure you provide 'Resultados de aprendizaje' for each of the 5 levels of the SOLO taxonomy, generate 3 achievement "
        f"indicators for each of the learning outcomes according to Quality Matters standards. Then, indicate the most "
        f"relevant active learning methodologies for collecting each of those indicators. Format the response as numbered multilevel lists."
    )

    prompt = f"{system_message}. For the request: {user_request}"

    try:
        response = client.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_request},
            ],
            max_tokens=4000,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def display():
    # Initialize session state variables
    if 'response' not in st.session_state:
        st.session_state.response = None

    nombre_asignatura = st.text_input("Nombre de la Asignatura", key="nombre_asignatura_key")
    topico = st.text_input("Introduce un Contenido", key="topico_key")

    # Dictionary cine2013.cine2013 should be defined somewhere in the module cine2013.py
    cmapos_amplios = list(cine2013.cine2013.keys())
    campo_amplio_seleccionado = st.selectbox("Selecciona un Campo Amplio", cmapos_amplios)
    campos_especificos = list(cine2013.cine2013[campo_amplio_seleccionado].keys())
    campo_especifico_seleccionado = st.selectbox("Selecciona un Campo Específico", campos_especificos)
    campos_detallados = cine2013.cine2013[campo_amplio_seleccionado][campo_especifico_seleccionado]
    campo_detallado_seleccionado = st.selectbox("Selecciona un Campo Detallado", campos_detallados)

    if st.button("Generar Resultados de Aprendizaje"):
        with st.spinner('Generando... Esto puede tomar unos minutos.'):
            response_text = get_chat_response(
                nombre_asignatura, topico, campo_amplio_seleccionado,
                campo_especifico_seleccionado, campo_detallado_seleccionado
            )
            if response_text:
        st.write(response_text)
        
        # Call function to create the document
        doc = create_document(
            nombre_asignatura, campo_especifico_seleccionado,
            campo_detallado_seleccionado, topico, response_text
        )
        
        # Generate and show the download link
        st.download_button(
                label="Descargar Resultados en Word",
                data=word_file,
                file_name="resultados_de_aprendizaje.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

if __name__ == "__main__":
    display()





