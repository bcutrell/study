from __future__ import annotations
import json
import requests
from datetime import datetime
from typing import Optional, Dict, List, Any, Union, Callable, TypedDict
from functools import partial
import pandas as pd
from dataclasses import dataclass, field, asdict


class FileUpload:
    """Base class for file upload fields"""

    def __init__(self, df=None):
        self.file_data = df

    def to_csv(self, *args, **kwargs):
        """Convert file data to CSV if it's a pandas DataFrame"""
        if isinstance(self.file_data, pd.DataFrame):
            return self.file_data.to_csv(*args, **kwargs)
        return self.file_data


@dataclass
class Accounts:
    """Generated from collection: accounts"""

    id: Optional[str] = None
    cash: Optional[float] = None
    firm: Optional[str] = None


@dataclass
class Firms:
    """Generated from collection: firm"""

    id: Optional[str] = None
    name: Optional[str] = None


@dataclass
class FirmMetrics:
    """Generated from collection: firm_metrics"""

    id: Optional[str] = None
    metrics_csv: FileUpload = None
    metrics_json: Optional[Dict] = None
    analysis_date: Optional[datetime] = None


def flatten_dict(d: dict, parent_key: str = "", sep: str = "_") -> dict:
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            items.append((new_key, str(v)))
        else:
            items.append((new_key, v))
    return dict(items)


def records_to_df(
    records: List[dict], flatten: bool = True, exclude_fields: Optional[list] = None
) -> pd.DataFrame:
    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(
        [flatten_dict(record) for record in records] if flatten else records
    )

    if exclude_fields:
        df = df.drop(columns=exclude_fields, errors="ignore")

    for col in ["created", "updated"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    return df.sort_index(axis=1)


class PocketBaseClient:
    def __init__(self, base_url: str):
        """Initialize with base URL and create session"""
        self.base_url = base_url.rstrip("/")
        self.token = None
        self._session = requests.Session()

        # Partially apply common parameters to request functions
        self.get = partial(self._request, "GET")
        self.post = partial(self._request, "POST")
        self.patch = partial(self._request, "PATCH")
        self.delete = partial(self._request, "DELETE")

    def _get_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def _build_url(self, endpoint: str) -> str:
        return f"{self.base_url}/api/{endpoint}"

    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        url = self._build_url(endpoint)
        headers = {**self._get_headers(), **kwargs.pop("headers", {})}

        try:
            response = self._session.request(method, url, headers=headers, **kwargs)
            return self._handle_response(response)
        except requests.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    @staticmethod
    def _handle_response(response: requests.Response) -> dict:
        if response.status_code == 204:  # No Content
            return {}

        try:
            if not response.content:  # Empty response
                return {}

            data = response.json()
            if response.ok:
                return data
            raise Exception(
                f"PocketBase API error: {data.get('message', 'Unknown error')}"
            )
        except ValueError:
            if response.ok:
                return {}
            raise Exception(f"Invalid JSON response: {response.text}")

    def _prepare_payload(self, data: dict) -> tuple[dict, dict]:
        payload = {}
        files = {}

        for key, value in data.items():
            if isinstance(value, FileUpload):
                if value.file_data is not None:
                    content_type = "text/csv"
                    files[key] = (f"{key}.csv", value.to_csv(index=False), content_type)
            else:
                payload[key] = value

        return payload, files

    def auth_with_password(
        self, email: str, password: str, collection: str = "admins"
    ) -> dict:
        endpoint = f"{'admins' if collection == 'admins' else f'collections/{collection}'}/auth-with-password"
        result = self.post(endpoint, json={"identity": email, "password": password})
        if "token" in result:
            self.token = result["token"]
        return result

    def logout(self) -> None:
        self.token = None
        self._session.cookies.clear()

    def create_record(self, collection: str, data: dict) -> dict:
        """Create record with special handling for CSV files"""
        endpoint = f"collections/{collection}/records"

        payload, files = self._prepare_payload(data)
        if files:
            # send as multipart/form-data
            return self.post(endpoint, data=payload, files=files)
        else:
            # send as JSON
            return self.post(endpoint, json=payload)

    def upsert(self, collection: str, data: dict, filter_str: str) -> dict:
        """Updates or creates record based on filter"""
        existing = self.get_first_list_item(collection, filter_str)
        if existing:
            return self.update_one(collection, existing["id"], data)
        return self.create_record(collection, data)

    def get_one(self, collection: str, record_id: str) -> dict:
        """Get single record"""
        return self.get(f"collections/{collection}/records/{record_id}")

    def update_one(self, collection: str, record_id: str, data: dict) -> dict:
        """Update existing record"""
        return self.patch(f"collections/{collection}/records/{record_id}", json=data)

    def get_first_list_item(self, collection: str, filter_str: str) -> dict:
        """Get single record using filter"""
        records = self.get_list(collection, filter_str=filter_str)
        return records["items"][0] if records["items"] else None

    def get_full_list(self, collection: str, filter_str: str) -> List[dict]:
        """Get all records using filter"""
        all_records = []
        page = 1
        while True:
            records = self.get_list(
                collection=collection, page=page, per_page=100, filter_str=filter_str
            )
            if not records["items"]:
                break
            all_records.extend(records["items"])
            page += 1
        return all_records

    def get_list(
        self,
        collection: str,
        page: int = 1,
        per_page: int = 30,
        filter_str: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> dict:
        """List records using query parameters"""
        params = {"page": page, "perPage": per_page}
        if filter_str:
            params["filter"] = filter_str
        if sort:
            params["sort"] = sort

        return self.get(f"collections/{collection}/records", params=params)

    def delete_one(self, collection: str, record_id: str) -> dict:
        """Delete record"""
        return self.delete(f"collections/{collection}/records/{record_id}")

    def delete_full_list(
        self, collection: str, filter_str: Optional[str] = None, batch_size: int = 100
    ) -> dict:
        """Delete multiple records in batches"""
        deleted_count = 0

        while True:
            records = self.get_list(
                collection=collection,
                page=1,
                per_page=batch_size,
                filter_str=filter_str,
            )

            if not records["items"]:
                break

            deletes = [
                self.delete_one(collection, record["id"]) for record in records["items"]
            ]
            deleted_count += len(deletes)

        return {"deleted_count": deleted_count}

    def get_dataframe(
        self,
        collection: str,
        filter_str: Optional[str] = None,
        sort: Optional[str] = None,
        flatten: bool = True,
        exclude_fields: Optional[list] = None,
    ) -> pd.DataFrame:
        """Convert collection to DataFrame using functional operations"""

        def fetch_page(page: int) -> List[dict]:
            """Inner function to fetch a single page"""
            return self.get_list(
                collection=collection,
                page=page,
                per_page=100,
                filter_str=filter_str,
                sort=sort,
            )["items"]

        # Fetch all pages
        all_records = []
        page = 1
        while True:
            items = fetch_page(page)
            if not items:
                break
            all_records.extend(items)
            page += 1

        return records_to_df(
            all_records, flatten=flatten, exclude_fields=exclude_fields
        )

    def get_file(self, collection: str, record, filename: str) -> bytes:
        """Download a file from a record
        https://pocketbase.io/docs/files-handling/
        """
        url = self._build_url(
            f"files/{record['collectionName']}/{record['id']}/{filename}"
        )
        headers = self._get_headers()
        response = self._session.get(url, headers=headers)
        if not response.ok:
            raise Exception(f"Failed to download file: {response.text}")
        return response.content


if __name__ == "__main__":
    # Initialize client
    pb = PocketBaseClient("http://localhost:8090")

    try:
        # Authenticate
        auth_data = pb.auth_with_password(email="", password="")
        print("Authenticated:", auth_data)

        # Create a new firm using dataclass
        new_firm = Firms(name="Big Firm")
        created_firm = pb.create_record("firms", asdict(new_firm))
        print("Created firm:", created_firm)

        # Create an account linked to the firm
        new_account = Accounts(cash=100, firm=created_firm["id"])
        created_account = pb.create_record("accounts", asdict(new_account))
        print("Created account:", created_account)

        # List accounts with filtering
        accounts = pb.get_list(
            collection="accounts",
            filter_str=f'firm = "{created_firm['id']}"',
            sort="-created",
        )
        print("Found accounts:", accounts)

        # Update firm
        created_firm["name"] = "Updated Big Firm"
        updated_firm = pb.update_one("firms", created_firm["id"], created_firm)
        print("Updated firm:", updated_firm)

        import pandas as pd

        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})

        # Create FirmMetrics record
        firm_metrics = FirmMetrics(
            metrics_csv=FileUpload(df),
            metrics_json=df.to_json(orient="records"),
            analysis_date=datetime.now().isoformat(),
        )
        created_metrics = pb.create_record("firm_metrics", asdict(firm_metrics))

        get_file = pb.get_file(
            "firm_metrics", created_metrics, created_metrics["metrics_csv"]
        )
        print("Created metrics:", created_metrics)

        # get_dataframe
        df = pb.get_dataframe("firm_metrics")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        pb.delete_full_list("firms")
        pb.delete_full_list("accounts")
        pb.delete_full_list("firm_metrics")
        pb.logout()
