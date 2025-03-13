import requests
import json
import sys
import time
from PIL import Image
from io import BytesIO

# Base URL for Cloudflare WorkerAI with specific account ID
API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/f4c5b2e0774ec8a04b77e02e6f850c33/ai/run/"

# Add timeout for API requests
TIMEOUT_SECONDS = 60

# Choose a model
MODEL = "@cf/bytedance/stable-diffusion-xl-lightning"  # Fast & high-quality image gen

def generate_image(prompt, api_key):
    """ Calls Cloudflare WorkerAI to generate an image from text """
    endpoint = API_BASE_URL + MODEL
    
    # Set up headers with the API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Prepare the payload with 'prompt' as required by the API
    payload = {
        "prompt": prompt
    }
    
    print(f"Sending request to: {endpoint}")
    print(f"Headers: {headers}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        print("Sending request...")
        response = requests.post(endpoint, headers=headers, json=payload, timeout=TIMEOUT_SECONDS)
        
        # Debugging: Print response status & headers
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        if response.status_code == 200:
            # Check content type to determine how to handle the response
            content_type = response.headers.get('Content-Type', '')
            print(f"Content-Type: {content_type}")
            
            if 'image/' in content_type:
                # Direct binary image response
                print("Received direct image response")
                image_path = "generated_image.png"
                
                # Save binary image data
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"Image saved to {image_path}")
                return {"success": True, "image_path": image_path}
            
            elif 'application/json' in content_type:
                # JSON response
                print("Received JSON response")
                result = response.json()
                print(f"JSON content: {json.dumps(result, indent=2)}")
                
                if "result" in result:
                    if isinstance(result["result"], dict) and "response" in result["result"]:
                        if "base64" in result["result"]["response"]:
                            # Handle base64 encoded image
                            import base64
                            image_data = base64.b64decode(result["result"]["response"]["base64"])
                            image = Image.open(BytesIO(image_data))
                            image_path = "generated_image.png"
                            image.save(image_path)
                            print(f"Image saved to {image_path}")
                            return {"success": True, "image_path": image_path}
                    return result
                else:
                    return {"error": "Unexpected JSON format", "response": result}
            
            else:
                # Unknown content type
                print(f"Unknown content type: {content_type}")
                image_path = "generated_image.bin"
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                print(f"Raw content saved to {image_path}")
                return {"success": True, "raw_path": image_path}
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out", "message": f"The request timed out after {TIMEOUT_SECONDS} seconds"}
    except requests.exceptions.RequestException as e:
        return {"error": "Request Failed", "message": str(e)}
    except Exception as e:
        return {"error": "Unexpected error", "message": str(e), "exception_type": type(e).__name__}

# Example: Generate an image
if __name__ == "__main__":
    # Get API key from command line argument if provided, otherwise prompt
    if len(sys.argv) > 1:
        API_KEY = sys.argv[1]
        print("Using API key from command line argument")
    else:
        API_KEY = input("Enter your Cloudflare API key: ").strip()
    
    # Allow custom prompt from command line (optional second argument)
    if len(sys.argv) > 2:
        image_prompt = sys.argv[2]
    else:
        image_prompt = "inidan girl in mumbai"
    
    print(f"Generating image with prompt: {image_prompt}")
    start_time = time.time()
    print(f"Request started at: {time.strftime('%H:%M:%S')}")
    
    output = generate_image(image_prompt, API_KEY)
    
    end_time = time.time()
    print(f"Request finished at: {time.strftime('%H:%M:%S')}")
    print(f"Total time: {end_time - start_time:.2f} seconds")
    print(output)  # Expect image path or error details