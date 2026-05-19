#!/usr/bin/env bash

API_PREFIX="${API_PREFIX:-http://localhost:8000}"

echo "=== 1. Ping ==="
curl -s "$API_PREFIX/ping"

echo -e "

=== 2. Echo ==="
curl -s -X POST "$API_PREFIX/echo"  \
  -H "Content-Type: application/json"  \
  -d '{"hello":"world"}'

echo -e "

=== 3. Empty echo ==="
curl -s -X POST "$API_PREFIX/echo"

echo -e "

=== 4. Get token ==="
TOKEN=$(curl -s -X POST "$API_PREFIX/auth/token"  \
  -H "Content-Type: application/json"  \
  -d '{"username":"admin","password":"password123"}'  \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
echo "Token: ${TOKEN:0:20}..."

echo -e "
=== 5. Unauthorized ==="
curl -s "$API_PREFIX/books"

echo -e "

=== 6. Invalid token ==="
curl -s "$API_PREFIX/books" -H "Authorization: Bearer invalid"

echo -e "

=== 7. Create books ==="
curl -s -X POST "$API_PREFIX/books"  \
  -H "Content-Type: application/json"  \
  -H "Authorization: Bearer $TOKEN"  \
  -d '{"title":"1984","author":"Orwell"}'
echo ""

curl -s -X POST "$API_PREFIX/books"  \
  -H "Content-Type: application/json"  \
  -H "Authorization: Bearer $TOKEN"  \
  -d '{"title":"Animal Farm","author":"Orwell"}'
echo ""

curl -s -X POST "$API_PREFIX/books"  \
  -H "Content-Type: application/json"  \
  -H "Authorization: Bearer $TOKEN"  \
  -d '{"title":"The Old Man and the Sea","author":"Hemingway"}'
echo ""

echo -e "
=== 8. List all books ==="
curl -s "$API_PREFIX/books" -H "Authorization: Bearer $TOKEN"

echo -e "

=== 9. Search by author ==="
curl -s "$API_PREFIX/books?author=Orwell" -H "Authorization: Bearer $TOKEN"

echo -e "

=== 10. Search by title ==="
curl -s "$API_PREFIX/books?title=1984" -H "Authorization: Bearer $TOKEN"

echo -e "

=== 11. Search title + author ==="
curl -s "$API_PREFIX/books?title=1984&author=Orwell" -H "Authorization: Bearer $TOKEN"

echo -e "

=== 12. Paginate page=1 limit=2 ==="
curl -s "$API_PREFIX/books?page=1&limit=2" -H "Authorization: Bearer $TOKEN"

echo -e "

=== 13. Filter + paginate ==="
curl -s "$API_PREFIX/books?author=Orwell&page=1&limit=1" -H "Authorization: Bearer $TOKEN"

echo -e "

=== 14. Get book by ID ==="
BOOK_ID=$(curl -s "$API_PREFIX/books?limit=1" -H "Authorization: Bearer $TOKEN" | python3 -c "import sys,json; print(json.load(sys.stdin)['data'][0]['id'])")
curl -s "$API_PREFIX/books/$BOOK_ID" -H "Authorization: Bearer $TOKEN"

echo -e "

=== 15. Update book ==="
curl -s -X PUT "$API_PREFIX/books/$BOOK_ID"  \
  -H "Content-Type: application/json"  \
  -H "Authorization: Bearer $TOKEN"  \
  -d '{"title":"Animal Farm (Updated)","author":"George Orwell"}'

echo -e "

=== 16. Get 404 ==="
curl -s "$API_PREFIX/books/nonexistent" -H "Authorization: Bearer $TOKEN"

echo -e "

=== 17. Validation error (missing title) ==="
curl -s -X POST "$API_PREFIX/books"  \
  -H "Content-Type: application/json"  \
  -H "Authorization: Bearer $TOKEN"  \
  -d '{"author":"NoTitle"}'

echo -e "

=== 18. Auth validation error (contact message) ==="
curl -s -X POST "$API_PREFIX/auth/token"

echo -e "

=== 19. Delete book ==="
curl -s -o /dev/null -w "Status: %{http_code}" -X DELETE "$API_PREFIX/books/$BOOK_ID" -H "Authorization: Bearer $TOKEN"

echo -e "

=== 20. Confirm deleted ==="
curl -s "$API_PREFIX/books/$BOOK_ID" -H "Authorization: Bearer $TOKEN"

echo ""
