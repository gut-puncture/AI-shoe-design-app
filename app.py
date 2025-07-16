from flask import Flask, request, jsonify, render_template
import openai
import fal_client
import os
import base64
from PIL import Image
import io
import tempfile
from werkzeug.utils import secure_filename
import logging

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize clients
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System prompt for o3 model
SYSTEM_PROMPT = """You are **"PromptForge-O3-Footwear,"** an elite product-design assistant.
Your sole task: given (a) up to 10 user-supplied reference images, (b) OPTIONAL brand names, and (c) OPTIONAL creative notes, you must return **one—and only one—finished image-generation prompt** ready for Fal.ai Imagen-4-Ultra (or any best-in-class model) that depicts a brand-new **SHOE** concept the label can manufacture.
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

def call_openai_with_fallback(messages):
    """Call OpenAI API with model fallback logic"""
    # Try o3 first, then fall back to other models if access is restricted
    models_to_try = ["o3-2025-04-16", "gpt-4o", "gpt-4-turbo"]
    
    for model in models_to_try:
        try:
            logger.info(f"Trying model: {model}")
            
            if model == "o4-mini-2025-04-16":
                response = openai_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_completion_tokens=4000,
                    reasoning_effort="high"
                )
            else:
                response = openai_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=4000,
                    temperature=0.7
                )
            
            logger.info(f"Successfully used model: {model}")
            return response, model
            
        except openai.NotFoundError as e:
            logger.warning(f"Model {model} not found or not accessible: {str(e)}")
            continue
        except openai.AuthenticationError as e:
            logger.error(f"Authentication error with {model}: {str(e)}")
            raise e
        except openai.RateLimitError as e:
            logger.warning(f"Rate limit exceeded for {model}: {str(e)}")
            continue
        except Exception as e:
            logger.warning(f"Error with {model}: {str(e)}")
            continue
    
    raise Exception("All models failed or are not accessible")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/favicon.png')
def favicon_png():
    return '', 204

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """API endpoint for chat with OpenAI models"""
    try:
        message = request.form.get('message', '')
        files = request.files.getlist('images')
        
        if not message and not files:
            return jsonify({'error': 'Please provide a message or upload images.'}), 400
        
        # Prepare messages for the API
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Prepare current message with images
        current_message_content = []
        
        # Add text
        if message:
            current_message_content.append({"type": "text", "text": message})
        
        # Add images if provided (up to 10)
        if files:
            processed_images = 0
            for file in files[:10]:  # Limit to 10 images
                if file and file.filename:
                    try:
                        # Open and process the image
                        pil_img = Image.open(file.stream)
                        base64_image = encode_image_to_base64(pil_img)
                        current_message_content.append({
                            "type": "image_url",
                            "image_url": {"url": base64_image}
                        })
                        processed_images += 1
                    except Exception as e:
                        logger.warning(f"Failed to process image: {str(e)}")
                        continue  # Skip invalid images
        
        if current_message_content:
            messages.append({"role": "user", "content": current_message_content})
        
        # Call OpenAI API with fallback logic
        response, used_model = call_openai_with_fallback(messages)
        
        assistant_response = response.choices[0].message.content
        
        # Add model info to response for debugging
        response_data = {
            'response': assistant_response,
            'model_used': used_model
        }
        
        return jsonify(response_data)
        
    except openai.AuthenticationError as e:
        logger.error(f"Authentication error: {str(e)}")
        return jsonify({'error': f'Authentication failed. Please check your API key: {str(e)}'}), 401
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/generate', methods=['POST'])
def generate_image_api():
    """API endpoint for image generation using fal.ai"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        
        if not prompt:
            return jsonify({'error': 'Please provide a prompt.'}), 400
        
        # Call fal.ai API
        result = fal_client.subscribe(
            "fal-ai/imagen4/preview/ultra",
            arguments={
                "prompt": prompt,
                "aspect_ratio": "1:1",
                "num_images": 1
            }
        )
        
        if result and "images" in result and len(result["images"]) > 0:
            image_url = result["images"][0]["url"]
            return jsonify({'image_url': image_url})
        else:
            return jsonify({'error': 'Failed to generate image'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Error generating image: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True) 
