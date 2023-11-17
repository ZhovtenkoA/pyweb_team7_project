from starlette import status


def test_get_unauthorized(client, comment):
    response = client.get("/api/comments/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

# def test_create_image(client, image):
#
#     response = client.post(
#         "/api/comments",
#         json=image,
#         headers={"Authorization": f"Bearer {token}"},
#     )
#
#     assert response.status_code == status.HTTP_201_CREATED


def test_create_comment(client, comment, token, image, monkeypatch):
    async def mock_get_image_by_id(*args, **kwargs):
        return image

    monkeypatch.setattr("pyweb_team7_project.routes.comments.comments_repo.get_image_by_id", mock_get_image_by_id)

    response = client.post(
        "/api/comments",
        json=comment,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["content"] == comment.get("content")
    assert data["image_id"] == comment.get("image_id")

