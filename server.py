import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="Sogeti MCP Gateway Pure FastAPI")

SOGETI_EMPLOYEES = {
    "amara": {"poste": "Data Architect", "competences": ["GCP", "Python", "IA Architecture"], "dispo": "Immédiate"},
    "jean": {"poste": "Cloud Engineer", "competences": ["AWS", "Terraform", "Docker"], "dispo": "En mission"}
}

@app.get("/")
async def health():
    return {"status": "healthy"}

@app.post("/mcp")
async def handle_mcp(request: Request):
    body = await request.json()
    method = body.get("method")
    request_id = body.get("id", 1)

    # 1. Gestion de la liste des outils demandée par l'ADK
    if method in ["tools/list", "list_tools"]:
        return JSONResponse(content={
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "get_collaborator_profile",
                        "description": "Récupère le profil technique d'un collaborateur Sogeti.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string", "description": "Le prénom du collaborateur (ex: amara)"}
                            },
                            "required": ["name"]
                        }
                    }
                ]
            }
        })

    # 2. Gestion de l'exécution de l'outil demandée par l'ADK
    elif method in ["tools/call", "call_tool"]:
        params = body.get("params", {})
        arguments = params.get("arguments", body.get("arguments", {}))
            
        employee_name = arguments.get("name", "").lower()
        profile = SOGETI_EMPLOYEES.get(employee_name, {"erreur": "Collaborateur introuvable."})
        
        return JSONResponse(content={
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": f"Poste: {profile.get('poste')}, Competences: {profile.get('competences')}, Dispo: {profile.get('dispo')}"
                    }
                ]
            }
        })

    # Réponse par défaut pour l'initialisation de session de l'ADK
    return JSONResponse(content={
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {}
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
