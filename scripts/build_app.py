#!/usr/bin/env python3
import os
from pathlib import Path


def get_input(prompt: str) -> str:
    """
    Get input from user with validation
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def create_directory_structure(app_name: str, route_slug: str):
    """
    Create a new app directory structure with controllers and routes
    """
    # Base directory for the new app at root level
    app_dir = Path(app_name)

    # Create main app directory
    app_dir.mkdir(parents=True, exist_ok=True)

    # Create __init__.py
    (app_dir / "__init__.py").touch()

    # Create controllers directory
    controllers_dir = app_dir / "controllers"
    controllers_dir.mkdir(exist_ok=True)
    (controllers_dir / "__init__.py").touch()

    # Create utils directory
    utils_dir = app_dir / "utils"
    utils_dir.mkdir(exist_ok=True)
    (utils_dir / "__init__.py").touch()

    # Create base controller file
    controller_file = controllers_dir / f"{route_slug}_controller.py"
    with open(controller_file, "w") as f:
        f.write(
            f'''from fastapi import APIRouter, Depends, HTTPException
from typing import List

router = APIRouter()

@router.get("/")
async def get_items():
    """
    Get all items
    """
    return {{"message": "Get all items"}}

'''
        )

    # Create routes file directly in app directory
    routes_file = app_dir / "routes.py"
    with open(routes_file, "w") as f:
        f.write(
            f'''from fastapi import APIRouter
from .controllers.{route_slug}_controller import router as controller_router

router = APIRouter()
router.include_router(controller_router, prefix="/{route_slug}", tags=["{route_slug}"])
'''
        )

    print(f"\nCreated new app structure for '{app_name}' with route '{route_slug}'")
    print(f"Directory structure:")
    print(f"{app_name}/")
    print(f"├── controllers/")
    print(f"│   └── {route_slug}_controller.py")
    print(f"├── utils/")
    print(f"└── routes.py")


def main():
    print("\nFastAPI App Structure Generator")
    print("==============================\n")

    app_name = get_input("Enter app name (e.g., users, products): ")
    route_slug = get_input("Enter route slug (e.g., user, product): ")

    create_directory_structure(app_name, route_slug)


if __name__ == "__main__":
    main()
