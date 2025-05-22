from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

from core.projects import store_project, get_project, get_all_projects, update_project, delete_project

router = APIRouter()

class ProjectBase(BaseModel):
    name: str
    description: str
    status: str
    technologies: List[str]
    start_date: str
    end_date: Optional[str] = None
    repo_url: Optional[str] = None
    notes: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class Project(ProjectBase):
    id: str
    created_at: str
    updated_at: str

@router.post("/projects", response_model=Project)
async def create_project(project: ProjectCreate):
    """
    Create a new project for Arun Jayesh.
    """
    try:
        project_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        project_data = project.model_dump()
        project_data.update({
            "id": project_id,
            "created_at": timestamp,
            "updated_at": timestamp
        })
        
        # Store project in database and vector store
        store_project(project_data)
        
        return project_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projects", response_model=List[Project])
async def list_projects(
    status: Optional[str] = Query(None, description="Filter by project status")
):
    """
    List all projects or filter by status.
    """
    try:
        projects = get_all_projects()
        
        # Filter by status if provided
        if status:
            projects = [p for p in projects if p.get("status") == status]
        
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projects/{project_id}", response_model=Project)
async def get_project_by_id(project_id: str):
    """
    Get a project by ID.
    """
    try:
        project = get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")
        return project
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/projects/{project_id}", response_model=Project)
async def update_project_by_id(project_id: str, project_update: ProjectUpdate):
    """
    Update an existing project.
    """
    try:
        # Check if project exists
        existing = get_project(project_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")
        
        # Update project
        update_data = project_update.model_dump()
        update_data["id"] = project_id
        update_data["created_at"] = existing["created_at"]
        update_data["updated_at"] = datetime.now().isoformat()
        
        # Store updated project
        update_project(update_data)
        
        return update_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/projects/{project_id}")
async def delete_project_by_id(project_id: str):
    """
    Delete a project by ID.
    """
    try:
        # Check if project exists
        existing = get_project(project_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")
        
        # Delete project
        delete_project(project_id)
        
        return {"message": f"Project with ID {project_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 