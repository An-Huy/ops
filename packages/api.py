from fastapi import FastAPI, HTTPException
from packages.utils import opsclt
import uvicorn

#import sys
#sys.setrecursionlimit(5000)

app = FastAPI()
ops = opsclt.Openstack()

@app.get("/api/v3/servers")
async def get_all_servers(page: int = 1, limit: int = 5):
    try: 
        servers = ops._get_all_servers(page, limit)
        return servers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/v3/servers/{ins_id}")
async def get_all_server_by_id(ins_id: str):
    try: 
        server = ops._get_server_by_id(ins_id)
        return server
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/v3/images")
async def get_all_images():
    try: 
        images = ops._get_images()
        return images
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/v3/flavors")
async def get_all_flavors():
    try: 
        flavors = ops._get_flavors()
        return flavors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/v3/networks")
async def get_all_networks():
    try: 
        networks = ops._get_networks()
        return networks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v3/create_server")
async def create_server(name: str, size: int, image_id: str, flavor_id: str, network_id: str):
    try:
        server = ops._create_server(name, size, image=image_id, flavor=flavor_id, network=network_id)
        return server
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v3/list_server_port")
async def create_server(ins_id: str):
    try:
        server = ops._list_server_port(ins_id)
        return server
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v3/attach_port")
async def create_server(ins_id: str, network_id: str):
    try:
        server = ops._create_port_for_server(ins_id, network_id)
        return server
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/api/v3/detach_port")
async def create_server(ins_id: str, network_id: str):
    try:
        server = ops._detach_port_for_server(ins_id, network_id)
        return server
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v3/console_url")
async def console_url(ins_id: str):
    try:
        console_url = ops._console_url(ins_id)
        return console_url
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/api/v3/start_server/{ins_id}")
async def start_server(ins_id: str):
    try:
        return ops._start_server(ins_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/api/v3/stop_server/{ins_id}")
async def stop_server(ins_id: str):
    try:
        return ops._stop_server(ins_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v3/delete/{ins_id}")
async def stop_server(ins_id: str):
    try:
        return ops._delete_server(ins_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="10.5.11.221", port=12340)