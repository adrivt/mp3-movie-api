def test_upload_csv(client, sample_csv_bytes):
    response = client.post(
        "/upload",
        files={"file": ("sample_data.csv", sample_csv_bytes, "text/csv")},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["rows"] == 6
    assert payload["columns"] == 2
    assert isinstance(payload["id"], int)
    assert payload["id"] > 0


def test_process_and_retrieve(client, uploaded_dataset_id, processing_body):
    response = client.post(
        f"/datasets/{uploaded_dataset_id}/process",
        json=processing_body,
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["validation_rows_removed"] == 1
    assert payload["cleaning_report"]["rows_before"] == 5
    assert payload["cleaning_report"]["rows_after"] == 3

    retrieved = client.get(f"/datasets/{uploaded_dataset_id}")

    assert retrieved.status_code == 200
    body = retrieved.json()
    assert body["total_rows"] == 3

    records = body["data"]
    assert [row["student_id"] for row in records] == [1, 2, 5]
    assert [row["score"] for row in records] == [80, 90, 85]


def test_retrieve_missing_dataset(client):
    response = client.get("/datasets/999")

    assert response.status_code == 404