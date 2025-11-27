import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Base de conhecimento
base = pd.DataFrame({
    'head': [
        'Paola', 'Lucas',
        'Paola', 'Lucas',
        'Agachamento', 'Rosca 21', 'Tríceps Testa', 'Elevação Pélvica', 'Puxada Alta', 'Leg 45°',
        'Agachamento', 'Rosca 21', 'Tríceps Testa','Leg 45°','Leg 45°',
        'Tríceps Testa','Elevação Pélvica','Leg 45°'
    ],
    'relacao': [
        'tem objetivo', 'tem objetivo',
        'treina', 'treina',
        'trabalha','trabalha','trabalha','trabalha','trabalha','trabalha',
        'ativa','ativa','ativa','ativa','ativa',
        'usa máquina','usa máquina','usa máquina'
    ],
    'tail': [
        'Emagrecimento', 'Hipertrofia',
        'Agachamento', 'Rosca 21',
        'Quadríceps','Bíceps','Tríceps','Glúteo','Costas','Quadríceps',
        'Glúteo','Antebraço','Ombros','Glúteo','Posterior de coxa',
        'banco e halteres','Aparelho de elevação','Leg Press'
    ]
})

print("-------------------- Base de Conhecimento ----------------------")
print(base)

# ================================================
# Classe Grafo de Conhecimento (Métodos Manuais)
# ================================================
class GrafoDeConhecimento:
    def __init__(self):
        self.grafo = {}

    # Adicionar nó manualmente
    def adicionar_no(self, no):
        existe = False
        for chave in self.grafo:
            if chave == no:
                existe = True
                break
        if not existe:
            self.grafo[no] = []
            print("Nó adicionado com sucesso!")
        else:
            print("Nó já existe.")

    # Remover nó manualmente
    def remover_no(self, no):
        novo_grafo = {}
        for chave in self.grafo:
            if chave != no:
                novas_relacoes = []
                for relacao, destino in self.grafo[chave]:
                    if destino != no:
                        novas_relacoes = novas_relacoes + [(relacao, destino)]
                novo_grafo[chave] = novas_relacoes
        self.grafo = novo_grafo
        print("Nó removido com sucesso!")

        # Atualizar a base
        global base
        nova_base = []
        for i in range(len(base)):
            linha = base.iloc[i].to_dict()
            if linha['head'] != no and linha['tail'] != no:
                nova_base = nova_base + [linha]
        base = pd.DataFrame(nova_base)

    # Adicionar relacionamento manualmente
    def adicionar_relacionamento(self, head, relation, tail, atualizar_base=True):
        if head not in self.grafo:
            self.adicionar_no(head)
        if tail not in self.grafo:
            self.adicionar_no(tail)

        relacoes_atuais = self.grafo[head]
        relacoes_atuais = relacoes_atuais + [(relation, tail)]
        self.grafo[head] = relacoes_atuais
        print("Relacionamento adicionado ao grafo!")

        if atualizar_base:
            global base
            nova_linha = {'head': head, 'relacao': relation, 'tail': tail}
            base = pd.concat([base, pd.DataFrame([nova_linha])], ignore_index=True)

    # Remover relacionamento manualmente
    def remover_relacionamento(self, head, relation, tail):
        if head in self.grafo:
            novas_relacoes = []
            for relacao_atual, destino in self.grafo[head]:
                if not (relacao_atual == relation and destino == tail):
                    novas_relacoes = novas_relacoes + [(relacao_atual, destino)]
            self.grafo[head] = novas_relacoes
            print("Relacionamento removido do grafo!")

            global base
            nova_base = []
            for i in range(len(base)):
                linha = base.iloc[i].to_dict()
                if not (linha['head'] == head and linha['relacao'] == relation and linha['tail'] == tail):
                    nova_base = nova_base + [linha]
            base = pd.DataFrame(nova_base)
        else:
            print("Relacionamento não encontrado")

    # Consultar relacionamentos de um nó
    def consultar_relacionamentos_de(self, no):
        if no in self.grafo:
            print(self.grafo[no])
            return
        else:
            print(f"Nó '{no}' não existe.")
            return []

    # Listar nós
    def listar_nos(self):
        lista = []
        for chave in self.grafo:
            lista = lista + [chave]
        return lista

    # Listar relacionamentos
    def listar_relacionamentos(self):
        triplas = []
        for head in self.grafo:
            for relation, tail in self.grafo[head]:
                triplas = triplas + [(head, relation, tail)]
        return triplas

    # Mostrar grafo completo
    def mostrar_grafo(self):
        G = nx.DiGraph()
        for head, relation, tail in self.listar_relacionamentos():
            G.add_node(head)
            G.add_node(tail)
            G.add_edge(head, tail, label=relation)

        
        alunos_objetivo = set(base[base['relacao'] == "tem objetivo"]['head'])
        alunos_treinam = set(base[base['relacao'] == "treina"]['head'])
        alunos = alunos_objetivo|alunos_treinam
        objetivos = set(base[base['relacao'] == "tem objetivo"]['tail'])
        exercicios = set(base[base['relacao'].isin(["trabalha", "ativa", "usa máquina"])]["head"])
        musculos = set(base[base['relacao'].isin(["trabalha", "ativa"])]["tail"])
        maquinas = set(base[base['relacao'] == "usa máquina"]["tail"])

        def cor_no(no):
            if no in alunos: return "skyblue"
            if no in exercicios: return "orange"
            if no in musculos: return "lightgreen"
            if no in objetivos: return "violet"
            if no in maquinas: return "grey"
            return "white"

        camadas = {
            "alunos": list(alunos),
            "objetivos": list(objetivos),
            "exercicios": list(exercicios),
            "musculos": list(musculos),
            "maquinas": list(maquinas),
        }

        pos = {}
        y = 0
        for camada_nome, nos in camadas.items():
            x = 0
            for no in nos:
                pos[no] = (x, y)
                x += 3
            y -= 3

        plt.figure(figsize=(14, 10))
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=[cor_no(no) for no in G.nodes()],
            node_size=2500,
            font_size=10,
            arrows=True,
            linewidths=1,
            edge_color="black"
        )
        labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=9)
        plt.title("Grafo de Conhecimento (Organizado por Camadas)", fontsize=14)
        plt.tight_layout()
        plt.show()

    # Exercícios que trabalham determinado músculo
    def exercicios_para_musculo(self, musculo):
        musculo = musculo.lower()
        resultados = []
        for head, relacao, tail in self.listar_relacionamentos():
            if tail.lower() == musculo and relacao in ["trabalha", "ativa"]:
                resultados = resultados + [f"{head} → {relacao} → {tail}"]
        if not resultados:
            return ["Nenhum exercício encontrado para este músculo."]
        return resultados

    # Grafo filtrado por músculo
    def mostrar_grafo_musculo(self, musculo):
        G1 = nx.DiGraph()
        for head, relacao, tail in self.listar_relacionamentos():
            if tail.lower() == musculo.lower() and relacao in ["trabalha", "ativa"]:
                G1.add_edge(head, tail, label=relacao)
        pos = nx.spring_layout(G1, seed=42)
        labels = nx.get_edge_attributes(G1, 'label')
        plt.figure(figsize=(10, 8))
        nx.draw(G1, pos, with_labels=True, node_size=2000, font_size=12, node_color='lightgreen')
        nx.draw_networkx_edge_labels(G1, pos, edge_labels=labels, font_size=10)
        plt.title(f"Grafo filtrado – Músculo: {musculo}")
        plt.show()


# ================================================
# Integração do DataFrame com o Grafo
# ================================================
kg = GrafoDeConhecimento()
for _, row in base.iterrows():
    kg.adicionar_relacionamento(
        head=row['head'],
        relation=row['relacao'],
        tail=row['tail'],
        atualizar_base=False
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
        print("10- Consultar grafo por músculo e visualização")
        print("11 -Encerrar")

    def inicio(self):
        self.menu=Menu()
        while True:
            self.menu.mostrar_opcoes()

            opcao=int(input("Digite a ação que deseja para o grafo: "))
            if opcao== 1:
                no= input("Digite o nó que deseja adicionar: ")
                self.grafo.adicionar_no(no)

            elif opcao== 2:
                no=input("Digite o nó que deseja remover: ")
                self.grafo.remover_no(no)
                
            elif opcao==3:
                head=input("Adicione o Head: ")
                relation=input("Adicione a relação: ")
                tail=input("Adicione o final: ")
                self.grafo.adicionar_relacionamento(head,relation,tail)

            elif opcao ==4:
                head=input("Digite o Head que deseja remover: ")
                relation=input("Digite a relação que deseja remover: ")
                tail=input("Digite o destino que deseja remover: ")
                self.grafo.remover_relacionamento(head,relation,tail)

            elif opcao==5:
                no=input("Qual o nó que deseja consultar? ")
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
                musculo = input("Digite o músculo desejado: ")

                resultados = self.grafo.exercicios_para_musculo(musculo)

                print("\nExercícios que trabalham ou ativam esse músculo:")
                for r in resultados:
                    print(r)

                print("\nGerando grafo...")
                self.grafo.mostrar_grafo_musculo(musculo)

            elif opcao==11:
                print("Encerrando...")
                break

            else:
                print("Opção inválida, tente novamente!")

if __name__ == "__main__":
    menu=Menu()
    menu.inicio()