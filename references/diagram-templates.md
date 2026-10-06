# Diagram Templates

Architecture diagram templates. Mermaid is the primary format — GitHub renders it natively. SVG is the fallback for complex architectures.

Include a diagram only when confirmed visual preferences allow it and source-backed relationships help the intended reader. Skip diagrams for simple projects or unsupported relationships. Treat every example below as syntax/layout guidance, not target-project evidence. Default Mermaid themes are acceptable. Prefer 3–8 readable nodes; group or link detailed docs for larger graphs. Create SVG assets only when explicitly authorized.

---

## Diagram Type Selection

| Project Type | Primary Diagram | Secondary (if complex) |
|---|---|---|
| **Microservice** | Architecture Graph | Sequence Diagram |
| **Frontend-Backend** | Architecture Graph | ER Diagram (if DB-heavy) |
| **Monolithic Layered** | Architecture Graph | Class Diagram (if OOP-heavy) |
| **Event-Driven** | Architecture Graph | Sequence Diagram |
| **CLI Tool** | Flowchart | — |
| **Library / Package** | Class Diagram | Flowchart |
| **API Service** | Sequence Diagram | ER Diagram |
| **Data Pipeline** | Flowchart | ER Diagram |
| **Stateful App** | State Diagram | Sequence Diagram |
| **Default / Unknown** | Architecture Graph | — |

---

## Color System

All diagrams use a consistent color palette. Apply colors via `classDef` and `style` directives.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| **Client / Frontend** | Blue | `#3B82F6` | UI, mobile, SPA |
| **Gateway / Load Balancer** | Amber | `#F59E0B` | API gateways, proxies |
| **Service / Logic** | Emerald | `#10B981` | Business logic, workers |
| **Data / Storage** | Violet | `#8B5CF6` | Databases, caches, queues |
| **External / Third-party** | Rose | `#F43F5E` | External APIs, webhooks |
| **Auth / Security** | Orange | `#F97316` | Auth modules, JWT |
| **Message / Queue** | Cyan | `#06B6D4` | Kafka, RabbitMQ, pub/sub |

### Applying Colors in Mermaid

Treat the following as a flowchart styling fragment, not a complete diagram. Insert after a `flowchart`/`graph` declaration only when styling is useful.

```text
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#3B82F6',
  'primaryTextColor': '#fff',
  'lineColor': '#64748B',
  'fontSize': '14px'
}}}%%

classDef client fill:#3B82F6,stroke:#2563EB,color:#fff,stroke-width:2px
classDef service fill:#10B981,stroke:#059669,color:#fff,stroke-width:2px
classDef data fill:#8B5CF6,stroke:#7C3AED,color:#fff,stroke-width:2px
classDef gateway fill:#F59E0B,stroke:#D97706,color:#fff,stroke-width:2px
classDef external fill:#F43F5E,stroke:#E11D48,color:#fff,stroke-width:2px
classDef auth fill:#F97316,stroke:#EA580C,color:#fff,stroke-width:2px
classDef queue fill:#06B6D4,stroke:#0891B2,color:#fff,stroke-width:2px
```

**Rules:**
- Use diagram-specific syntax; flowchart `classDef` is not valid sequence-diagram syntax.
- For flowcharts, place the graph declaration before styling; apply classes to the intended nodes.
- Use `%%{init}%%` for optional theme customization, or keep a readable default theme.
- Use dark text on light fills and light text only on sufficiently dark fills; check contrast.
- Prefer restrained styling and readable labels over mandatory colors.

---

## Mermaid Templates

### 1. Architecture Graph (Microservice)

For projects with multiple independent services communicating via RPC/HTTP.

````mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '14px'}}}%%
graph LR
    A[Client<br/>React] --> B[API Gateway<br/>Express]
    B --> C[User Service<br/>Go]
    B --> D[Order Service<br/>Go]
    B --> E[Payment Service<br/>Go]
    C --> F[(PostgreSQL)]
    D --> F
    E --> G[(Redis)]

    classDef client fill:#3B82F6,stroke:#2563EB,color:#fff,stroke-width:2px
    classDef gateway fill:#F59E0B,stroke:#D97706,color:#fff,stroke-width:2px
    classDef service fill:#10B981,stroke:#059669,color:#fff,stroke-width:2px
    classDef data fill:#8B5CF6,stroke:#7C3AED,color:#fff,stroke-width:2px

    class A client
    class B gateway
    class C,D,E service
    class F,G data
````

**Rules:**
- `graph LR` for left-to-right flow
- Node labels: `Name<br/>Technology` (two lines)
- Database nodes: `[(Name)]` for cylinder shape
- Max 8 nodes. If more services exist, group related ones
- Apply color classes to all nodes

---

### 2. Architecture Graph (Frontend-Backend)

For SPA + API + database projects.

````mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '14px'}}}%%
graph LR
    A[Frontend<br/>Vue.js] --> B[API Server<br/>Express]
    B --> C[Auth Module<br/>JWT]
    B --> D[Business Logic<br/>TypeScript]
    D --> E[(PostgreSQL)]
    D --> F[(Redis)]

    classDef client fill:#3B82F6,stroke:#2563EB,color:#fff,stroke-width:2px
    classDef service fill:#10B981,stroke:#059669,color:#fff,stroke-width:2px
    classDef auth fill:#F97316,stroke:#EA580C,color:#fff,stroke-width:2px
    classDef data fill:#8B5CF6,stroke:#7C3AED,color:#fff,stroke-width:2px

    class A client
    class B,D service
    class C auth
    class E,F data
````

---

### 3. Architecture Graph (Monolithic Layered)

For traditional MVC or layered architecture.

````mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '14px'}}}%%
graph TD
    A[UI Layer<br/>React] --> B[Controller Layer<br/>Express]
    B --> C[Service Layer<br/>TypeScript]
    C --> D[Data Layer<br/>Prisma]
    D --> E[(PostgreSQL)]

    classDef client fill:#3B82F6,stroke:#2563EB,color:#fff,stroke-width:2px
    classDef service fill:#10B981,stroke:#059669,color:#fff,stroke-width:2px
    classDef data fill:#8B5CF6,stroke:#7C3AED,color:#fff,stroke-width:2px

    class A client
    class B,C service
    class D,E data
````

**Rules:**
- `graph TD` for top-down flow
- Each layer is one node
- Max 5 layers

---

### 4. Architecture Graph (Event-Driven)

For projects using message queues or event buses.

````mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '14px'}}}%%
graph LR
    A[Producer<br/>Express] --> B[Message Queue<br/>Kafka]
    B --> C[Consumer A<br/>Go]
    B --> D[Consumer B<br/>Python]
    B --> E[Consumer C<br/>Node.js]
    C --> F[(PostgreSQL)]
    D --> G[(MongoDB)]
    E --> H[(Redis)]

    classDef service fill:#10B981,stroke:#059669,color:#fff,stroke-width:2px
    classDef queue fill:#06B6D4,stroke:#0891B2,color:#fff,stroke-width:2px
    classDef data fill:#8B5CF6,stroke:#7C3AED,color:#fff,stroke-width:2px

    class A,C,D,E service
    class B queue
    class F,G,H data
````

---

### 5. Class Diagram

For OOP-heavy projects with clear class hierarchies, inheritance, or composition.

````mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '14px'}}}%%
classDiagram
    class UserService {
        +findUser(id: string): User
        +createUser(data: CreateUserDto): User
        +updateUser(id: string, data: UpdateUserDto): User
        +deleteUser(id: string): void
    }
    class UserRepository {
        +findById(id: string): User
        +save(user: User): User
        +delete(id: string): void
    }
    class User {
        +id: string
        +name: string
        +email: string
        +createdAt: Date
    }
    class AuthService {
        +login(email: string, password: string): Token
        +verify(token: string): Payload
        +hashPassword(password: string): string
    }
    class CacheService {
        +get(key: string): any
        +set(key: string, value: any, ttl: number): void
        +delete(key: string): void
    }

    UserService --> UserRepository : uses
    UserService --> AuthService : uses
    UserService --> CacheService : uses
    UserRepository --> User : manages
    AuthService --> User : authenticates

    classDef service fill:#10B981,stroke:#059669,color:#fff,stroke-width:2px
    classDef auth fill:#F97316,stroke:#EA580C,color:#fff,stroke-width:2px
    classDef data fill:#8B5CF6,stroke:#7C3AED,color:#fff,stroke-width:2px
    classDef model fill:#3B82F6,stroke:#2563EB,color:#fff,stroke-width:2px

    class UserService,UserRepository,CacheService service
    class AuthService auth
    class User model
````

**Rules:**
- Extract real class names and methods from source code
- Show key public methods only (max 5 per class)
- Include member variables for model/entity classes
- Use relationships: `-->` (uses), `--*` (composition), `--o` (aggregation), `<|--` (inheritance)
- Apply colors: services=green, auth=orange, models=blue, data=violet

---

### 6. ER Diagram (Entity Relationship)

For database-heavy projects. Shows tables, columns, and relationships.

````mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '14px'}}}%%
erDiagram
    USERS {
        uuid id PK
        string name
        string email UK
        string password_hash
        timestamp created_at
    }
    POSTS {
        uuid id PK
        uuid author_id FK
        string title
        text content
        timestamp published_at
    }
    COMMENTS {
        uuid id PK
        uuid post_id FK
        uuid author_id FK
        text content
        timestamp created_at
    }
    TAGS {
        uuid id PK
        string name UK
    }
    POST_TAGS {
        uuid post_id FK
        uuid tag_id FK
    }

    USERS ||--o{ POSTS : "writes"
    USERS ||--o{ COMMENTS : "writes"
    POSTS ||--o{ COMMENTS : "has"
    POSTS ||--o{ POST_TAGS : "tagged"
    TAGS ||--o{ POST_TAGS : "tagged"

    classDef entity fill:#3B82F6,stroke:#2563EB,color:#fff,stroke-width:2px
    classDef junction fill:#F59E0B,stroke:#D97706,color:#fff,stroke-width:2px

    class USERS,POSTS,COMMENTS,TAGS entity
    class POST_TAGS junction
````

**Rules:**
- Extract real table/column names from ORM models or migration files
- Show column types and constraints (PK, FK, UK)
- Use `||--o{` for one-to-many, `||--||` for one-to-one, `}o--o{` for many-to-many
- Junction tables: yellow/amber color
- Entity tables: blue color

---

### 7. Flowchart

For CLI tools, scripts, data pipelines, or process-heavy projects.

````mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '14px'}}}%%
flowchart TD
    A[Parse CLI Arguments] --> B{Config File Exists?}
    B -->|Yes| C[Load Config]
    B -->|No| D[Use Defaults]
    C --> E[Initialize Services]
    D --> E
    E --> F[Read Input]
    F --> G{Input Valid?}
    G -->|Yes| H[Process Data]
    G -->|No| I[Show Error & Exit]
    H --> J[Write Output]
    J --> K[Cleanup & Exit]

    classDef start fill:#3B82F6,stroke:#2563EB,color:#fff,stroke-width:2px
    classDef process fill:#10B981,stroke:#059669,color:#fff,stroke-width:2px
    classDef decision fill:#F59E0B,stroke:#D97706,color:#fff,stroke-width:2px
    classDef error fill:#F43F5E,stroke:#E11D48,color:#fff,stroke-width:2px
    classDef end fill:#8B5CF6,stroke:#7C3AED,color:#fff,stroke-width:2px

    class A start
    class C,D,E,F,H,J process
    class B,G decision
    class I error
    class K end
````

**Rules:**
- `flowchart TD` for top-down, `flowchart LR` for left-to-right
- Decision nodes use `{}` diamond shape
- Apply colors: start=blue, process=green, decision=amber, error=rose, end=violet
- Max 10 nodes

---

### 8. Sequence Diagram

For API-heavy projects showing request/response flow between components.

````mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '14px'}}}%%
sequenceDiagram
    participant Client as Client (React)
    participant API as API Gateway
    participant Auth as Auth Service
    participant User as User Service
    participant DB as PostgreSQL
    participant Cache as Redis

    Client->>API: POST /api/login
    API->>Auth: validateCredentials()
    Auth->>DB: SELECT user WHERE email = ?
    DB-->>Auth: User record
    Auth->>Auth: bcrypt.compare()
    Auth-->>API: JWT token
    API-->>Client: 200 OK + token

    Client->>API: GET /api/users/me (Bearer token)
    API->>Auth: verifyToken()
    Auth-->>API: decoded payload
    API->>Cache: GET user:{id}
    alt Cache hit
        Cache-->>API: cached user
    else Cache miss
        API->>User: findById(id)
        User->>DB: SELECT * FROM users WHERE id = ?
        DB-->>User: User record
        User-->>API: User object
        API->>Cache: SET user:{id} (TTL 300s)
    end
    API-->>Client: 200 OK + user data
````

**Rules:**
- Show real API endpoints and method calls from the project
- Use `alt`/`else` for conditional flows (cache hit/miss, error handling)
- Use `loop` for repeated operations
- Participants represent actual components/services
- Use native sequence-diagram theme/participant styling; never insert flowchart `classDef` or `class` directives

---

### 9. State Diagram

For stateful applications (order processing, workflows, game states, etc.).

````mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '14px'}}}%%
stateDiagram-v2
    [*] --> Pending
    Pending --> Processing : payment_received
    Processing --> Shipped : order_packed
    Processing --> Failed : stock_unavailable
    Shipped --> Delivered : delivery_confirmed
    Shipped --> Returned : customer_return
    Delivered --> [*]
    Failed --> Pending : retry
    Returned --> Refunded : return_approved
    Refunded --> [*]

    classDef initial fill:#64748B,stroke:#475569,color:#fff,stroke-width:2px
    classDef active fill:#3B82F6,stroke:#2563EB,color:#fff,stroke-width:2px
    classDef success fill:#10B981,stroke:#059669,color:#fff,stroke-width:2px
    classDef error fill:#F43F5E,stroke:#E11D48,color:#fff,stroke-width:2px
    classDef terminal fill:#64748B,stroke:#475569,color:#fff,stroke-width:2px

    class Pending active
    class Processing active
    class Shipped active
    class Delivered success
    class Failed error
    class Returned error
    class Refunded success
````

**Rules:**
- Extract real states from state machines, workflow engines, or order/status logic
- Show transition triggers (event names on arrows)
- Use `[*]` for start and end states
- Apply colors: active=blue, success=green, error=rose, terminal=gray

---

## SVG Fallback

Use an existing relevant SVG when available. Create a new SVG only when the developer explicitly requests or approves that supporting asset. For large graphs, group/split the verified relationships or link detailed documentation; node count and branding alone do not authorize asset creation.

### Dynamic Layout Algorithm

SVG nodes are positioned dynamically, not hardcoded.

**Horizontal layout (client → gateway → services → data):**
- Column width: 180px (120px node + 60px gap)
- Node height: 60px
- Vertical gap between nodes in same column: 80px (center-to-center)
- Columns: client (x=20) → gateway (x=200) → services (x=380) → data (x=560)

**Canvas sizing:**
- Width: `num_columns × 180 + 40`
- Height: `max_nodes_in_any_column × 80 + 40`
- viewBox: `0 0 {WIDTH} {HEIGHT}`

**Connector lines:**
- From source node right edge to target node left edge
- For 1:many connections: lines fan from source center to each target center
- Arrow marker: `<marker>` with `polygon points="0 0, 10 3.5, 0 7"`

**Node structure:**
```svg
<rect x="{X}" y="{Y}" width="120" height="60" rx="8" fill="{COLOR}"/>
<text x="{X+60}" y="{Y+25}" text-anchor="middle" fill="white" font-size="14" font-weight="bold">{NAME}</text>
<text x="{X+60}" y="{Y+45}" text-anchor="middle" fill="white" font-size="11">{TECH}</text>
```

**Color scheme (same as Mermaid palette):**
- Client/Frontend: `#3B82F6` (blue)
- Gateway: `#F59E0B` (amber)
- Services: `#10B981` (emerald)
- Auth: `#F97316` (orange)
- Data/DB: `#8B5CF6` (violet)
- Queue: `#06B6D4` (cyan)
- External: `#F43F5E` (rose)
- Arrows: `#64748B` (slate)

---

## Decision Logic

```
1. Check confirmed visuals/renderer preferences and the reader's need
2. If relationships lack evidence or add no value → omit the diagram
3. Select a diagram type that explains the actual interaction
4. Extract source-backed names and edges; prefer 3–8 nodes
5. Use valid diagram-specific syntax and readable default themes or restrained styling
6. If too large → group/split or link existing detailed docs
7. If portable rendering → use a concise prose explanation
8. Create SVG only with explicit approval of the asset path
```
