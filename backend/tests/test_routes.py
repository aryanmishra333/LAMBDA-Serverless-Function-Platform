from fastapi.testclient import TestClient
from ..api.routes import router

client = TestClient(router)

def test_list_functions():
    response = client.get("/functions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_upload_function():
    test_function = {
        "name": "test_function",
        "language": "python",
        "timeout": 5,
        "code": "print('Hello, World!')"
    }
    response = client.post("/functions/", json=test_function)
    assert response.status_code == 200
    assert "function_id" in response.json()

def test_upload_verilog_function():
    """Test uploading a Verilog function with polar codec"""
    test_verilog_function = {
        "name": "polar_codec_test",
        "language": "verilog",
        "timeout": 10,
        "code": """
// Simple Verilog polar codec test
module polar_test;
    initial begin
        $display("Polar Codec Test - 128-bit data width with 50%% compression");
        $display("Input: 128 bits -> Compressed: 64 bits -> Output: 128 bits");
        $display("Compression ratio: 50.0%%");
        $finish;
    end
endmodule
"""
    }
    response = client.post("/functions/", json=test_verilog_function)
    assert response.status_code == 200
    assert "function_id" in response.json()

def test_run_function():
    # First upload a function
    test_function = {
        "name": "test_run",
        "language": "python",
        "timeout": 5,
        "code": "print('Hello, World!')"
    }
    upload_response = client.post("/functions/", json=test_function)
    function_id = upload_response.json()["function_id"]
    
    # Then try to run it
    response = client.post(f"/functions/{function_id}/run", json={"use_gvisor": False})
    assert response.status_code == 200
    assert "result" in response.json() 