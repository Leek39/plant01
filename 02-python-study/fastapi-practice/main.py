from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def hello():
    return {"message" : "Hello World~"}

@app.get("/user/{name}")
def hello_user(name: str):
    """
    Path parameter handling with type validation
    - {name} syntax (not <name> like Flask)
    - Type hints provide automatic validation
    - Generates accurate API documentation
    """
    return {"message": "Hello! " + name}

# Synchronous endpoint (similar to Spring MVC)
# Runs in thread pool internally
@app.get("/sync")
def sync_endpoint():
    """
    Synchronous endpoint processing
    - Blocks the thread during execution
    - Similar to traditional Spring MVC controllers
    - Good for CPU-bound operations
    """
    import time
    time.sleep(2)  # Simulate blocking operation
    return {"message": "sync processing completed", "type": "blocking"}



# Asynchronous endpoint (similar to Spring WebFlux)
# Runs in event loop
@app.get("/async")
async def async_endpoint():
    """
    Asynchronous endpoint processing
    - Non-blocking execution
    - Similar to Spring WebFlux reactive programming
    - Excellent for I/O-bound operations
    """
    import asyncio
    await asyncio.sleep(2)  # Simulate non-blocking operation
    return {"message": "async processing completed", "type": "non-blocking"}



# Run with: uvicorn main:app --reload
