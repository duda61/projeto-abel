import os
from datetime import datetime
from typing import List, Optional


class Task:
    """
    Representa uma tarefa com atributos como nome, prioridade, categoria,
    data de criação, status (pendente/concluída) e data de conclusão.
    """
    def __init__(self, nome: str, prioridade: str, categoria: str):
        self.nome = nome  # Nome da tarefa
        self.prioridade = prioridade.lower()  # Prioridade (baixa, média, alta)
        self.categoria = categoria  # Categoria da tarefa (ex: trabalho, pessoal)
        self.data_criacao = datetime.now()  # Data e hora em que a tarefa foi criada
        self.concluida = False  # Status inicial da tarefa (pendente)
        self.data_conclusao = None  # Data de conclusão (nula enquanto não concluída)

    def concluir(self):
        """
        Marca a tarefa como concluída e registra a data de conclusão.
        """
        self.concluida = True
        self.data_conclusao = datetime.now()

    def to_line(self) -> str:
        """
        Converte os atributos da tarefa para uma linha de texto formatada,
        para ser salva em arquivo.
        """
        return f"{self.nome};{self.prioridade};{self.categoria};{self.data_criacao.isoformat()};{self.concluida};{self.data_conclusao}"

    @staticmethod
    def from_line(linha: str):
        """
        Converte uma linha de texto de um arquivo para um objeto `Task`.
        """
        nome, prioridade, categoria, data_criacao, concluida, data_conclusao = linha.strip().split(";")
        task = Task(nome, prioridade, categoria)
        task.data_criacao = datetime.fromisoformat(data_criacao)
        task.concluida = concluida == "True"
        if data_conclusao != "None":
            task.data_conclusao = datetime.fromisoformat(data_conclusao)
        return task


class TaskManager:
    """
    Gerencia a lista de tarefas, permitindo adicionar, listar, concluir,
    remover tarefas e salvá-las em um arquivo.
    """
    def __init__(self, arquivo="tarefas.txt"):
        self.arquivo = arquivo  # Nome do arquivo onde as tarefas são salvas
        self.tasks: List[Task] = self.carregar_tarefas()  # Carrega tarefas do arquivo

    def adicionar_tarefa(self, nome: str, prioridade: str, categoria: str):
        """
        Adiciona uma nova tarefa ao gerenciador. Valida se a prioridade é válida
        e se o nome da tarefa já existe.
        """
        if prioridade.lower() not in {"baixa", "média", "alta"}:
            raise ValueError("Prioridade deve ser 'baixa', 'média' ou 'alta'.")
        if any(t.nome == nome for t in self.tasks):
            raise ValueError("Tarefa já existe!")
        self.tasks.append(Task(nome, prioridade, categoria))
        self.salvar_tarefas()

    def listar_tarefas(self, concluida: Optional[bool] = None) -> List[Task]:
        """
        Retorna a lista de tarefas. Pode filtrar por status (pendente/concluída).
        """
        return [t for t in self.tasks if concluida is None or t.concluida == concluida]

    def concluir_tarefa(self, nome: str):
        """
        Marca uma tarefa como concluída, buscando-a pelo nome.
        """
        tarefa = self.encontrar_tarefa(nome)
        tarefa.concluir()
        self.salvar_tarefas()

    def remover_tarefa(self, nome: str):
        """
        Remove uma tarefa pelo nome, se ela existir.
        """
        self.tasks = [t for t in self.tasks if t.nome != nome]
        self.salvar_tarefas()

    def salvar_tarefas(self):
        """
        Salva todas as tarefas em um arquivo de texto, uma por linha.
        """
        with open(self.arquivo, "w") as f:
            for t in self.tasks:
                f.write(t.to_line() + "\n")

    def carregar_tarefas(self) -> List[Task]:
        """
        Carrega as tarefas salvas em um arquivo de texto, caso ele exista.
        """
        if not os.path.exists(self.arquivo):
            return []
        with open(self.arquivo, "r") as f:
            return [Task.from_line(linha) for linha in f]

    def encontrar_tarefa(self, nome: str) -> Task:
        """
        Busca uma tarefa pelo nome e a retorna. Levanta um erro se não encontrada.
        """
        for t in self.tasks:
            if t.nome == nome:
                return t
        raise ValueError("Tarefa não encontrada.")


def menu_principal():
    """
    Exibe o menu principal do gerenciador de tarefas e lida com a interação do usuário.
    """
    manager = TaskManager()

    while True:
        print("\n=== GERENCIADOR DE TAREFAS ===")
        print("1. Adicionar Tarefa")
        print("2. Listar Tarefas")
        print("3. Concluir Tarefa")
        print("4. Remover Tarefa")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        try:
            if opcao == "1":
                # Adicionar nova tarefa
                nome = input("Nome: ")
                prioridade = input("Prioridade (baixa/média/alta): ")
                categoria = input("Categoria: ")
                manager.adicionar_tarefa(nome, prioridade, categoria)
                print("Tarefa adicionada!")

            elif opcao == "2":
                # Listar tarefas
                status = input("Filtrar por status? (pendente/concluída/todas): ").lower()
                if status == "pendente":
                    tarefas = manager.listar_tarefas(concluida=False)
                elif status == "concluída":
                    tarefas = manager.listar_tarefas(concluida=True)
                else:
                    tarefas = manager.listar_tarefas()
                for t in tarefas:
                    print(f"{t.nome} - {t.prioridade.capitalize()} - {t.categoria} - {'Concluída' if t.concluida else 'Pendente'}")

            elif opcao == "3":
                # Concluir tarefa
                nome = input("Nome da tarefa para concluir: ")
                manager.concluir_tarefa(nome)
                print("Tarefa concluída!")

            elif opcao == "4":
                # Remover tarefa
                nome = input("Nome da tarefa para remover: ")
                manager.remover_tarefa(nome)
                print("Tarefa removida!")

            elif opcao == "5":
                # Sair
                print("Saindo...")
                break

            else:
                print("Opção inválida!")

        except ValueError as e:
            print(f"Erro: {e}")
        input("Pressione Enter para continuar...")


if __name__ == "__main__":
    menu_principal() 