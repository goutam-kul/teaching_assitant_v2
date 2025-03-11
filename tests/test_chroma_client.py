import pytest
import os
import shutil
from src.database.chroma_client import ChromaClient

@pytest.fixture(scope="function")
def test_db_path(tmp_path):
    """Fixture to create a temporary database path for testing."""
    db_path = tmp_path / "test_chroma_db"
    yield str(db_path)
    # Cleanup after tests
    if os.path.exists(db_path):
        shutil.rmtree(db_path)

def test_singleton_pattern(test_db_path):
    """Test that ChromaClient follows the singleton pattern."""
    client1 = ChromaClient(test_db_path)
    client2 = ChromaClient(test_db_path)
    assert client1 is client2
    assert client1.client is client2.client


def test_create_collection(test_db_path):
    """Test creating a new collection."""
    client = ChromaClient(test_db_path)

    # Create a new collection
    collection_name = "test_collection"
    collection = client.create_collection(collection_name)
    assert collection_name in client.list_collections()
    assert collection is not None

def test_delete_collection(test_db_path):
    """Test deleting and existing collection."""
    client = ChromaClient(test_db_path)

    # Create a new collection
    collection_name = "test_collection"
    client.create_collection(collection_name)
    assert collection_name in client.list_collections()

    # Delete the collection
    client.delete_collection(collection_name)
    assert collection_name not in client.list_collections()

def test_list_collections(test_db_path):
    """Test listing all collections."""
    client = ChromaClient(test_db_path)

    # Create two collections
    collection_name1 = "test_collection1"
    collection_name2 = "test_collection2"
    client.create_collection(collection_name1)
    client.create_collection(collection_name2)

    # List all collections
    collections = client.list_collections()
    assert collection_name1 in collections
    assert collection_name2 in collections
    
def test_create_collection_idempotent(test_db_path):
    """Test creating the same collection multiple times in idempotent."""
    client = ChromaClient(test_db_path)

    # Create a new collection
    collection_name = "test_collection"
    collection1 = client.create_collection(collection_name)
    collection2 = client.create_collection(collection_name)

    assert collection1.name == collection2.name
    assert collection1 is not None
    assert collection2 is not None

