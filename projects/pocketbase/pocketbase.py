import requests
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any, Optional, Union
import urllib.parse


class PocketBaseClient:
    """Python client for PocketBase API"""

    def __init__(self, base_url: str):
        """
        Initialize PocketBase client

        Args:
            base_url: PocketBase server URL (e.g., 'http://localhost:8090')
        """
        self.base_url = base_url.rstrip("/")
        self.token = None
        self.token_expiry = None
        self._session = requests.Session()

    def _handle_response(self, response: requests.Response) -> dict:
        """Handle API response and errors"""
        try:
            data = response.json()
            if response.ok:
                return data
            else:
                error_msg = data.get("message", "Unknown error")
                raise Exception(f"PocketBase API error: {error_msg}")
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON response: {response.text}")

    def _get_headers(self) -> dict:
        """Get request headers with authentication if available"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def auth_with_password(
        self, email: str, password: str, collection: str = "admins"
    ) -> dict:
        """
        Authenticate using email and password

        Args:
            email: User email
            password: User password
            collection: Collection name (default: 'admins')

        Returns:
            dict: Authentication response data
        """
        if collection == "admins":
            endpoint = f"{self.base_url}/api/admins/auth-with-password"
        else:
            endpoint = (
                f"{self.base_url}/api/collections/{collection}/auth-with-password"
            )

        data = {"identity": email, "password": password}

        response = self._session.post(endpoint, json=data)
        result = self._handle_response(response)

        if "token" in result:
            self.token = result["token"]
            # Set token expiry to 14 days from now (PocketBase default)
            self.token_expiry = datetime.now() + timedelta(days=14)

        return result

    def logout(self):
        """Clear authentication token"""
        self.token = None
        self.token_expiry = None
        self._session.cookies.clear()

    def create_record(self, collection: str, data: dict) -> dict:
        """
        Create a new record

        Args:
            collection: Collection name
            data: Record data

        Returns:
            dict: Created record data
        """
        endpoint = f"{self.base_url}/api/collections/{collection}/records"
        response = self._session.post(endpoint, headers=self._get_headers(), json=data)
        return self._handle_response(response)

    def get_record(self, collection: str, record_id: str) -> dict:
        """
        Retrieve a single record

        Args:
            collection: Collection name
            record_id: Record ID

        Returns:
            dict: Record data
        """
        endpoint = f"{self.base_url}/api/collections/{collection}/records/{record_id}"
        response = self._session.get(endpoint, headers=self._get_headers())
        return self._handle_response(response)

    def update_record(self, collection: str, record_id: str, data: dict) -> dict:
        """
        Update an existing record

        Args:
            collection: Collection name
            record_id: Record ID
            data: Updated record data

        Returns:
            dict: Updated record data
        """
        endpoint = f"{self.base_url}/api/collections/{collection}/records/{record_id}"
        response = self._session.patch(endpoint, headers=self._get_headers(), json=data)
        return self._handle_response(response)

    def delete_record(self, collection: str, record_id: str) -> dict:
        """
        Delete a record

        Args:
            collection: Collection name
            record_id: Record ID

        Returns:
            dict: Deletion response data
        """
        endpoint = f"{self.base_url}/api/collections/{collection}/records/{record_id}"
        response = self._session.delete(endpoint, headers=self._get_headers())
        return self._handle_response(response)

    def delete_records(
        self, collection: str, filter_str: Optional[str] = None, batch_size: int = 100
    ) -> dict:
        """
        Delete multiple records from a collection with optional filtering

        Args:
            collection: Collection name
            filter_str: Filter query string to select specific records
            batch_size: Number of records to delete in each batch

        Returns:
            dict: Summary of deletion operation
        """
        deleted_count = 0
        while True:
            # Get a batch of records
            records = self.list_records(
                collection=collection,
                filter_str=filter_str,
                per_page=batch_size,
                page=1,  # Always get first page since we're deleting
            )
            if not records["items"]:
                break

            # Delete each record in the batch
            for record in records["items"]:
                self.delete_record(collection, record["id"])
                deleted_count += 1
        return {"deleted_count": deleted_count}

    def list_records(
        self,
        collection: str,
        page: int = 1,
        per_page: int = 30,
        filter_str: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> dict:
        """
        List records with pagination and filtering

        Args:
            collection: Collection name
            page: Page number
            per_page: Records per page
            filter_str: Filter query string
            sort: Sort query string

        Returns:
            dict: List of records with pagination info
        """
        endpoint = f"{self.base_url}/api/collections/{collection}/records"
        params = {"page": page, "perPage": per_page}

        if filter_str:
            params["filter"] = filter_str
        if sort:
            params["sort"] = sort

        response = self._session.get(
            endpoint, headers=self._get_headers(), params=params
        )
        return self._handle_response(response)

    def upload_file(
        self, collection: str, record_id: str, field: str, file_path: str
    ) -> dict:
        """
        Upload a file to a record

        Args:
            collection: Collection name
            record_id: Record ID
            field: Field name for the file
            file_path: Path to the file to upload

        Returns:
            dict: Updated record data
        """
        endpoint = f"{self.base_url}/api/collections/{collection}/records/{record_id}"

        with open(file_path, "rb") as f:
            files = {field: f}
            response = self._session.patch(
                endpoint, headers={"Authorization": f"Bearer {self.token}"}, files=files
            )

        return self._handle_response(response)


def to_dataframe(
    self,
    collection: str,
    filter_str: Optional[str] = None,
    sort: Optional[str] = None,
    flatten: bool = True,
    exclude_fields: Optional[List[str]] = None,
):
    """
    Convert collection records to a pandas DataFrame

    Args:
        collection: Collection name
        filter_str: Optional filter query string
        sort: Optional sort query string
        flatten: Whether to flatten nested JSON structures into columns
        exclude_fields: List of fields to exclude from the DataFrame

    Returns:
        pd.DataFrame: DataFrame containing the records

    Raises:
        ImportError: If pandas is not installed
        Exception: If there's an error fetching or processing the records
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError(
            "pandas is required for this function. "
            "Install it with: pip install pandas"
        )

    # Initialize list to store all records
    all_records = []
    page = 1

    # Fetch all records with pagination
    while True:
        records = self.list_records(
            collection=collection,
            page=page,
            per_page=100,
            filter_str=filter_str,
            sort=sort,
        )

        if not records["items"]:
            break

        all_records.extend(records["items"])
        page += 1

    if not all_records:
        # Return empty DataFrame with appropriate columns
        return pd.DataFrame()

    # Convert records to DataFrame
    df = pd.DataFrame(all_records)

    # Handle exclude_fields
    if exclude_fields:
        df = df.drop(columns=exclude_fields, errors="ignore")

    if flatten:
        # Function to flatten nested dictionaries
        def flatten_dict(
            d: Dict[str, Any], parent_key: str = "", sep: str = "_"
        ) -> Dict[str, Any]:
            items: List[Tuple[str, Any]] = []
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten_dict(v, new_key, sep=sep).items())
                elif isinstance(v, list):
                    # Convert lists to string representation
                    items.append((new_key, str(v)))
                else:
                    items.append((new_key, v))
            return dict(items)

        # Flatten nested structures
        flattened_records = []
        for record in all_records:
            flattened_records.append(flatten_dict(record))

        df = pd.DataFrame(flattened_records)

    # Convert PocketBase's ISO timestamps to pandas datetime
    timestamp_columns = ["created", "updated"]
    for col in timestamp_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    # Sort index
    df = df.sort_index(axis=1)

    return df


# Example usage
if __name__ == "__main__":
    # Initialize client
    pb = PocketBaseClient("http://localhost:8090")

    try:
        # Authenticate
        auth_data = pb.auth_with_password(
            email="bcutrell@smartleaf.com", password="spiderman123"
        )
        print("Authenticated:", auth_data)

        # Create a record
        new_record = pb.create_record(
            collection="posts",
            data={"title": "Test Post", "content": "This is a test post"},
        )
        print("Created record:", new_record)

        # List records with filtering
        records = pb.list_records(
            collection="posts", filter_str='title ~ "Test"', sort="-created"
        )
        print("Found records:", records)

        # Update a record
        updated_record = pb.update_record(
            collection="posts",
            record_id=new_record["id"],
            data={"content": "Updated content"},
        )
        print("Updated record:", updated_record)

        # Delete the record
        pb.delete_record(collection="posts", record_id=new_record["id"])
        print("Record deleted")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Logout
        pb.logout()
