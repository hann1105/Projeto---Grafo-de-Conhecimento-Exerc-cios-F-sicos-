import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


#Base de conhecimento - Aluno, objetivo, exercício, grupo muscular
base=pd.DataFrame({
    'head':['Paola','Paola','Paola', 'agachamento','Lucas'],
    'relacao':['tem objetivo','treina', 'tem objetivo','trabalha','tem objetivo'],
    'tail':['Hipertrofia ','agachamento','Emagrecimento','Quadriceps', 'Hipertrofia']
})
print("-------------------- Base de Conhecimento ----------------------")
print(base)

#Classe do Grafo de Conhecimento

class GrafoDeConhecimento:
    def __init__(self):
        self.grafo={}

    def adicionar_no(self,no):
        if no not in self.grafo:
            self.grafo[no]=[]

    def remover_no(self,no):
        if no in self.grafo:
            del self.grafo[no]
            for n in self.grafo:
                self.grafo[n]=[rel for rel in self.grafo[n] if rel [1]!=no]

    def adicionar_relacionamento(self, head,relation,tail):
        if head not in self.grafo:
            self.adicionar_no(head)
        
        if tail not in self.grafo:
            self.adicionar_no(tail)
        
        self.grafo[head].append((relation,tail))

    def remover_relacionamento(self, head, relation, tail):
        if head in self.grafo:
            self.grafo[head] = [
                r for r in self.grafo[head]
                if not (r[0] == relation and r[1] == tail)
            ]

    def consultar_relacionamentos_de(self, no):
        if no in self.grafo:
            return self.grafo[no]
        else:
            print(f"Nó '{no}' não existe.")
            return []

    def listar_nos(self):
        return list(self.grafo.keys())

    def listar_relacionamentos(self):
        triplas = []
        for head in self.grafo:
            for relation, tail in self.grafo[head]:
                triplas.append((head, relation, tail))
        return triplas
    
    def mostrar_grafo(self):

        # Criar grafo direcionado
        G = nx.DiGraph()

        # Adiciona as triplas ao grafo
        for head, relation, tail in self.listar_relacionamentos():
            G.add_edge(head, tail, label=relation)

        # Layout
        pos = nx.spring_layout(G, seed=42)

        # Labels das arestas
        labels = nx.get_edge_attributes(G, 'label')

        # Desenho
        plt.figure(figsize=(12, 10))
        nx.draw(G, pos, with_labels=True, node_size=2000, font_size=12, node_color='lightblue')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10)

        plt.title('Grafo de Conhecimento - Academia')
        plt.show()

            

# ============================================================
#          INTEGRAÇÃO DO DATAFRAME COM O GRAFO
# ============================================================

kg = GrafoDeConhecimento()

# Carrega cada linha da base de conhecimento para o grafo
for _, row in base.iterrows():
    kg.adicionar_relacionamento(
        head=row['head'],
        relation=row['relacao'],
        tail=row['tail']
    )

#Menu de opções para o usuário

class Menu:
    def __init__(self):
        self.grafo=kg

    def mostrar_opcoes(self):
        print("-------------------- MENU------------------")
        print("1 - Inserir nó ")
        print("2 - Remover nó ")
        print("3 - Inserir relacionamento ")
        print("4 - Remover relacionamento ")
        print("5 - Consultar relacionamento ")
        print("6 - Listar nós ")
        print("7 - Listar Relacionamentos ")
        print("8 - Ver Base de conhecimento")
        print("9 - Mostrar grafo")
        print("10 -Encerrar")

    def inicio(self):
        self.menu=Menu()
        while True:
            self.menu.mostrar_opcoes()

            opcao=int(input("Digite a ação que deseja para o grafo: "))
            if opcao== 1:
                no= input("Digite o nó que deseja adicionar: ")
                self.grafo.adicionar_no(no)
                print("Nó adicionado com sucesso!")

            elif opcao== 2:
                no=input("Digite o nó que deseja remover: ")
                self.grafo.remover_no(no)
                print("Nó removido com sucesso!")
                
            elif opcao==3:
                head=input("Adicione o Head: ")
                relation=input("Adicione a relação: ")
                tail=input("Adicione o final: ")
                self.grafo.adicionar_relacionamento(head,relation,tail)
                print("Relação adicionada com sucesso!")

            elif opcao ==4:
                head=input("Digite o Head que deseja remover: ")
                relation=input("Digite a relação que deseja remover: ")
                tail=input("Digite o destino que deseja remover:: ")
                self.grafo.remover_relacionamento(head,relation,tail)
                print("Relação removida com sucesso!")

            elif opcao==5:
                no=input("Qual o nome que deseja consultar? ")
                self.grafo.consultar_relacionamentos_de(no)

            elif opcao==6:
                print("------NÓS-----")
                for t in self.grafo.listar_nos():
                    print(t)

            elif opcao==7:
                print("----- RELAÇÕES-----")
                for t in self.grafo.listar_relacionamentos():
                    print(t)

            elif opcao==8:
                print(base)

            elif opcao==9:
                self.grafo.mostrar_grafo()

            elif opcao==10:
                print("Encerrando...")
                break

            else:
                print("Opção inválida, tente novamente!")

if __name__ == "__main__":
    menu=Menu()
    menu.inicio()