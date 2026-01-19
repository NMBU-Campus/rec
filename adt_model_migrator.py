#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Azure Digital Twins Model Migration Tool

Provides functionality to migrate DTDL models from a folder to Azure Digital Twins.
Similar to ADT Explorer's bulk upload functionality, but as a Python module.

Usage in notebook:
    import adt_model_migrator
    
    result = adt_model_migrator.migrate_models(
        folder_path="./Source/DTDLv2",
        adt_url="https://your-instance.api.region.digitaltwins.azure.net"
    )
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from azure.core.exceptions import AzureError, HttpResponseError
from azure.digitaltwins.core import DigitalTwinsClient
from azure.identity import DefaultAzureCredential

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def _is_interface(model: Dict[str, Any]) -> bool:
    """Check if a model is an Interface type."""
    model_type = model.get("@type") or model.get("type")
    if isinstance(model_type, list):
        return "Interface" in model_type
    return model_type == "Interface"


def load_dtdl_models(folder_path: Path) -> List[Dict[str, Any]]:
    """
    Recursively load all DTDL Interface models from a folder.
    
    Args:
        folder_path: Path to folder containing DTDL JSON files
        
    Returns:
        List of Interface model dictionaries
    """
    models: List[Dict[str, Any]] = []
    
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    
    if not folder_path.is_dir():
        raise ValueError(f"Path is not a directory: {folder_path}")
    
    # Recursively find all JSON files
    json_files = list(folder_path.rglob("*.json"))
    logger.info(f"Found {len(json_files)} JSON files in {folder_path}")
    
    for json_file in json_files:
        try:
            content = json_file.read_text(encoding="utf-8")
            data = json.loads(content)
            
            # Handle arrays of models
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and _is_interface(item):
                        models.append(item)
            # Handle single model
            elif isinstance(data, dict) and _is_interface(data):
                models.append(data)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON file {json_file}: {e}")
        except Exception as e:
            logger.warning(f"Error reading file {json_file}: {e}")
    
    logger.info(f"Loaded {len(models)} Interface models")
    return models


def _extract_extends(model: Dict[str, Any]) -> List[str]:
    """
    Extract all extends relationships from a model.
    
    Args:
        model: DTDL model dictionary
        
    Returns:
        List of DTMI strings that this model extends
    """
    extends = model.get("extends", [])
    if isinstance(extends, str):
        return [extends]
    elif isinstance(extends, list):
        return [e for e in extends if isinstance(e, str)]
    return []


def _extract_dependencies(model: Dict[str, Any]) -> Set[str]:
    """
    Extract all dependencies from a model (extends, components, etc.).
    
    Args:
        model: DTDL model dictionary
        
    Returns:
        Set of DTMI strings that this model depends on
    """
    dependencies: Set[str] = set()
    
    # Add extends dependencies
    dependencies.update(_extract_extends(model))
    
    # Add component dependencies
    contents = model.get("contents", [])
    for content in contents:
        if isinstance(content, dict):
            # Check for Component type
            content_type = content.get("@type")
            if isinstance(content_type, list):
                content_type = content_type[0] if content_type else None
            
            if content_type == "Component":
                schema = content.get("schema")
                if isinstance(schema, str) and schema.startswith("dtmi:"):
                    dependencies.add(schema)
    
    return dependencies


def resolve_dependencies(models: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Resolve model dependencies and return models in topological order.
    
    Args:
        models: List of DTDL model dictionaries
        
    Returns:
        Tuple of (ordered models, list of warnings/errors)
    """
    warnings: List[str] = []
    
    # Build index by @id
    model_index: Dict[str, Dict[str, Any]] = {}
    for model in models:
        model_id = model.get("@id")
        if not model_id:
            warnings.append("Model missing @id field, skipping")
            continue
        if model_id in model_index:
            warnings.append(f"Duplicate model ID: {model_id}")
        model_index[model_id] = model
    
    # Build dependency graph
    dependencies: Dict[str, Set[str]] = {}
    for model_id, model in model_index.items():
        deps = _extract_dependencies(model)
        # Filter to only dependencies that exist in our model set
        existing_deps = {d for d in deps if d in model_index}
        dependencies[model_id] = existing_deps
        
        # Warn about missing dependencies
        missing_deps = deps - existing_deps
        if missing_deps:
            warnings.append(
                f"Model {model_id} has dependencies not in model set: {missing_deps}"
            )
    
    # Topological sort using DFS
    visited: Set[str] = set()
    temp_visited: Set[str] = set()
    ordered_ids: List[str] = []
    
    def visit(model_id: str):
        if model_id in visited:
            return
        if model_id in temp_visited:
            warnings.append(f"Circular dependency detected involving {model_id}")
            return
        
        temp_visited.add(model_id)
        
        # Visit all dependencies first
        for dep_id in dependencies.get(model_id, set()):
            if dep_id in model_index:
                visit(dep_id)
        
        temp_visited.remove(model_id)
        visited.add(model_id)
        ordered_ids.append(model_id)
    
    # Visit all models
    for model_id in model_index.keys():
        visit(model_id)
    
    # Return models in order
    ordered_models = [model_index[mid] for mid in ordered_ids if mid in model_index]
    
    return ordered_models, warnings


def validate_dtmi(dtmi: str) -> bool:
    """
    Validate DTMI format.
    
    Args:
        dtmi: DTMI string to validate
        
    Returns:
        True if valid DTMI format
    """
    if not dtmi.startswith("dtmi:"):
        return False
    parts = dtmi.split(":")
    if len(parts) < 3:
        return False
    # Check for version number at the end (e.g., ;1)
    if ";" not in dtmi:
        return False
    return True


def validate_models(models: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """
    Validate DTDL models before upload.
    
    Args:
        models: List of DTDL model dictionaries
        
    Returns:
        Tuple of (is_valid, list of errors)
    """
    errors: List[str] = []
    
    for model in models:
        model_id = model.get("@id")
        if not model_id:
            errors.append("Model missing @id field")
            continue
        
        if not validate_dtmi(model_id):
            errors.append(f"Invalid DTMI format: {model_id}")
        
        if not _is_interface(model):
            errors.append(f"Model {model_id} is not an Interface type")
    
    return len(errors) == 0, errors


def _delete_twins_using_model(client: DigitalTwinsClient, model_id: str) -> int:
    """
    Delete all digital twins that are using a specific model.
    
    Args:
        client: DigitalTwinsClient instance
        model_id: DTMI of the model
        
    Returns:
        Number of twins deleted
    """
    deleted_count = 0
    try:
        twin_list = client.list_digital_twins()
        for twin in twin_list:
            twin_id = twin.get('$dtId') or twin.get('$metadata', {}).get('$dtId')
            twin_model = twin.get('$metadata', {}).get('$model')
            
            if twin_model == model_id and twin_id:
                try:
                    client.delete_digital_twin(twin_id)
                    deleted_count += 1
                    logger.debug(f"Deleted twin {twin_id} using model {model_id}")
                except Exception as e:
                    logger.warning(f"Failed to delete twin {twin_id}: {e}")
    except Exception as e:
        logger.warning(f"Error finding twins using model {model_id}: {e}")
    
    return deleted_count


def delete_all_twins(client: DigitalTwinsClient) -> Dict[str, Any]:
    """
    Delete all digital twins from Azure Digital Twins instance.
    This must be done before deleting models that are in use.
    
    Args:
        client: DigitalTwinsClient instance
        
    Returns:
        Dictionary with deletion results
    """
    logger.info("Fetching existing digital twins...")
    twins = []
    
    try:
        twin_list = client.list_digital_twins()
        for twin in twin_list:
            twins.append(twin)
    except AzureError as e:
        logger.error(f"Failed to list digital twins: {e}")
        raise
    
    logger.info(f"Found {len(twins)} digital twins")
    
    if not twins:
        return {
            "deleted": 0,
            "failed": 0,
            "errors": []
        }
    
    deleted_count = 0
    failed_count = 0
    errors: List[str] = []
    
    for twin in twins:
        twin_id = twin.get('$dtId') or twin.get('$metadata', {}).get('$dtId', 'unknown')
        try:
            client.delete_digital_twin(twin_id)
            deleted_count += 1
            logger.debug(f"Deleted twin: {twin_id}")
        except HttpResponseError as e:
            error_msg = f"Failed to delete twin {twin_id}: {e.message}"
            logger.warning(error_msg)
            errors.append(error_msg)
            failed_count += 1
        except Exception as e:
            error_msg = f"Unexpected error deleting twin {twin_id}: {e}"
            logger.error(error_msg)
            errors.append(error_msg)
            failed_count += 1
    
    logger.info(f"Deleted {deleted_count} digital twins, {failed_count} failed")
    
    return {
        "deleted": deleted_count,
        "failed": failed_count,
        "errors": errors
    }


def delete_all_relationships(client: DigitalTwinsClient) -> Dict[str, Any]:
    """
    Delete all relationships from Azure Digital Twins instance.
    This should be done after deleting twins but before deleting models.
    
    Args:
        client: DigitalTwinsClient instance
        
    Returns:
        Dictionary with deletion results
    """
    logger.info("Fetching existing relationships...")
    
    try:
        # Get all twins first to delete their relationships
        twin_list = client.list_digital_twins()
        twin_ids = []
        for twin in twin_list:
            twin_id = twin.get('$dtId') or twin.get('$metadata', {}).get('$dtId')
            if twin_id:
                twin_ids.append(twin_id)
        
        # Delete relationships for each twin
        deleted_count = 0
        failed_count = 0
        errors: List[str] = []
        
        for twin_id in twin_ids:
            try:
                rel_list = client.list_relationships(twin_id)
                for rel in rel_list:
                    rel_id = rel.get('$relationshipId', 'unknown')
                    try:
                        client.delete_relationship(twin_id, rel_id)
                        deleted_count += 1
                        logger.debug(f"Deleted relationship {rel_id} from twin {twin_id}")
                    except Exception as e:
                        error_msg = f"Failed to delete relationship {rel_id} from {twin_id}: {e}"
                        logger.warning(error_msg)
                        errors.append(error_msg)
                        failed_count += 1
            except Exception as e:
                error_msg = f"Failed to list relationships for twin {twin_id}: {e}"
                logger.warning(error_msg)
                errors.append(error_msg)
        
        logger.info(f"Deleted {deleted_count} relationships, {failed_count} failed")
        
        return {
            "deleted": deleted_count,
            "failed": failed_count,
            "errors": errors
        }
    except AzureError as e:
        logger.error(f"Failed to list digital twins for relationship deletion: {e}")
        return {
            "deleted": 0,
            "failed": 0,
            "errors": [f"Failed to list twins: {e}"]
        }


def delete_all_models(
    client: DigitalTwinsClient,
    max_attempts: int = 5
) -> Dict[str, Any]:
    """
    Delete all models from Azure Digital Twins instance.
    
    Models that are in use by digital twins cannot be deleted and will be skipped.
    This function attempts deletion multiple times to handle dependency chains.
    
    Args:
        client: DigitalTwinsClient instance
        max_attempts: Maximum number of deletion attempts (to handle dependencies)
        
    Returns:
        Dictionary with deletion results
    """
    logger.info("Fetching existing models...")
    existing_models = []
    
    try:
        model_list = client.list_models()
        for model in model_list:
            existing_models.append(model)
    except AzureError as e:
        logger.error(f"Failed to list models: {e}")
        raise
    
    logger.info(f"Found {len(existing_models)} existing models")
    
    if not existing_models:
        return {
            "deleted": 0,
            "failed": 0,
            "errors": [],
            "remaining": []
        }
    
    # Track which models we've successfully deleted
    deleted_model_ids: Set[str] = set()
    all_model_ids = {m.id for m in existing_models}
    errors: List[str] = []
    
    # Build dependency graph to determine deletion order
    # Models that extend others should be deleted first (derived before base)
    # Models that are components should be deleted after models that use them
    model_dependencies: Dict[str, Set[str]] = {}
    for model in existing_models:
        deps = set()
        # Check extends - model object from SDK may have different structure
        # Try accessing model definition directly
        try:
            # The model object might have a 'model' attribute with the DTDL definition
            model_def = getattr(model, 'model', None)
            if model_def:
                if isinstance(model_def, dict):
                    extends = model_def.get('extends', [])
                    if isinstance(extends, str):
                        deps.add(extends)
                    elif isinstance(extends, list):
                        deps.update([e for e in extends if isinstance(e, str)])
                elif isinstance(model_def, str):
                    # Might be JSON string
                    try:
                        import json
                        model_dict = json.loads(model_def)
                        extends = model_dict.get('extends', [])
                        if isinstance(extends, str):
                            deps.add(extends)
                        elif isinstance(extends, list):
                            deps.update([e for e in extends if isinstance(e, str)])
                    except Exception:
                        pass
        except Exception:
            pass
        model_dependencies[model.id] = deps
    
    # Try multiple passes to handle dependencies
    for attempt in range(max_attempts):
        logger.info(f"Deletion attempt {attempt + 1}/{max_attempts}")
        deleted_this_round = 0
        
        # Sort models: those with no dependencies or only deleted dependencies first
        # Then reverse to delete derived models before base models
        def deletion_priority(model_id: str) -> int:
            deps = model_dependencies.get(model_id, set())
            # Count how many dependencies are still not deleted
            remaining_deps = len([d for d in deps if d not in deleted_model_ids])
            return remaining_deps
        
        sorted_models = sorted(
            existing_models,
            key=lambda m: (deletion_priority(m.id), m.id),
            reverse=True  # Derived models (with dependencies) first
        )
        
        for model in sorted_models:
            if model.id in deleted_model_ids:
                continue  # Already deleted
            
            # Check if all dependencies are deleted
            deps = model_dependencies.get(model.id, set())
            remaining_deps = [d for d in deps if d not in deleted_model_ids and d in all_model_ids]
            if remaining_deps:
                logger.debug(f"Model {model.id} has undeleted dependencies: {remaining_deps}, skipping for now")
                continue
            
            try:
                client.delete_model(model.id)
                deleted_model_ids.add(model.id)
                deleted_this_round += 1
                logger.info(f"Deleted model: {model.id}")
            except HttpResponseError as e:
                status_code = getattr(e, 'status_code', None)
                error_message = getattr(e, 'message', str(e))
                
                # Extract detailed error
                try:
                    if hasattr(e, 'response') and hasattr(e.response, 'json'):
                        error_json = e.response.json()
                        if isinstance(error_json, dict) and 'error' in error_json:
                            error_info = error_json['error']
                            if isinstance(error_info, dict) and 'message' in error_info:
                                error_message = error_info['message']
                except Exception:
                    pass
                
                # Check if model is in use (409 Conflict or specific error messages)
                if status_code == 409 or 'in use' in error_message.lower() or 'referenced' in error_message.lower():
                    # Model is in use by digital twins - cannot delete, skip it
                    logger.warning(f"Model {model.id} is in use by digital twins and cannot be deleted. It will be skipped.")
                    # Mark as "remaining" so we know it couldn't be deleted
                    # Don't add to errors since this is expected behavior
                    # Will try again in next attempt in case dependencies change
                    logger.debug(f"Model {model.id} is in use, will retry: {error_message}")
                else:
                    # Other error - log it
                    error_msg = f"Failed to delete {model.id}: {error_message}"
                    if error_msg not in errors:
                        errors.append(error_msg)
                    logger.warning(error_msg)
            except Exception as e:
                error_msg = f"Unexpected error deleting {model.id}: {e}"
                if error_msg not in errors:
                    errors.append(error_msg)
                logger.error(error_msg)
        
        logger.info(f"Deleted {deleted_this_round} models in this attempt")
        
        # If we didn't delete any this round, stop trying
        if deleted_this_round == 0:
            break
    
    failed_count = len(all_model_ids) - len(deleted_model_ids)
    remaining_models = list(all_model_ids - deleted_model_ids)
    
    logger.info(f"Deletion complete: {len(deleted_model_ids)} deleted, {failed_count} failed/remaining")
    
    if remaining_models:
        logger.warning(f"Could not delete {len(remaining_models)} models (likely in use by digital twins)")
        logger.warning(f"Remaining models: {remaining_models[:10]}")  # Show first 10
        if len(remaining_models) > 10:
            logger.warning(f"... and {len(remaining_models) - 10} more")
    
    return {
        "deleted": len(deleted_model_ids),
        "failed": failed_count,
        "errors": errors,
        "remaining": remaining_models
    }


def upload_model_single(
    client: DigitalTwinsClient,
    model: Dict[str, Any],
    max_retries: int = 1,
    retry_delay: float = 0.5
) -> Tuple[bool, Optional[str]]:
    """
    Upload a single model to Azure Digital Twins with retry logic.
    Used as fallback when batch upload fails.
    
    Args:
        client: DigitalTwinsClient instance
        model: Single DTDL model dictionary
        max_retries: Maximum number of retry attempts
        retry_delay: Initial delay in seconds between retries
        
    Returns:
        Tuple of (success, error_message)
    """
    model_id = model.get("@id", "unknown")
    
    for attempt in range(max_retries + 1):
        try:
            client.create_models([model])
            return True, None
        except HttpResponseError as e:
            status_code = getattr(e, 'status_code', None)
            error_message = getattr(e, 'message', str(e))
            
            # Extract detailed error
            try:
                if hasattr(e, 'response') and hasattr(e.response, 'json'):
                    error_json = e.response.json()
                    if isinstance(error_json, dict) and 'error' in error_json:
                        error_info = error_json['error']
                        if isinstance(error_info, dict) and 'message' in error_info:
                            error_message = error_info['message']
            except Exception:
                pass
            
            # Don't retry on client errors (4xx) except for rate limiting
            if status_code and 400 <= status_code < 500 and status_code != 429:
                return False, f"{model_id}: {error_message}"
            
            # Retry on server errors (5xx) or rate limiting (429)
            if attempt < max_retries:
                delay = retry_delay * (2 ** attempt)
                logger.debug(f"Model {model_id} failed (attempt {attempt + 1}/{max_retries + 1}), retrying in {delay:.1f}s")
                time.sleep(delay)
            else:
                return False, f"{model_id}: {error_message} after {max_retries + 1} attempts"
        except Exception as e:
            if attempt < max_retries:
                delay = retry_delay * (2 ** attempt)
                logger.debug(f"Model {model_id} failed (attempt {attempt + 1}/{max_retries + 1}), retrying in {delay:.1f}s: {e}")
                time.sleep(delay)
            else:
                return False, f"{model_id}: {str(e)}"
    
    return False, f"{model_id}: Unknown error"


def upload_models(
    client: DigitalTwinsClient,
    models: List[Dict[str, Any]],
    batch_size: int = 100,
    max_retries: int = 3,
    retry_delay: float = 1.0,
    fallback_to_single: bool = True
) -> Dict[str, Any]:
    """
    Upload models to Azure Digital Twins in batches with retry logic.
    
    Args:
        client: DigitalTwinsClient instance
        models: List of DTDL model dictionaries (should be in dependency order)
        batch_size: Number of models to upload per batch (max 100)
        max_retries: Maximum number of retry attempts for failed batches
        retry_delay: Initial delay in seconds between retries (exponential backoff)
        fallback_to_single: If True, attempt individual uploads when batch fails
        
    Returns:
        Dictionary with upload results
    """
    if not models:
        logger.warning("No models to upload")
        return {
            "uploaded": 0,
            "failed": 0,
            "errors": []
        }
    
    batch_size = min(batch_size, 100)  # Azure limit
    uploaded_count = 0
    failed_count = 0
    errors: List[str] = []
    
    # Upload in batches
    total_batches = (len(models) + batch_size - 1) // batch_size
    
    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, len(models))
        batch = models[start_idx:end_idx]
        
        logger.info(f"Uploading batch {batch_num + 1}/{total_batches} ({len(batch)} models)...")
        
        # Retry logic with exponential backoff
        success = False
        last_error = None
        
        for attempt in range(max_retries + 1):
            try:
                created_models = client.create_models(batch)
                uploaded_count += len(created_models)
                logger.info(f"Successfully uploaded {len(created_models)} models in batch {batch_num + 1}")
                success = True
                break
            except HttpResponseError as e:
                last_error = e
                status_code = getattr(e, 'status_code', None)
                
                # Extract detailed error information
                error_details = []
                error_message = getattr(e, 'message', str(e))
                
                # Try to get more detailed error from response
                try:
                    if hasattr(e, 'response'):
                        response = e.response
                        if hasattr(response, 'text'):
                            error_details.append(f"Response: {response.text}")
                        if hasattr(response, 'json'):
                            try:
                                error_json = response.json()
                                if isinstance(error_json, dict):
                                    if 'error' in error_json:
                                        error_info = error_json['error']
                                        if isinstance(error_info, dict):
                                            if 'message' in error_info:
                                                error_message = error_info['message']
                                            if 'details' in error_info:
                                                error_details.append(f"Details: {error_info['details']}")
                                    # Azure sometimes puts errors directly in the response
                                    if 'message' in error_json:
                                        error_message = error_json['message']
                            except Exception:
                                pass
                except Exception:
                    pass
                
                # Log detailed error information
                full_error_msg = f"Batch {batch_num + 1} failed: {error_message}"
                if error_details:
                    full_error_msg += f" ({'; '.join(error_details)})"
                
                # Don't retry on client errors (4xx) except for rate limiting
                if status_code and 400 <= status_code < 500 and status_code != 429:
                    logger.error(full_error_msg)
                    errors.append(full_error_msg)
                    
                    # Try to identify which specific models failed
                    model_ids = [m.get("@id", "unknown") for m in batch]
                    logger.error(f"Failed models in batch {batch_num + 1}: {model_ids[:5]}")  # Show first 5
                    if len(model_ids) > 5:
                        logger.error(f"... and {len(model_ids) - 5} more models")
                    
                    failed_count += len(batch)
                    break
                
                # Retry on server errors (5xx) or rate limiting (429)
                if attempt < max_retries:
                    delay = retry_delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(
                        f"Batch {batch_num + 1} failed (attempt {attempt + 1}/{max_retries + 1}), "
                        f"retrying in {delay:.1f}s: {error_message}"
                    )
                    time.sleep(delay)
                else:
                    logger.error(full_error_msg)
                    errors.append(full_error_msg)
                    
                    # Try to identify which models failed
                    model_ids = [m.get("@id", "unknown") for m in batch]
                    logger.error(f"Failed models in batch {batch_num + 1}: {model_ids[:5]}")
                    if len(model_ids) > 5:
                        logger.error(f"... and {len(model_ids) - 5} more models")
                    
                    # If batch failed and fallback is enabled, try uploading individually
                    if fallback_to_single and status_code and 400 <= status_code < 500:
                        logger.info(f"Attempting to upload batch {batch_num + 1} models individually...")
                        for model in batch:
                            success, error_msg = upload_model_single(client, model, max_retries=1, retry_delay=0.5)
                            if success:
                                uploaded_count += 1
                                failed_count -= 1  # Adjust count since we're retrying
                            else:
                                errors.append(error_msg)
                                logger.error(f"Individual upload failed: {error_msg}")
                    else:
                        failed_count += len(batch)
            except Exception as e:
                last_error = e
                if attempt < max_retries:
                    delay = retry_delay * (2 ** attempt)
                    logger.warning(
                        f"Batch {batch_num + 1} failed (attempt {attempt + 1}/{max_retries + 1}), "
                        f"retrying in {delay:.1f}s: {e}"
                    )
                    time.sleep(delay)
                else:
                    error_msg = f"Unexpected error in batch {batch_num + 1} after {max_retries + 1} attempts: {e}"
                    logger.error(error_msg)
                    errors.append(error_msg)
                    failed_count += len(batch)
        
        if not success and last_error:
            logger.error(f"Failed to upload batch {batch_num + 1} after all retries")
    
    logger.info(f"Upload complete: {uploaded_count} uploaded, {failed_count} failed")
    
    return {
        "uploaded": uploaded_count,
        "failed": failed_count,
        "errors": errors
    }


def delete_all(
    client: DigitalTwinsClient,
    delete_twins: bool = True,
    delete_relationships: bool = True,
    delete_models: bool = True
) -> Dict[str, Any]:
    """
    Delete all twins, relationships, and models from Azure Digital Twins instance.
    This mimics the "Delete All" functionality in Azure Digital Twins Explorer.
    
    Deletion order (matching Explorer behavior):
    1. Delete all digital twins
    2. Delete all relationships
    3. Delete all models (in dependency order)
    
    Args:
        client: DigitalTwinsClient instance
        delete_twins: Whether to delete all digital twins
        delete_relationships: Whether to delete all relationships
        delete_models: Whether to delete all models
        
    Returns:
        Dictionary with deletion results
    """
    results = {
        "twins": {"deleted": 0, "failed": 0, "errors": []},
        "relationships": {"deleted": 0, "failed": 0, "errors": []},
        "models": {"deleted": 0, "failed": 0, "errors": [], "remaining": []}
    }
    
    # Step 1: Delete all digital twins (if enabled)
    if delete_twins:
        logger.info("=== Step 1: Deleting all digital twins ===")
        try:
            results["twins"] = delete_all_twins(client)
        except Exception as e:
            logger.error(f"Failed to delete twins: {e}")
            results["twins"]["errors"].append(str(e))
            results["twins"]["failed"] = 1
    
    # Step 2: Delete all relationships (if enabled)
    if delete_relationships:
        logger.info("=== Step 2: Deleting all relationships ===")
        try:
            results["relationships"] = delete_all_relationships(client)
        except Exception as e:
            logger.error(f"Failed to delete relationships: {e}")
            results["relationships"]["errors"].append(str(e))
    
    # Step 3: Delete all models (if enabled)
    if delete_models:
        logger.info("=== Step 3: Deleting all models ===")
        try:
            results["models"] = delete_all_models(client)
        except Exception as e:
            logger.error(f"Failed to delete models: {e}")
            results["models"]["errors"].append(str(e))
    
    total_deleted = (
        results["twins"]["deleted"] +
        results["relationships"]["deleted"] +
        results["models"]["deleted"]
    )
    total_failed = (
        results["twins"]["failed"] +
        results["relationships"]["failed"] +
        results["models"]["failed"]
    )
    
    logger.info("=== Deletion Summary ===")
    logger.info(f"Total deleted: {total_deleted} (twins: {results['twins']['deleted']}, "
                f"relationships: {results['relationships']['deleted']}, "
                f"models: {results['models']['deleted']})")
    logger.info(f"Total failed: {total_failed}")
    
    return results


def migrate_models(
    folder_path: str,
    adt_url: str,
    delete_existing: bool = True,
    credential: Optional[Any] = None,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Main function to migrate DTDL models from a folder to Azure Digital Twins.
    
    This function matches ADT Explorer's bulk upload behavior:
    - Loads all DTDL models from the folder
    - Resolves dependencies and orders models correctly
    - Deletes all existing models (if delete_existing=True)
      * If models are in use by digital twins, those twins will be deleted to allow model deletion
      * After re-uploading models with the same DTMI, twins can be recreated to use the updated models
    - Uploads models in the correct dependency order
    
    Args:
        folder_path: Path to folder containing DTDL JSON files
        adt_url: Azure Digital Twins instance URL
        delete_existing: Whether to delete all existing models before upload
                         (twins using these models will be deleted to allow model deletion)
        credential: Optional Azure credential (defaults to DefaultAzureCredential)
        dry_run: If True, validate and prepare but don't actually upload
        
    Returns:
        Dictionary with migration results
    """
    folder = Path(folder_path)
    
    logger.info(f"Starting model migration from {folder_path}")
    logger.info(f"Azure Digital Twins URL: {adt_url}")
    logger.info(f"Delete existing: {delete_existing}, Dry run: {dry_run}")
    
    # Load models
    try:
        models = load_dtdl_models(folder)
    except Exception as e:
        logger.error(f"Failed to load models: {e}")
        return {
            "success": False,
            "error": f"Failed to load models: {e}",
            "loaded": 0,
            "uploaded": 0,
            "deleted": 0
        }
    
    if not models:
        logger.warning("No models found to migrate")
        return {
            "success": False,
            "error": "No models found",
            "loaded": 0,
            "uploaded": 0,
            "deleted": 0
        }
    
    logger.info(f"Loaded {len(models)} models")
    
    # Validate models
    is_valid, validation_errors = validate_models(models)
    if not is_valid:
        logger.error(f"Model validation failed: {validation_errors}")
        return {
            "success": False,
            "error": "Model validation failed",
            "validation_errors": validation_errors,
            "loaded": len(models),
            "uploaded": 0,
            "deleted": 0
        }
    
    # Resolve dependencies
    ordered_models, warnings = resolve_dependencies(models)
    
    if warnings:
        logger.warning(f"Dependency resolution warnings: {warnings}")
    
    logger.info(f"Resolved dependencies, {len(ordered_models)} models ready for upload")
    
    if dry_run:
        logger.info("DRY RUN: Would upload the following models:")
        for i, model in enumerate(ordered_models, 1):
            model_id = model.get("@id", "unknown")
            logger.info(f"  {i}. {model_id}")
        return {
            "success": True,
            "dry_run": True,
            "loaded": len(models),
            "ordered": len(ordered_models),
            "warnings": warnings
        }
    
    # Initialize Azure client
    if credential is None:
        credential = DefaultAzureCredential()
    
    # Normalize ADT URL (remove trailing slash if present)
    adt_url = adt_url.rstrip('/')
    
    try:
        client = DigitalTwinsClient(adt_url, credential)
    except Exception as e:
        logger.error(f"Failed to initialize Azure Digital Twins client: {e}")
        return {
            "success": False,
            "error": f"Failed to initialize client: {e}",
            "loaded": len(models),
            "uploaded": 0,
            "deleted": 0
        }
    
    # Delete existing models if requested
    # Note: Models in use by digital twins cannot be deleted and will be skipped
    deletion_result = {"deleted": 0, "failed": 0, "errors": [], "remaining": []}
    if delete_existing:
        logger.info("Deleting all existing models (models in use by twins will be skipped)")
        try:
            deletion_result = delete_all_models(client)
        except Exception as e:
            logger.error(f"Failed to delete existing models: {e}")
            return {
                "success": False,
                "error": f"Failed to delete existing models: {e}",
                "loaded": len(models),
                "uploaded": 0,
                "deleted": 0
            }
        try:
            deletion_result = delete_all_models(client)
            
            if deletion_result["failed"] > 0 or deletion_result.get("remaining"):
                remaining = deletion_result.get("remaining", [])
                if remaining:
                    logger.warning(
                        f"Could not delete {len(remaining)} models after multiple attempts: "
                        f"{remaining[:5]}"
                    )
                    
                    # Check if any of the models we're trying to upload are in the remaining list
                    new_model_ids = {m.get("@id") for m in ordered_models if m.get("@id")}
                    conflicting_models = new_model_ids.intersection(set(remaining))
                    
                    if conflicting_models:
                        logger.error(
                            f"Found {len(conflicting_models)} models that couldn't be deleted: "
                            f"{list(conflicting_models)[:5]}"
                        )
                        logger.error(
                            "These models may still be in use or have complex dependencies.\n"
                            "The upload will proceed, but may fail for these specific models."
                        )
                        # Don't block the upload - let it try and report errors
            
            if deletion_result["errors"]:
                logger.warning(f"Some deletion errors occurred: {deletion_result['errors'][:5]}")
        except Exception as e:
            logger.error(f"Failed to delete existing models: {e}")
            return {
                "success": False,
                "error": f"Failed to delete existing models: {e}",
                "loaded": len(models),
                "uploaded": 0,
                "deleted": 0
            }
    
    # Upload models
    try:
        upload_result = upload_models(client, ordered_models)
    except Exception as e:
        logger.error(f"Failed to upload models: {e}")
        return {
            "success": False,
            "error": f"Failed to upload models: {e}",
            "loaded": len(models),
            "uploaded": 0,
            "deleted": deletion_result["deleted"]
        }
    
    # Prepare result
    success = upload_result["failed"] == 0
    
    result = {
        "success": success,
        "loaded": len(models),
        "uploaded": upload_result["uploaded"],
        "failed": upload_result["failed"],
        "deleted": deletion_result["deleted"],
        "deletion_failed": deletion_result["failed"],
        "warnings": warnings
    }
    
    if upload_result["errors"]:
        result["upload_errors"] = upload_result["errors"]
    if deletion_result["errors"]:
        result["deletion_errors"] = deletion_result["errors"]
    
    if success:
        logger.info("Migration completed successfully!")
    else:
        logger.warning("Migration completed with errors")
    
    return result
