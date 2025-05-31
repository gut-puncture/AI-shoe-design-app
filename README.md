---
title: AI Shoe Designer
emoji: 🦶
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.32.0
app_file: app.py
pinned: false
license: mit
---

# 🦶 AI Shoe Designer

A modern web application that helps you design shoes using AI-powered assistance. Upload up to 10 reference images, describe your design ideas, and get detailed design specifications plus generated shoe images.

## Features

- **Multi-Image Upload**: Upload up to 10 reference images at once
- **AI-Powered Design Chat**: Get detailed shoe design specifications using OpenAI's o3 model
- **Image Generation**: Generate visual shoe designs using Fal.ai Imagen-4
- **Modern UI**: Beautiful, responsive interface with drag-and-drop file uploads
- **Vercel-Ready**: Optimized for deployment on Vercel

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **AI Models**: OpenAI o3, Fal.ai Imagen-4
- **Deployment**: Vercel

## Quick Start

### Environment Variables

Create a `.env` file in your project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
FAL_KEY=your_fal_api_key_here
```

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and go to `http://localhost:5000`

### Deploy to Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Set up environment variables in Vercel:
```bash
vercel env add OPENAI_API_KEY
vercel env add FAL_KEY
```

3. Deploy:
```bash
vercel --prod
```

## Usage

1. **Design Chat Tab**:
   - Upload up to 10 reference images (drag & drop or click to upload)
   - Describe your shoe design ideas in the text area
   - Click "Generate Design Specification"
   - Get detailed AI-generated design specifications

2. **Image Generator Tab**:
   - Copy the design prompt from the chat (auto-filled)
   - Click "Generate Shoe Design"
   - View your generated shoe image

## API Endpoints

- `GET /` - Main application interface
- `POST /api/chat` - Chat with AI for design specifications
- `POST /api/generate` - Generate shoe images

## File Structure

```
ai-shoe-designer/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── vercel.json        # Vercel configuration
├── templates/
│   └── index.html     # Main UI template
└── README.md          # This file
```

## Features Overview

### Multiple Image Upload
- Supports up to 10 images simultaneously
- Drag and drop interface
- Image preview with removal options
- Automatic file type validation

### AI Design Assistant
- Powered by OpenAI's o3 model with high reasoning effort
- Analyzes multiple reference images
- Generates detailed, manufacturable shoe specifications
- Considers brand DNA, target audience, and market trends

### Image Generation
- Uses Fal.ai Imagen-4 for high-quality shoe visualizations
- 1:1 aspect ratio optimized for shoe designs
- Real-time generation with loading indicators

### Modern UI/UX
- Responsive design for all devices
- Beautiful gradient backgrounds
- Smooth animations and transitions
- Professional tab-based interface
- Error handling and user feedback

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - feel free to use this project for your own needs!

## Support

If you encounter any issues or have questions, please open an issue in the repository.

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

## Disclaimer

This application uses external APIs (OpenAI and fal.ai) which may have usage costs. Please monitor your API usage and set appropriate limits to avoid unexpected charges.

## Support

For issues and questions:
- Check the troubleshooting section above
- Review Hugging Face Spaces documentation
- Check OpenAI and fal.ai documentation for API-specific issues 