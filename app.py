import gradio as gr
import openai
import fal_client
import os
import base64
from typing import List, Tuple, Optional
from PIL import Image
import io

# Initialize clients
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System prompt for o3 model
SYSTEM_PROMPT = """You are **"PromptForge-O3-Footwear,"** an elite product-design assistant.
Your sole task: given (a) up to 10 user-supplied reference images, (b) OPTIONAL brand names, and (c) OPTIONAL creative notes, you must return **one—and only one—finished image-generation prompt** ready for Fal.ai Imagen-4 (or any best-in-class model) that depicts a brand-new **SHOE** concept the label can manufacture.
The user will paste your prompt directly into the image tool, so *no other text* (analysis, greetings, Markdown) is allowed in your answer.

––––––  METHODOLOGY  ––––––

1. **Extract design DNA**
   • From EACH reference image and brand, identify recurring signatures—silhouette, proportions, seam placement, collar/lapel geometry, drape or rigidity, fabric hand, surface treatments, palette, hardware finish, logo language, styling mood.
   • Determine the common aesthetic thread (e.g., quiet-luxury minimalism, sculptural hardware, earthy palette).
   • Translate textile or garment cues into footwear equivalents (e.g., satin wrap → fluid vamp fold; pin-stripe shirting → subtle stitched channel lines).

2. **Contextualise the wearer**
   • Infer target consumer profile (age range, gender identity, locale, lifestyle, price band).
   • Consider current market trends and comfort/utility expectations for that audience.

3. **Ideate manufacturable footwear**
   • Select ONE logical silhouette (e.g., relaxed square-toe mule, low-block heel slide, minimalist thong sandal, sculpted kitten-heel pump, sleek cup-sole sneaker) that fits the brand's line-up.
   • Specify: upper material + treatment, colourway, lining, heel/sole build, outsole tread, hardware/logo application, stitch detailing, edge finish, closure system, last shape, heel height, fit notes.
   • Ensure all elements are technically feasible with standard factory capabilities.

4. **Craft the Fal.ai prompt** – structure EXACTLY as below, each block on its own line so Imagen-4 parses cleanly:
   ① **Scene directive & consumer** – concise line describing clean studio setup (e.g., "45-degree hero shot on seamless neutral ground, calm softbox lighting") + customer profile.
   ② **Shoe specification** – bullet-style string detailing every component in this order: silhouette, upper material/colour/finish, toe shape, vamp treatment, closure/hardware, lining, insole branding, heel style + height, outsole/tread, edge finish.
   ③ **Material call-outs** – 2–3 seamless macro swatch descriptors (e.g., "liquid ecru satin, subtle weft sheen" / "smooth bone-white calf, micro-edge paint").
   ④ **Colour-chip strip** – 4–6 HEX codes light→dark from merged palette.
   ⑤ **Stylistic adjectives** – 5–10 comma-separated modifiers (e.g., quiet-luxury, Scandinavian restraint, clean negative space, editorial daylight, muted reflections).
   ⑥ **Technical directives** – 3:2 aspect, 4K resolution, natural colour rendering, true shadows, no HDR artefacts.
   ⑦ **Negative prompt** – forbid brand logos, noisy backgrounds, clutter, garish hues, cartoonish styling.

5. **Clarify only if essential**
   • Ask a follow-up *only* if a critical manufacturing or consumer detail is missing. Otherwise, proceed.

6. **Output rules**
   • Begin immediately with the finished Fal.ai prompt blocks—no title line, no "Prompt:" prefix.
   • Provide **one** shoe image concept only; no mood boards, no multiple angles.
   • Keep under 650 tokens.

Failure to follow any of the above invalidates the output. Now wait for the user's references, then comply.
"""

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string for OpenAI API"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def chat_with_o3(message, *image_files):
    """Chat with OpenAI o3 model with image support"""
    if not message and not any(image_files):
        return "Please provide a message or upload images."
    
    try:
        # Prepare messages for the API
        messages = [{"role": "developer", "content": SYSTEM_PROMPT}]
        
        # Prepare current message with images
        current_message_content = []
        
        # Add text
        if message:
            current_message_content.append({"type": "text", "text": message})
        
        # Add images (up to 10)
        if image_files:
            for image_file in image_files[:10]:
                if image_file is not None:
                    try:
                        # Open and process the image
                        pil_img = Image.open(image_file)
                        base64_image = encode_image_to_base64(pil_img)
                        current_message_content.append({
                            "type": "image_url",
                            "image_url": {"url": base64_image}
                        })
                    except Exception as e:
                        print(f"Error processing image: {e}")
        
        if current_message_content:
            messages.append({"role": "user", "content": current_message_content})
        
        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model="o3-2025-04-16",
            messages=messages,
            max_completion_tokens=4000,
            reasoning_effort="high"
        )
        
        assistant_response = response.choices[0].message.content
        return assistant_response
        
    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}"

def generate_image_with_fal(prompt):
    """Generate image using fal.ai imagen4/preview model"""
    if not prompt or not prompt.strip():
        return None
        
    try:
        # Call fal.ai API
        result = fal_client.subscribe(
            "fal-ai/imagen4/preview",
            arguments={
                "prompt": prompt,
                "aspect_ratio": "1:1",
                "num_images": 1
            }
        )
        
        if result and "images" in result and len(result["images"]) > 0:
            image_url = result["images"][0]["url"]
            return image_url
        else:
            return None
            
    except Exception as e:
        return None

# Create the main Gradio interface
with gr.Blocks(title="🦶 AI Shoe Designer", theme=gr.themes.Soft()) as demo:
    
    gr.Markdown("""
    # 🦶 AI Shoe Designer
    
    Welcome to the AI Shoe Designer! This tool helps you create innovative shoe designs using cutting-edge AI.
    
    ## How to use:
    1. **Design Chat**: Upload up to 10 images and chat with our AI to generate detailed design specifications
    2. **Image Generator**: Take the generated prompts and create visual representations of your shoe designs
    """)
    
    with gr.Tab("🗨️ Design Chat with o3"):
        gr.Markdown("""
        ### Chat with OpenAI's o3 Model
        Upload up to 10 images of shoes, sketches, or inspiration and describe your design ideas. 
        The AI will help you create detailed design specifications and prompts for shoe creation.
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                # User input
                chat_message = gr.Textbox(
                    label="Your Message",
                    placeholder="Describe your shoe design ideas, ask questions, or request modifications...",
                    lines=3
                )
                
                # File uploads (up to 10 images)
                with gr.Row():
                    img1 = gr.File(label="Image 1", file_types=["image"])
                    img2 = gr.File(label="Image 2", file_types=["image"])
                    img3 = gr.File(label="Image 3", file_types=["image"])
                    img4 = gr.File(label="Image 4", file_types=["image"])
                    img5 = gr.File(label="Image 5", file_types=["image"])
                
                with gr.Row():
                    img6 = gr.File(label="Image 6", file_types=["image"])
                    img7 = gr.File(label="Image 7", file_types=["image"])
                    img8 = gr.File(label="Image 8", file_types=["image"])
                    img9 = gr.File(label="Image 9", file_types=["image"])
                    img10 = gr.File(label="Image 10", file_types=["image"])
                
                chat_btn = gr.Button("Send Message", variant="primary")
            
            with gr.Column(scale=2):
                # AI response
                chat_output = gr.Textbox(
                    label="AI Response",
                    lines=15,
                    interactive=False
                )
    
    with gr.Tab("🎨 Image Generator"):
        gr.Markdown("""
        ### Generate Shoe Images with fal.ai
        Copy a detailed design prompt from the chat above and paste it here to generate visual representations of your shoe design.
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                image_prompt = gr.Textbox(
                    label="Design Prompt",
                    placeholder="Paste the detailed design prompt from the chat above...",
                    lines=8
                )
                generate_btn = gr.Button("Generate Image", variant="primary")
            
            with gr.Column(scale=1):
                generated_image = gr.Image(
                    label="Generated Shoe Design",
                    height=400
                )
    
    # Event handlers
    chat_btn.click(
        fn=chat_with_o3,
        inputs=[chat_message, img1, img2, img3, img4, img5, img6, img7, img8, img9, img10],
        outputs=chat_output
    )
    
    generate_btn.click(
        fn=generate_image_with_fal,
        inputs=image_prompt,
        outputs=generated_image
    )

# Launch the app
if __name__ == "__main__":
    demo.launch() 