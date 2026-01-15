from PIL import Image

def hide_text(image_path, text, output_path):
    try:
        img = Image.open(image_path)
        binary_text = ''.join([format(ord(i), '08b') for i in text]) + '1111111111111110'
        pixels = img.getdata()
        new_pixels = []
        idx = 0
        for p in pixels:
            if idx < len(binary_text):
                r, g, b = p[:3]
                nr = (r & ~1) | int(binary_text[idx])
                new_p = (nr, g, b)
                if len(p) == 4: new_p += (p[3],)
                new_pixels.append(new_p)
                idx += 1
            else:
                new_pixels.append(p)
        img.putdata(new_pixels)
        img.save(output_path)
        return f"Saved: {output_path}"
    except Exception as e: return f"Error: {e}"

def extract_text(image_path):
    try:
        img = Image.open(image_path)
        binary = "".join([str(p[0] & 1) for p in img.getdata()])
        chars = []
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if byte == "11111111": break
            chars.append(chr(int(byte, 2)))
        return "".join(chars)
    except Exception as e: return f"Error: {e}"
