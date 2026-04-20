document.addEventListener('DOMContentLoaded', function () {
    if (!requireAuth()) return;
    const form = document.getElementById('todo-form');
    const resetButton = document.getElementById('todo-reset');
    const messageEl = document.getElementById('todo-message');
    const todoList = document.getElementById('todo-list');
    const emptyState = document.getElementById('empty-state');

    async function loadTodos() {
        try {
            const todos = await fetchJson('/todos/', {
                method: 'GET',
                headers: authHeaders(),
            });
            renderTodos(todos);
        } catch (error) {
            todoList.innerHTML = '<p class="form-error">Unable to load todos.</p>';
        }
    }

    function renderTodos(todos) {
        if (!todos.length) {
            emptyState.style.display = 'block';
            todoList.innerHTML = '';
            return;
        }
        emptyState.style.display = 'none';
        todoList.innerHTML = todos
            .map(todo => {
                return `
                    <div class="todo-card${todo.complete ? ' todo-complete' : ''}">
                        <div class="todo-header">
                            <strong>${todo.title}</strong>
                            <span class="todo-priority">Priority ${todo.priority}</span>
                        </div>
                        <p>${todo.description}</p>
                        <div class="todo-actions">
                            <button class="button button-secondary todo-edit" data-id="${todo.id}">Edit</button>
                            <button class="button button-danger todo-delete" data-id="${todo.id}">Delete</button>
                        </div>
                    </div>
                `;
            })
            .join('');
        attachTodoActions();
    }

    function attachTodoActions() {
        document.querySelectorAll('.todo-edit').forEach(button => {
            button.addEventListener('click', async function () {
                const todoId = this.dataset.id;
                await populateTodoForm(todoId);
            });
        });

        document.querySelectorAll('.todo-delete').forEach(button => {
            button.addEventListener('click', async function () {
                const todoId = this.dataset.id;
                await deleteTodo(todoId);
            });
        });
    }

    async function populateTodoForm(id) {
        try {
            const todo = await fetchJson(`/todos/todo/${id}`, {
                method: 'GET',
                headers: authHeaders(),
            });
            document.getElementById('todo-id').value = todo.id;
            document.getElementById('title').value = todo.title;
            document.getElementById('description').value = todo.description;
            document.getElementById('priority').value = todo.priority;
            document.getElementById('complete').value = todo.complete ? 'true' : 'false';
            messageEl.textContent = 'Editing todo. Click Save to update.';
        } catch (error) {
            messageEl.textContent = error.detail || 'Unable to load the todo item.';
            messageEl.classList.add('form-error');
        }
    }

    async function deleteTodo(id) {
        try {
            await fetchJson(`/todos/todo/${id}`, {
                method: 'DELETE',
                headers: authHeaders(),
            });
            messageEl.textContent = 'Todo deleted successfully.';
            messageEl.classList.remove('form-error');
            await loadTodos();
        } catch (error) {
            messageEl.textContent = error.detail || 'Unable to delete todo.';
            messageEl.classList.add('form-error');
        }
    }

    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        const id = document.getElementById('todo-id').value;
        const data = {
            title: document.getElementById('title').value.trim(),
            description: document.getElementById('description').value.trim(),
            priority: Number(document.getElementById('priority').value),
            complete: document.getElementById('complete').value === 'true',
        };

        try {
            if (id) {
                await fetchJson(`/todos/todo/${id}`, {
                    method: 'PUT',
                    headers: authHeaders(),
                    body: JSON.stringify(data),
                });
                messageEl.textContent = 'Todo updated successfully.';
            } else {
                await fetchJson('/todos/todo/', {
                    method: 'POST',
                    headers: authHeaders(),
                    body: JSON.stringify(data),
                });
                messageEl.textContent = 'Todo added successfully.';
            }
            messageEl.classList.remove('form-error');
            form.reset();
            document.getElementById('todo-id').value = '';
            await loadTodos();
        } catch (error) {
            messageEl.textContent = error.detail || 'Unable to save todo.';
            messageEl.classList.add('form-error');
        }
    });

    resetButton.addEventListener('click', function () {
        form.reset();
        document.getElementById('todo-id').value = '';
        messageEl.textContent = '';
    });

    document.getElementById('logout-button')?.addEventListener('click', function () {
        clearAuthToken();
        window.location.href = '/login';
    });

    loadTodos();
});
