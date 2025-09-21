def cargar_gramatica(nombre_archivo):
    print("\nGramática cargada:")
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        for linea in f:
            print(" ", linea.strip())

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def reconocer(self, esperado):
        if self.actual() == esperado:
            self.pos += 1
            return True
        return False

    def parseE(self):
        nodo = ["E"]
        nodoT = self.parseT()
        if nodoT is None:
            return None
        nodo.append(nodoT)

        while self.reconocer("+"):
            nodoMas = ["+"]
            nodoT2 = self.parseT()
            if nodoT2 is None:
                return None
            nodoMas.append(nodoT2)
            nodo.append(nodoMas)
        return nodo

    def parseT(self):
        nodo = ["T"]
        nodoF = self.parseF()
        if nodoF is None:
            return None
        nodo.append(nodoF)

        while self.reconocer("*"):
            nodoMul = ["*"]
            nodoF2 = self.parseF()
            if nodoF2 is None:
                return None
            nodoMul.append(nodoF2)
            nodo.append(nodoMul)
        return nodo

    def parseF(self):
        nodo = ["F"]
        if self.reconocer("("):
            nodoE = self.parseE()
            if nodoE is None or not self.reconocer(")"):
                return None
            nodo.append(["(", nodoE, ")"])
            return nodo
        elif self.actual() and self.actual().isdigit():
            nodo.append(self.actual())
            self.pos += 1
            return nodo
        return None


def imprimir_arbol(arbol, prefijo="", es_ultimo=True):
    if isinstance(arbol, str):
        rama = "└" if es_ultimo else "├─ "
        print(prefijo + rama + arbol)
    elif isinstance(arbol, list):
        etiqueta = arbol[0]
        hijos = arbol[1:]
        rama = "└─ " if es_ultimo else "├─ "
        print(prefijo + rama + etiqueta)
        for i, hijo in enumerate(hijos):
            ultimo = (i == len(hijos) - 1)
            nuevo_prefijo = prefijo + ("   " if es_ultimo else "│  ")
            imprimir_arbol(hijo, nuevo_prefijo, ultimo)


def main():
    cargar_gramatica("gra.txt")  

    while True:
        print("\nLa operación debe ir con espacios, ej: ( 2 + 3 ) * 4")
        cadena = input("Ingresa una cadena  (o 'salir'): ")
        if cadena.lower() == "salir":
            break

        tokens = cadena.replace("(", "( ").replace(")", " )").split()
        parser = Parser(tokens)
        arbol = parser.parseE()

        if arbol and parser.pos == len(tokens):
            print("Cadena aceptada")
            imprimir_arbol(arbol)
        else:
            print("Cadena no aceptada")


if __name__ == "__main__":
    main()

