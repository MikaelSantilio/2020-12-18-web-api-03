# 2020-12-18-web-api-03

## Insomnia Export

[Insomnia_2020-12-18.json](https://github.com/MikaelSantilio/2020-12-18-web-api-03/blob/master/Insomnia_2020-12-18.json)

## endpoints

```json
{
  "/endpoints/": [
    "get"
  ],
  "/reports/": [
    "get"
  ],
  "/profiles/": [
    "get",
    "post"
  ],
  "/profiles/{id}": [
    "get",
    "put",
    "delete"
  ],
  "/profile-posts/": [
    "get"
  ],
  "/profile-posts/{id}": [
    "get"
  ],
  "/posts-comments/": [
    "get"
  ],
  "/posts-comments/{id}": [
    "get"
  ],
  "/posts/{post_id}/comments": [
    "get",
    "post"
  ],
  "/posts/{post_id}/comments/{comment_id}": [
    "get",
    "put",
    "delete"
  ],
  "/import/{filename}": [
    "post"
  ]
}
```