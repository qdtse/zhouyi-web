from PIL import Image
import os

img_path = r"D:\Users\sugarworm\.claude\skills\zhouyi-web\public\paypal.png"

try:
    if os.path.exists(img_path):
        print(f"Processing {img_path}...")
        img = Image.open(img_path)
        img = img.convert("RGBA")
        
        # Create a white background image
        background = Image.new("RGBA", img.size, (255, 255, 255, 255))
        
        # Paste the original image on top of the white background
        # using the alpha channel as a mask
        background.paste(img, (0, 0), img)
        
        # Convert to RGB (removes alpha channel)
        final_img = background.convert("RGB")
        
        # Save it back
        final_img.save(img_path, "PNG")
        print("Successfully changed background to white.")
    else:
        print("Image not found.")
except Exception as e:
    print(f"Error: {e}")
