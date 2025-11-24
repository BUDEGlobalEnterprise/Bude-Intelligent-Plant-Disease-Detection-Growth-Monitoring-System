import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Bude Intelligent System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main {
        background-color: #f5fdf5;
    }
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 10px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        color: white;
    }
    h1 {
        color: #1b5e20;
    }
    .report-box {
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #2e7d32;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/628/628283.png", width=100)
    st.title("🌿 Bude Intelligent System")
    st.markdown("---")
    
    # Secure API Key Input
    api_key = st.text_input("Enter Google Gemini API Key", type="password")
    st.caption("Get your key from [Google AI Studio](https://aistudio.google.com/)")
    
    st.markdown("---")
    
    # Mode Selection
    st.subheader("🛠️ Select Function")
    mode = st.radio("Choose Mode:", ["🦠 Disease Detection", "📈 Growth Monitoring"])
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    model_version = st.selectbox("Select Model", ["gemini-2.0-flash", "gemini-1.5-flash"])
    
    st.markdown("---")
    st.info("💡 **Tip:** Ensure the plant is well-lit. For growth monitoring, try to include the whole plant in the frame.")

# --- MAIN APP LOGIC ---

if mode == "🦠 Disease Detection":
    st.title("🦠 Disease Detection")
    st.markdown("### Upload a leaf photo to diagnose diseases and get treatment plans.")
else:
    st.title("📈 Growth Monitoring")
    st.markdown("### Upload a plant photo to assess growth stage, health, and vitality.")

# 1. Image Input (Upload or Camera)
col1, col2 = st.columns([1, 1])

with col1:
    tab1, tab2 = st.tabs(["📤 Upload Image", "📸 Take Photo"])
    
    image_input = None
    
    with tab1:
        uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image_input = uploaded_file

    with tab2:
        camera_file = st.camera_input("Take a picture")
        if camera_file:
            image_input = camera_file

    # Display Image if available
    if image_input:
        image = Image.open(image_input)
        st.image(image, caption="Uploaded Plant Image", use_column_width=True)

# 2. Analysis Logic
with col2:
    st.write("## 🔍 Analysis Results")
    
    if image_input:
        if not api_key:
            st.warning("⚠️ Please enter your API Key in the sidebar to proceed.")
        else:
            # Dynamic button text based on mode
            analyze_button = st.button(f"Analyze for {mode.split(' ')[1]}")
            
            if analyze_button:
                try:
                    # Configure API
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(model_version)

                    with st.spinner("🤖 Consulting the AI Botanist..."):
                        
                        # Define Prompts based on Mode
                        if mode == "🦠 Disease Detection":
                            prompt = """
                            Act as an expert agricultural botanist. Analyze the uploaded plant leaf image.
                            
                            Provide the output in the following structured Markdown format:
                            
                            1. **Disease Name:** (Identify the disease. If healthy, state "Healthy").
                            2. **Confidence Level:** (High/Medium/Low based on visual clarity).
                            3. **Symptoms Observed:** (Briefly describe spots, discoloration, or curling).
                            4. **Causes:** (Fungal, bacterial, pest, or environmental).
                            5. **Recommended Treatment:** (Organic and chemical remedies).
                            6. **Prevention:** (How to stop it from coming back).
                            
                            If the image is not a plant leaf, simply return: "⚠️ I cannot identify a plant in this image. Please upload a clear photo of a leaf."
                            """
                        else: # Growth Monitoring
                            prompt = """
                            Act as an expert agricultural botanist. Analyze the uploaded plant image for growth and vitality.
                            
                            Provide the output in the following structured Markdown format:
                            
                            1. **Plant Identification:** (Identify the plant species).
                            2. **Growth Stage:** (e.g., Seedling, Vegetative, Flowering, Fruiting).
                            3. **Health Assessment:** (Describe the overall vigor, leaf color, and stem strength).
                            4. **Estimated Age:** (Provide a rough estimate if possible, e.g., "2-3 weeks" or "Mature").
                            5. **Care Recommendations:** (Watering, lighting, and nutrient advice for this specific stage).
                            6. **Next Milestones:** (What to expect next in the growth cycle).
                            
                            If the image is not a plant, simply return: "⚠️ I cannot identify a plant in this image."
                            """

                        # Process image
                        img_byte_arr = io.BytesIO()
                        image.save(img_byte_arr, format='PNG')
                        img_byte_arr = img_byte_arr.getvalue()
                        
                        payload = {
                            "mime_type": "image/png",
                            "data": img_byte_arr
                        }

                        # Generate response
                        response = model.generate_content([prompt, payload])
                        
                        # Display Results
                        st.markdown(f'<div class="report-box">{response.text}</div>', unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
                    
    else:
        st.info("👈 Please upload an image to start.")

# --- FOOTER ---
st.markdown("---")
st.markdown("<center>⚠️ AI can make mistakes. Always consult a professional for valuable crops.</center>", unsafe_allow_html=True)