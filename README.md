A serverless function platform that allows you to run Python and Node.js code in isolated containers, similar to AWS Lambda.

## Features

- Run Python and Node.js code in isolated Docker containers
- **NEW: Verilog support with polar codec implementation**
- Support for multiple programming languages
- **Polar codec with 50% compression and 128-bit data width**
- Container isolation for security
- Memory limits and timeout controls
- Simple REST API for function management
- Built-in code execution monitoring
- **Hardware simulation with Icarus Verilog**
## Architecture Diagram:
![WhatsApp Image 2025-04-21 at 08 50 20_dc455af8](https://github.com/user-attachments/assets/ea5b8202-4f89-4624-a408-8b6862771702)

## Prerequisites

- Python 3.10+
- Docker
- Node.js 18+ (for Node.js functions)
- **Icarus Verilog** (included in Verilog Docker image)

## Setup Instructions

1. Clone the Repository
```bash
git clone https://github.com/aryanmishra333/PES2UG22CS100_PES2UG22CS103_PES2UG22CS110_PES2UG22CS117_LAMBDA-Serverless_Function.git
```

2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Start the FastAPI Backend
```bash
uvicorn backend.main:app --reload
```

5. Start the Streamlit Frontend
```bash
streamlit run frontend/app.py
```

6. Access the App
- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs

## Supported Languages
- Python 3
- JavaScript (Node.js)
- **Verilog** (with Icarus Verilog simulator)

### New: Verilog Polar Codec Support
The platform now supports Verilog hardware description language with specialized support for:
- **Polar codec implementation** with 50% compression ratio
- **128-bit data width** processing
- Hardware simulation using Icarus Verilog
- Polar encoding/decoding algorithms for error correction

Example Verilog polar codec:
```verilog
module polar_demo;
    reg [127:0] data_in = 128'hABCDEF1234567890FEDCBA0987654321;
    reg [63:0] compressed;
    
    initial begin
        // 50% compression: 128 bits -> 64 bits
        compressed = data_in[127:64] ^ data_in[63:0];
        $display("Original: %h", data_in);
        $display("Compressed: %h", compressed);
        $finish;
    end
endmodule
```

## API Endpoints

### Function Management

- `POST /functions/` - Upload a new function
- `GET /functions/{function_id}` - Get function details
- `POST /functions/{function_id}/run` - Execute a function
- `DELETE /functions/{function_id}` - Delete a function

## Project Structure

```
lambda-serverless-function/
├── backend/
│   ├── api/           # FastAPI routes and endpoints
│   ├── core/          # Core functionality
│   ├── db/            # Database models and operations
│   ├── schemas/       # Pydantic models
│   ├── tests/         # Test cases
│   └── utils/         # Utility functions
├── docker/            # Docker configuration files
├── frontend/          # Frontend application (if any)
└── requirements.txt   # Python dependencies
```



