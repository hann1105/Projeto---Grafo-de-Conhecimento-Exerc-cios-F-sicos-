import pandas as pd #Para a utilização e manipulação de tabelas (DataFrame para a Base de conhecimento)
import networkx as nx
import matplotlib.pyplot as plt

# Base de conhecimento - Data Frame  Aluno, Objetivo, Exercício, Grupo Muscular, Máquina
base = pd.DataFrame({ # cria um DataFrame com colunas head, relacao, tail representando triplas (head, relação, tail)
    'head': [ #Nós iniciais da relação
        #Alunos -> Objetivo
        'Paola', 'Lucas',
        #Alunos -> tipo de treino
        'Paola', 'Lucas',
        #Exercícios -> Músculos trabalhados (Músculo primário)
        'Agachamento', 'Rosca 21', 'Tríceps Testa', 'Elevação Pélvica', 'Puxada Alta', 'Leg 45°',
        #Exerícios -> Músculos secundários
        'Agachamento', 'Rosca 21', 'Tríceps Testa','Leg 45°','Leg 45°',
        #Exercício -> Máquina
        'Tríceps Testa','Elevação Pélvica','Leg 45°'
    ],
    'relacao': [ #Relação entre os nós 
        #Alunos -> Objetivo
        'tem objetivo', 'tem objetivo',
        #Alunos -> tipo de treino
        'treina', 'treina',
        #Exercícios -> Músculos trabalhados (Músculo primário)
        'trabalha','trabalha','trabalha','trabalha','trabalha','trabalha',
        #Exerícios -> Músculos secundários
        'ativa','ativa','ativa','ativa','ativa',
        #Exercício -> Máquina
        'usa máquina','usa máquina','usa máquina'
    ],
    'tail': [
        #Alunos -> Objetivo
        'Emagrecimento', 'Hipertrofia',
        #Alunos -> tipo de treino
        'Agachamento', 'Rosca 21',
        #Exercícios -> Músculos trabalhados (Músculo primário)
        'Quadríceps','Bíceps','Tríceps','Glúteo','Costas','Quadríceps',
        #Exerícios -> Músculos secundários
        'Glúteo','Antebraço','Ombros','Glúteo','Posterior de coxa',
        #Exercício -> Máquina
        'banco e halteres','Aparelho de elevação','Leg Press'
    ]
})

print("-------------------- Base de Conhecimento ----------------------")
print(base)#Mostra a base inicial

# Classe Grafo de Conhecimento (Métodos Manuais)

class GrafoDeConhecimento:
    def __init__(self):
        self.grafo = {} # inicializa o grafo como um dicionário vazio

    # Adicionar nó 
    def adicionar_no(self, no):
        existe = False #Checar se o nó ja existe
        for chave in self.grafo: #Percorre as chaves do dicionário (grafo)
            if chave == no: #se ja existir um nó com o mesmo nome troca o 'existe' por True
                existe = True
                break
        if not existe:
            self.grafo[no] = [] #cria uma lista de relações do novo nó no grafo
            print("Nó adicionado com sucesso!")
        else:
            print("Nó já existe.")

    # Remover nó 
    def remover_no(self, no):
        novo_grafo = {} #Cria novo_grafo = {} que irá conter o grafo reconstruído sem o nó a remover.
        for chave in self.grafo:#percorre todo o grafo em busca do nó que será removido
            if chave != no: #se não for o nó escolhido, cria as novas relaçoes para o novo grafo
                novas_relacoes = []
                for relacao, destino in self.grafo[chave]: #Em cada aresta (relacao, destino) da lista de adjacência de chave, 
                    if destino != no: #verifica if destino != no: — isso filtra e remove arestas que apontem para o nó removido.
                        novas_relacoes = novas_relacoes + [(relacao, destino)]
                novo_grafo[chave] = novas_relacoes #atribui a lista filtrada ao novo grafo
        self.grafo = novo_grafo #substitui o grafo antigo pelo novo grafo sem o nó e as relações dele
        print("Nó removido com sucesso!")

        # Atualizar a base
        global base
        nova_base = [] #cria nova base para reconstruir a base sem as relações do nó removido
        for i in range(len(base)):
            linha = base.iloc[i].to_dict() #converte a linha para dicionário
            if linha['head'] != no and linha['tail'] != no:#Mantém apenas linhas cujo head e tail não sejam o nó removido
                nova_base = nova_base + [linha]
        base = pd.DataFrame(nova_base) #recria a base de acordo com a lista filtrada

    # Adicionar relacionamento manualmente
    def adicionar_relacionamento(self, head, relation, tail, atualizar_base=True):
        if head not in self.grafo: #verifica se já possui aquele head no grafo
            self.adicionar_no(head) #se não tem, adiciona o nó
        if tail not in self.grafo: 
            self.adicionar_no(tail)

        relacoes_atuais = self.grafo[head] #Recupera a lista atual de relações de head
        relacoes_atuais = relacoes_atuais + [(relation, tail)] #adiciona nova tupla
        self.grafo[head] = relacoes_atuais #e atribuiu novamente ao grafo
        print("Relacionamento adicionado ao grafo!")

        if atualizar_base: #se atualizar_base for True
            global base #atualiza o DataFrame com o relacionamento novo
            nova_linha = {'head': head, 'relacao': relation, 'tail': tail}
            base = pd.concat([base, pd.DataFrame([nova_linha])], ignore_index=True) #concatina a linha a base

    # Remover relacionamento 
    def remover_relacionamento(self, head, relation, tail):
        if head in self.grafo: #Verifica se o head existe
            novas_relacoes = []
            for relacao_atual, destino in self.grafo[head]:#Mantém todas as tuplas que não coincidam com (relation, tail)
                if not (relacao_atual == relation and destino == tail):
                    novas_relacoes = novas_relacoes + [(relacao_atual, destino)]
            self.grafo[head] = novas_relacoes #Reatribui a lista filtrada a self.grafo[head]
            print("Relacionamento removido do grafo!")

            global base #Atualiza o DataFrame sem a relação que foi removida
            nova_base = []
            for i in range(len(base)):
                linha = base.iloc[i].to_dict() #percorre cada linha e mantem apenas as que não coincidam exatamente com (head, relation, tail).
                if not (linha['head'] == head and linha['relacao'] == relation and linha['tail'] == tail):
                    nova_base = nova_base + [linha]
            base = pd.DataFrame(nova_base)
        else:
            print("Relacionamento não encontrado")

    # Consultar relacionamentos de um nó
    def consultar_relacionamentos_de(self, no):
        if no in self.grafo:#se o nó está no grafo
            print(self.grafo[no]) #mostra as relações que pertencem a ele
            return
        else:
            print(f"Nó '{no}' não existe.")
            return []

    # Listar nós
    def listar_nos(self):
        lista = []
        for chave in self.grafo: #percorre cada chave do dicionario (os nós do grafo)
            lista = lista + [chave] #concatena cada chave de nós à lista
        return lista

    # Listar relacionamentos
    def listar_relacionamentos(self):
        triplas = []
        for head in self.grafo: #para cada head
            for relation, tail in self.grafo[head]:#e para cada relação e final na sua lista de adjacencia
                triplas = triplas + [(head, relation, tail)] #concatena à lista triplas e mostra as relações
        return triplas

    # Mostrar grafo completo
    def mostrar_grafo(self):
        G = nx.DiGraph() #cria um grafo direcionado para conseguir desenhar
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

        def cor_no(no):#nomeia cada nó com uma cor especifica para visualização
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

        pos = {} #Agrupa as listas em um dicionário camadas para criar um layout por linhas/camadas
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
        plt.title("Grafo de Conhecimento ", fontsize=14)
        plt.tight_layout()
        plt.show()

    # Exercícios que trabalham determinado músculo
    def exercicios_para_musculo(self, musculo):
        musculo = musculo.lower() #transforma todas as letras em minusculas
        resultados = []
        for head, relacao, tail in self.listar_relacionamentos(): #para cada tripla, compara se a relação é de 'trabalha' ou 'ativa'
            if tail.lower() == musculo and relacao in ["trabalha", "ativa"]:
                resultados = resultados + [f"{head} → {relacao} → {tail}"] #se sim, adiciona na lista resultados
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

# Integração do DataFrame com o Grafo

kg = GrafoDeConhecimento()# instancia um grafo de conhecimento
for _, row in base.iterrows(): #Percorre cada linha do DataFrame base
    kg.adicionar_relacionamento( #adiciona na base
        head=row['head'],
        relation=row['relacao'],
        tail=row['tail'],
        atualizar_base=False #evita concatenar novamente essas linhas na base
    )

#Menu de opções para o usuário

class Menu:
    def __init__(self):
        self.grafo=kg #o menu manipula o grafo que foi criado anteriormente 

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
            if opcao== 1: #Opção para adicionar nó
                no= input("Digite o nó que deseja adicionar: ")
                self.grafo.adicionar_no(no)

            elif opcao== 2: #opção para remover nó
                no=input("Digite o nó que deseja remover: ")
                self.grafo.remover_no(no)
                
            elif opcao==3: #Opção de adicionar relacionamento
                head=input("Adicione o Head: ")
                relation=input("Adicione a relação: ")
                tail=input("Adicione o final: ")
                self.grafo.adicionar_relacionamento(head,relation,tail)

            elif opcao ==4: #opção de remover relacionamento
                head=input("Digite o Head que deseja remover: ")
                relation=input("Digite a relação que deseja remover: ")
                tail=input("Digite o destino que deseja remover: ")
                self.grafo.remover_relacionamento(head,relation,tail)

            elif opcao==5: #opção para consultar os relacionamentos de um determinado nó
                no=input("Qual o nó que deseja consultar? ")
                self.grafo.consultar_relacionamentos_de(no)

            elif opcao==6: #opção de mostrar todos os nós
                print("------NÓS-----")
                for t in self.grafo.listar_nos():
                    print(t)

            elif opcao==7: #opção de mostrar todas os relacionamentos
                print("----- RELAÇÕES-----")
                for t in self.grafo.listar_relacionamentos():
                    print(t)

            elif opcao==8: #opção para mostrar a base de conhecimento
                print(base)

            elif opcao==9: #opção para visualizar o grafo
                self.grafo.mostrar_grafo()

            elif opcao==10: #opção para consultar os exercicios de determinado musculo
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