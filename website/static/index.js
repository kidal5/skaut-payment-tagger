function deleteTag(tagId) {
  fetch("/delete-tag", {
    method: "POST",
    body: JSON.stringify({ tagId: tagId }),
  }).then((_res) => {
    window.location.href = "/manage-tags";
  });
}
