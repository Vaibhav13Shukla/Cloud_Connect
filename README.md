# ☁️ CloudConnect – Cloud Resource Management System

### A Modular, Domain-Driven Python Application for Managing Cloud Resources

---

## 📘 Overview

**CloudConnect** is a console-based application that simulates a **cloud resource management system**.
It allows users to **create**, **start**, **stop**, and **delete** various types of cloud resources — such as:

* **AppService**
* **StorageAccount**
* **CacheDB**

The application is designed using **Domain-Driven Design (DDD)** principles and integrates multiple **software design patterns** to ensure scalability, maintainability, and clean separation of concerns.

---

## 🧩 Key Features

* 🏗️ **DDD-based layered architecture**
  (Domain, Application, Infrastructure, Interface layers)
* 🧠 **State Pattern** for resource lifecycle management
* 🏭 **Factory Pattern** for resource creation
* 🧾 **Observer Pattern** for event-based logging
* 💾 **Repository Pattern** for persistence management
* 🧱 **SOLID Principle Compliant** design
* 🖥️ **Interactive CLI** for end-user operations
* 🪵 **Structured logging** and persistent log files

---

## 🧱 Project Structure

```
cloudconnect/
├── domain/
│   ├── entities/
│   │   ├── resource.py
│   │   ├── app_service.py
│   │   ├── storage_account.py
│   │   └── cache_db.py
│   ├── value_objects.py
│   ├── states.py
│   ├── exceptions.py
│   └── repositories/
│       └── resource_repository.py
│
├── application/
│   ├── factories/
│   │   └── resource_factory.py
│   ├── observers/
│   │   └── resource_observer.py
│   └── services/
│       └── resource_management_service.py
│
├── infrastructure/
│   ├── cli/
│   │   └── cloud_connect_cli.py
│   └── logging/
│       └── logger.py
│
└── main.py
```

---

## ⚙️ Architecture Overview

CloudConnect follows a **layered architecture** inspired by **Domain-Driven Design**:

| Layer                   | Responsibility                                                   | Example Components                                                |
| ----------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------- |
| **Domain**              | Core business logic, entities, value objects, states, exceptions | `Resource`, `ResourceState`, `ResourceId`                         |
| **Application**         | Application services and orchestration logic                     | `ResourceManagementService`, `ResourceFactory`, `LoggingObserver` |
| **Infrastructure**      | Frameworks, logging, and CLI input/output                        | `Logger`, `CloudConnectCLI`                                       |
| **Interface (main.py)** | Application entry point and bootstrapper                         | `main()`                                                          |

---

## 🧠 Core Design Patterns

### 🧩 1. **State Pattern**

Each resource (e.g., AppService, StorageAccount, CacheDB) transitions through distinct states:

* **Created → Started → Stopped → Deleted**

Each state is represented by a subclass of `ResourceState`:

```python
CreatedState, StartedState, StoppedState, DeletedState
```

This pattern encapsulates behavior changes depending on the current state of the resource and prevents invalid state transitions (e.g., deleting a resource before stopping it).

---

### 🏭 2. **Factory Pattern**

Used to **abstract and centralize resource creation** logic.

* Each resource type (`AppService`, `StorageAccount`, `CacheDB`) has its own factory (`AppServiceFactory`, etc.).
* `ResourceFactoryRegistry` dynamically retrieves the correct factory at runtime.

```python
factory_registry.register('AppService', AppServiceFactory())
resource = factory_registry.create_resource('AppService', resource_id, **kwargs)
```

---

### 👁️ 3. **Observer Pattern**

Implements **event-driven notifications** for resource state changes.

* `Resource` maintains a list of observers.
* `LoggingObserver` listens for events like **started**, **stopped**, or **deleted**.
* On each event, the observer triggers the `Logger` to persist messages.

```python
resource.attach_observer(logging_observer)
resource.notify_started()
```

---

### 💾 4. **Repository Pattern**

`ResourceRepository` abstracts data persistence and ensures uniqueness and retrieval of resources.

It provides CRUD-like behavior for domain entities:

```python
add(resource)
get(resource_id)
exists(resource_id)
```

---

### 🧱 5. **Value Object Pattern**

`ResourceId` acts as an immutable value object ensuring validation and equality based on content rather than identity.

---

## 🧩 SOLID Principles Compliance

| Principle                     | Implementation Example                                                                                                                                                             |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **S — Single Responsibility** | Each class has a single reason to change (e.g., `Logger` handles only logging).                                                                                                    |
| **O — Open/Closed**           | New resource types can be added without modifying existing code (extend factories).                                                                                                |
| **L — Liskov Substitution**   | All `Resource` subclasses (`AppService`, `StorageAccount`, `CacheDB`) can replace the base `Resource` class.                                                                       |
| **I — Interface Segregation** | Abstract base classes (`ResourceObserver`, `ResourceState`) define minimal and focused contracts.                                                                                  |
| **D — Dependency Inversion**  | High-level modules depend on abstractions, not concrete implementations (e.g., `ResourceManagementService` depends on interfaces like `ResourceRepository` and `ResourceFactory`). |

✅ **No SOLID principle violations detected**; architecture adheres strongly to DDD best practices.

---

## 🔁 Execution Flow

1. **Startup (`main.py`)**

   * Initializes `Logger`, `Repository`, `FactoryRegistry`, `Observer`, and `Service`.
   * Registers factories and starts CLI.

2. **User Interaction (`CloudConnectCLI`)**

   * CLI presents menu options for resource management.
   * User inputs drive operations like create/start/stop/delete.

3. **Resource Creation**

   * CLI calls `ResourceManagementService.create_resource()`.
   * The service uses `ResourceFactoryRegistry` to instantiate a concrete resource.
   * The resource is attached to a `LoggingObserver` and persisted via `ResourceRepository`.

4. **State Management**

   * Resource transitions are handled by the active `ResourceState` subclass.
   * Invalid transitions raise `InvalidStateTransitionError`.

5. **Event Logging**

   * Observers log state transitions via the `Logger`.
   * Logs are printed and persisted in the `/logs` directory.

---

## 🧰 Example Usage

### Run the Application

```bash
python main.py
```

### CLI Options

```
1. Create Resource
2. Start Resource
3. Stop Resource
4. Delete Resource
5. View Logs
6. Exit
```

### Example Interaction

```
> 1
Select resource type: AppService
Enter resource name: myapp
Select runtime: python
Select region: EastUS
Replica count: 3
✅ AppService 'myapp' created successfully!

> 2
Enter resource name: myapp
AppService started at 10:32 AM in EastUS
```

---

## 🪵 Logging

Logs are stored in `logs/` directory per resource type:

```
logs/
├── appservice.log
├── storageaccount.log
└── cachedb.log
```

Each entry includes a timestamp and action message:

```
[10:32 AM] AppService started at 10:32 AM in EastUS
```

---

## 🚀 Extending the System

### Adding a New Resource Type

1. Create a new subclass of `Resource`.
2. Define `_get_start_message`, `_get_stop_message`, `_get_delete_message`.
3. Implement a factory extending `ResourceFactory`.
4. Register the factory in `main.py`:

   ```python
   factory_registry.register('NewResourceType', NewResourceFactory())
   ```

---

## 🧑‍💻 Tech Stack

* **Language:** Python 3.10+
* **Architecture:** Domain-Driven Design
* **Design Patterns:** State, Factory, Observer, Repository, Value Object
* **CLI Framework:** Built-in Python I/O
* **Logging:** Custom file-based logger

---

## 🧩 Conclusion

**CloudConnect** demonstrates a **production-grade, extensible architecture** suitable for cloud management systems.
Its design showcases:

* Proper **DDD boundaries**
* Clean **code modularity**
* Strong **adherence to SOLID**
* Multiple **behavioral and creational design patterns**

This codebase is ideal for **educational demonstration**, **viva preparation**, or as a **foundation for scalable Python enterprise systems**.

---