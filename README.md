## Run project

```bash
docker-compose up
```

## Usage API

1. POST /api/people/ - Create person

#### Required fields

- "name": string
- "topics": list

#### Response 201 (example)
```json
{
    "id": "Garry",
    "topics": ["books", "magic", "movies"]
}
```

2. POST /api/people/pk/trust_connections/ - Create/update trust connection between 2 persons

pk - ID of the Person from whom you want to create/update trust connection <br />
Number of fields - unlimited

##### Required fields

- person_id: int
- person_id: int
- ....
- person_id: int

#### Response 201

3. POST /api/messages/ - Send message based on people topics and trust connection level

##### Required fields

- "text": string
- "topics": list
- "from_person_id": int
- "min_trust_level": int

#### Response 201 (example)
```json
{
    "Garry": ["Hermione", "Rone"]
}
```

4. POST /api/path/ - Send message based on people topic and trust connection level in whole network

##### Required fields

- "text": string
- "topics": list
- "from_person_id": int
- "min_trust_level": int

#### Response 201 (example)
```json
{
    "from": "Garry",
    "path": ["Hermione"]
}
```

### Run tests
```bash
python trust_network/manage.py test api.tests
```
