# Polar Codec Examples

This directory contains example Verilog functions that demonstrate the polar codec implementation with 50% compression and 128-bit data width.

## Examples

### 1. Basic Polar Codec Demo (`polar_codec_demo.v`)
A simple demonstration of polar encoding and decoding with 128-bit input data compressed to 64 bits.

### 2. Polar Codec 128-bit (`polar_codec_full.v`)
Complete implementation of the polar codec module with proper encoding and decoding functions.

## Usage

Upload these examples through the serverless platform API:

```python
import requests

# Upload the polar codec demo
with open('examples/polar_codec_demo.v', 'r') as f:
    code = f.read()

payload = {
    "name": "polar_codec_demo",
    "language": "verilog", 
    "timeout": 10,
    "code": code
}

response = requests.post("http://localhost:8000/functions/", json=payload)
function_id = response.json()["function_id"]

# Run the function
run_response = requests.post(f"http://localhost:8000/functions/{function_id}/run")
print(run_response.json()["result"])
```

## Expected Output

The polar codec demo should output:
- Original 128-bit data
- Compressed 64-bit data (50% compression)
- Decompressed 128-bit data
- Compression statistics