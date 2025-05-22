import os
import json
from typing import Dict, List, Optional, Any
import uuid

from core.embeddings import embed_document, get_vectorstore

# Path to JSON file that stores projects
PROJECTS_FILE = os.path.join(os.path.dirname(__file__), "../../data/projects.json")

# Ensure data directory exists
os.makedirs(os.path.dirname(PROJECTS_FILE), exist_ok=True)

def _load_projects() -> List[Dict[str, Any]]:
    """
    Load projects from JSON file.
    """
    if not os.path.exists(PROJECTS_FILE):
        # Create empty projects file
        with open(PROJECTS_FILE, "w") as f:
            json.dump([], f)
        return []
    
    with open(PROJECTS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def _save_projects(projects: List[Dict[str, Any]]) -> None:
    """
    Save projects to JSON file.
    """
    with open(PROJECTS_FILE, "w") as f:
        json.dump(projects, f, indent=2)

def get_all_projects() -> List[Dict[str, Any]]:
    """
    Get all projects.
    """
    return _load_projects()

def get_project(project_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a project by ID.
    """
    projects = _load_projects()
    for project in projects:
        if project.get("id") == project_id:
            return project
    return None

def store_project(project: Dict[str, Any]) -> str:
    """
    Store a project and embed it in the vector store.
    """
    # Load existing projects
    projects = _load_projects()
    
    # Check if project already exists
    for i, p in enumerate(projects):
        if p.get("id") == project["id"]:
            # Update existing project
            projects[i] = project
            _save_projects(projects)
            
            # Embed in vector store
            _embed_project(project)
            
            return project["id"]
    
    # Add new project
    projects.append(project)
    _save_projects(projects)
    
    # Embed in vector store
    _embed_project(project)
    
    return project["id"]

def update_project(project: Dict[str, Any]) -> None:
    """
    Update a project.
    """
    store_project(project)

def delete_project(project_id: str) -> None:
    """
    Delete a project.
    """
    # Load existing projects
    projects = _load_projects()
    
    # Filter out project to delete
    projects = [p for p in projects if p.get("id") != project_id]
    
    # Save projects
    _save_projects(projects)
    
    # TODO: Remove from vector store (not directly supported by Chroma)
    # For now, we'll leave it in the vector store, as deleting is complex

def _embed_project(project: Dict[str, Any]) -> None:
    """
    Embed a project in the vector store.
    """
    # Convert project to text
    project_text = f"""
    Project: {project['name']}
    ID: {project['id']}
    Description: {project['description']}
    Status: {project['status']}
    Technologies: {', '.join(project['technologies'])}
    Start Date: {project['start_date']}
    End Date: {project.get('end_date', 'Ongoing')}
    Repository URL: {project.get('repo_url', 'N/A')}
    Notes: {project.get('notes', 'N/A')}
    """
    
    # Create metadata
    metadata = {
        "source": "project",
        "project_id": project["id"],
        "project_name": project["name"],
        "project_status": project["status"],
    }
    
    # Embed document
    embed_document(text=project_text, metadata=metadata)

def search_projects(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search projects by query.
    """
    # Get vector store
    vectorstore = get_vectorstore()
    
    # Search for documents
    results = vectorstore.similarity_search(
        query=query,
        k=top_k,
        filter={"source": "project"}
    )
    
    # Extract project IDs from results
    project_ids = [doc.metadata.get("project_id") for doc in results if doc.metadata.get("project_id")]
    
    # Get projects by IDs
    projects = []
    for project_id in project_ids:
        project = get_project(project_id)
        if project and project not in projects:
            projects.append(project)
    
    return projects 