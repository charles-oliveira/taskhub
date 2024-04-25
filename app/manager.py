import json

from .queue import Queue
from .task_manager import Task


class Manager:
    def __init__(self, name_file_json):
        self.name_file_json = name_file_json
        self.tasks = Queue()  # Usar a fila encadeada para armazenar as tarefas
        self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.name_file_json, "r") as file:
                data_json = json.load(file)
                for task_json in data_json:
                    task = Task.from_json(task_json)
                    # Adicionar a tarefa à fila usando enqueue
                    self.tasks.enqueue(task)
            if not self.tasks.is_empty():
                print(f"{self.tasks.size} tarefas carregadas com sucesso.")
        except FileNotFoundError:
            print("Nenhuma tarefa carregada.")

    def save_tasks(self):
        data_json = []
        # Criar uma fila temporária para armazenar as tarefas enquanto salvamos
        temp_queue = Queue()

        while not self.tasks.is_empty():
            task = self.tasks.dequeue()  # Remover tarefa da fila principal
            # Adicionar tarefa ao arquivo JSON
            data_json.append(task.to_json())
            temp_queue.enqueue(task)  # Adicionar tarefa à fila temporária

        while not temp_queue.is_empty():
            # Restaurar tarefas na fila principal
            self.tasks.enqueue(temp_queue.dequeue())

        with open(self.name_file_json, "w") as file:
            json.dump(data_json, file)

    def add_task(self, description, priority, status):
        new_task = Task(description, priority, status)
        self.tasks.enqueue(new_task)  # Adicionar a nova tarefa à fila
        self.save_tasks()

    def remove_task(self, indice):
        if indice < 0 or indice >= self.tasks.size:
            print("Índice inválido.")
            return

        # Criar uma fila temporária para armazenar as tarefas enquanto removemos
        temp_queue = Queue()
        current_index = 0

        while not self.tasks.is_empty():
            task = self.tasks.dequeue()  # Remover tarefa da fila principal
            if current_index != indice:
                # Se não for o índice da tarefa a ser removida, adicioná-la à fila temporária
                temp_queue.enqueue(task)
            current_index += 1

        while not temp_queue.is_empty():
            # Restaurar tarefas na fila principal
            self.tasks.enqueue(temp_queue.dequeue())

        self.save_tasks()
        print("Tarefa removida com sucesso!")

    def edit_task(self, indice):
        # Criar uma fila temporária para armazenar as tarefas enquanto editamos
        temp_queue = Queue()

        while not self.tasks.is_empty():
            task = self.tasks.dequeue()  # Remover tarefa da fila principal
            if indice == 0:
                description = input("Nova descrição da tarefa: ")
                priority = input("Nova prioridade da tarefa: ")
                status = input("Novo status da tarefa: ")
                task.description = description
                task.priority = priority
                task.status = status
            temp_queue.enqueue(task)  # Adicionar tarefa à fila temporária
            indice -= 1

        while not temp_queue.is_empty():
            # Restaurar tarefas na fila principal
            self.tasks.enqueue(temp_queue.dequeue())

        self.save_tasks()

    def get_tasks(self):
        if not self.tasks.is_empty():
            print("\nTarefas:")
            # Criar uma fila temporária para armazenar as tarefas enquanto exibimos
            temp_queue = Queue()
            current_index = 0

            while not self.tasks.is_empty():
                task = self.tasks.dequeue()  # Remover tarefa da fila principal
                print(
                    f"{current_index}. {task.description} - {task.priority} - {task.status}")  # Exibir o índice da tarefa
                temp_queue.enqueue(task)  # Adicionar tarefa à fila temporária
                current_index += 1

            while not temp_queue.is_empty():
                # Restaurar tarefas na fila principal
                self.tasks.enqueue(temp_queue.dequeue())
        else:
            print("Não há tarefas cadastradas.")
