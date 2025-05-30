# 🦶 AI Shoe Designer

A powerful Gradio web application that combines OpenAI's o3-2025-04-16 model for design consultation and fal.ai's Imagen4 model for image generation to help you create innovative shoe designs.

## Features

- **🗨️ Design Chat with o3**: Upload up to 10 images and chat with OpenAI's advanced o3 model to generate detailed shoe design specifications
- **🎨 Image Generator**: Use fal.ai's Imagen4 model to create visual representations of your shoe designs
- **🖼️ Multi-format Image Support**: Supports various image formats including .webp, .jpg, .png, etc.
- **💬 Interactive Chat**: Continuous conversation with context retention
- **📋 Copy-Paste Workflow**: Easy transfer of design prompts between chat and image generation

## How It Works

1. **Upload Images**: Add up to 10 reference images (shoes, sketches, inspiration photos)
2. **Describe Your Vision**: Chat with the o3 model about your design ideas
3. **Get Design Specifications**: Receive detailed, professional design prompts
4. **Generate Images**: Copy the prompts to the image generator for visual results
5. **Iterate and Refine**: Continue the conversation to perfect your design

## Deployment on Hugging Face Spaces

### Step 1: Create Hugging Face Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Configure your space:
   - **Owner**: Your Hugging Face username
   - **Space name**: `AI-shoe-design-app` (or your preferred name)
   - **SDK**: Gradio
   - **Hardware**: CPU Basic (free) or upgrade as needed
   - **Visibility**: Public

### Step 2: Get Hugging Face API Token

1. Go to [Hugging Face Settings > Access Tokens](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Configure:
   - **Name**: `github-sync` (or similar)
   - **Role**: **Write** (required for pushing to spaces)
4. Copy the generated token

### Step 3: Configure GitHub Secrets

1. Go to your GitHub repository settings
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click "New repository secret"
4. Add:
   - **Name**: `HF_TOKEN`
   - **Secret**: Your Hugging Face token from Step 2

### Step 4: Automatic Sync with GitHub Actions

This repository includes GitHub Actions that automatically sync your code to Hugging Face Spaces:

- **`.github/workflows/sync_to_hf.yml`**: Syncs code on every push to main branch
- **`.github/workflows/check_file_size.yml`**: Ensures files are under 10MB limit

The sync happens automatically when you push to the main branch. You can also trigger it manually from the GitHub Actions tab.

### Step 5: Set Environment Variables in Hugging Face

In your Hugging Face Space settings, add these environment variables:

```bash
OPENAI_API_KEY=your_openai_api_key_here
FAL_KEY=your_fal_ai_api_key_here
```

**Getting API Keys:**

- **OpenAI API Key**: 
  1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
  2. Create a new API key
  3. Ensure you have access to the o3-2025-04-16 model (may require special access)

- **fal.ai API Key**:
  1. Go to [fal.ai](https://fal.ai/)
  2. Sign up/login and go to your dashboard
  3. Generate an API key

### Step 6: Access Your Space

Once everything is configured, your Space will be available at:
`https://huggingface.co/spaces/YOUR_USERNAME/AI-shoe-design-app`

## Local Development

To run locally:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-shoe-designer.git
cd ai-shoe-designer

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your_openai_api_key"
export FAL_KEY="your_fal_ai_key"

# Run the app
python app.py
```

The app will be available at `http://localhost:7860`

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key with o3 model access | Yes |
| `FAL_KEY` | Your fal.ai API key | Yes |

## API Models Used

- **OpenAI o3-2025-04-16**: Advanced reasoning model for design consultation
- **fal.ai Imagen4/preview**: High-quality text-to-image generation

## System Requirements

- Python 3.10+
- Internet connection for API calls
- Sufficient RAM for image processing (recommended: 4GB+)

## File Structure

```
ai-shoe-designer/
├── app.py                              # Main Gradio application
├── requirements.txt                    # Python dependencies
├── README.md                          # This documentation
├── .gitignore                         # Git ignore file
├── vercel.json                        # Vercel configuration (optional)
└── .github/workflows/
    ├── sync_to_hf.yml                 # Auto-sync to Hugging Face
    └── check_file_size.yml            # File size validation
```

## Troubleshooting

### Common Issues

1. **"o3-2025-04-16 model not found"**
   - Ensure you have access to the o3 model (may require special OpenAI access)
   - Check your OpenAI API key has sufficient credits

2. **"fal.ai connection error"**
   - Verify your FAL_KEY is correct
   - Check fal.ai service status

3. **GitHub Actions sync failing**
   - Ensure `HF_TOKEN` secret is set correctly with **Write** permissions
   - Check that your Hugging Face Space exists and name matches the workflow

4. **Memory errors with large images**
   - Try reducing image file sizes before upload
   - Consider upgrading to GPU hardware on Hugging Face Spaces

5. **Slow response times**
   - Upgrade to GPU hardware on Hugging Face Spaces
   - Consider reducing the number of images uploaded simultaneously

### Performance Tips

- **For better o3 responses**: Provide clear, detailed descriptions along with your images
- **For better image generation**: Use the detailed prompts generated by o3 rather than generic descriptions
- **For faster performance**: Upgrade to GPU hardware on Hugging Face Spaces

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.

## Disclaimer

This application uses external APIs (OpenAI and fal.ai) which may have usage costs. Please monitor your API usage and set appropriate limits to avoid unexpected charges.

## Support

For issues and questions:
- Check the troubleshooting section above
- Review Hugging Face Spaces documentation
- Check OpenAI and fal.ai documentation for API-specific issues 