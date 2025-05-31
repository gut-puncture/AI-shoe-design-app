import gradio as gr
import openai
import fal_client
import os
import base64
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

def chat_with_o3(message, image_file):
    """Chat with OpenAI o3 model with image support"""
    if not message and not image_file:
        return "Please provide a message or upload an image."
    
    try:
        # Prepare messages for the API
        messages = [{"role": "developer", "content": SYSTEM_PROMPT}]
        
        # Prepare current message with images
        current_message_content = []
        
        # Add text
        if message:
            current_message_content.append({"type": "text", "text": message})
        
        # Add image if provided
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
                return f"Error processing image: {e}"
        
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

# Create the main Gradio interface using simple approach
demo = gr.TabbedInterface([
    gr.Interface(
        fn=chat_with_o3,
        inputs=[
            gr.Textbox(label="Your Message", placeholder="Describe your shoe design ideas...", lines=3),
            gr.File(label="Upload Image", type="filepath")
        ],
        outputs=gr.Textbox(label="AI Response", lines=10),
        title="🗨️ Design Chat with o3",
        description="Upload an image and describe your design ideas. The AI will create detailed design specifications.",
        article="Upload an image of shoes, sketches, or inspiration and describe your design ideas."
    ),
    gr.Interface(
        fn=generate_image_with_fal,
        inputs=gr.Textbox(label="Design Prompt", placeholder="Paste prompt from chat...", lines=8),
        outputs=gr.Image(label="Generated Shoe Design"),
        title="🎨 Image Generator", 
        description="Generate visual representations of your shoe design using detailed prompts.",
        article="Copy the design prompt from the chat above and generate your shoe image."
    )
], ["Design Chat", "Image Generator"], title="🦶 AI Shoe Designer")

# Launch the app
if __name__ == "__main__":
    demo.launch() 