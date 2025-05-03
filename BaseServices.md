# Markdown
```http request
POST https://localhost:8088/api/v1/services/Markdown
Content-Type: application/json

{
    "description": "Markdown support for messages in chat",
    "initializer_code": "import markdownIt from 'https://cdn.jsdelivr.net/npm/markdown-it@14.1.0/+esm';\nwindow.md = markdownIt();",
    "formatting_code": "msg = md.render(msg)"
}
```