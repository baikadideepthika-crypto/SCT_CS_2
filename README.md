# Image Encryption Tool - SkillCraft Technology

## Task 2 - Cyber Security Internship

A Python GUI application that encrypts and decrypts images using pixel manipulation techniques.

## Features
- Encrypt images using XOR pixel manipulation
- Decrypt images back to original using the same key
- Swap adjacent pixels for extra scrambling
- Combine XOR + Swap for stronger encryption
- Live side-by-side preview of original vs processed image
- Save encrypted/decrypted images to disk

## How It Works
Every image is made of pixels with RGB values (0-255).
The tool applies XOR operation on each pixel with a secret key:

- Encrypt: pixel XOR key = scrambled pixel
- Decrypt: scrambled pixel XOR key = original pixel

XOR is reversible — applying it twice with the same key restores the original!

## How to Run
```bash
pip install Pillow
py image_encryption.py
```

## Tech Stack
- Python 3
- Tkinter (GUI)
- Pillow (Image Processing)

## Author
Baikadi Deepthika - SkillCraft Technology Cyber Security Intern
