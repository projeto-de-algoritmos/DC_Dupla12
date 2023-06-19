import numpy as np
from tkinter import *
from tkinter import simpledialog, messagebox

def dividir(matriz):
    linha, coluna = matriz.shape
    linha2, coluna2 = linha//2, coluna//2
    return matriz[:linha2, :coluna2], matriz[:linha2, coluna2:], matriz[linha2:, :coluna2], matriz[linha2:, coluna2:]

def adicionar(matriz1, matriz2):
    return np.add(matriz1, matriz2)

def subtrair(matriz1, matriz2):
    return np.subtract(matriz1, matriz2)

def strassen(matriz1, matriz2):
    if len(matriz1) == 1:
        return matriz1 * matriz2

    a, b, c, d = dividir(matriz1)
    e, f, g, h = dividir(matriz2)

    p1 = strassen(a, subtrair(f, h))
    p2 = strassen(adicionar(a, b), h)
    p3 = strassen(adicionar(c, d), e)
    p4 = strassen(d, subtrair(g, e))
    p5 = strassen(adicionar(a, d), adicionar(e, h))
    p6 = strassen(subtrair(b, d), adicionar(g, h))
    p7 = strassen(subtrair(a, c), adicionar(e, f))

    c11 = adicionar(subtrair(adicionar(p5, p4), p2), p6)
    c12 = adicionar(p1, p2)
    c21 = adicionar(p3, p4)
    c22 = subtrair(subtrair(adicionar(p1, p5), p3), p7)

    c = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))

    return c

def obter_entrada_matriz(titulo):
    root = Tk()
    root.withdraw()
    while True:
        linhas = simpledialog.askstring(titulo, "Digite o número de linhas (deve ser uma potência de 2)")
        if linhas is None:
            root.destroy()
            return None

        try:
            linhas = int(linhas)
            if not (linhas & (linhas-1) == 0) and linhas != 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "O número de linhas deve ser uma potência de 2")
            continue

        matriz = []
        for i in range(linhas):
            while True:
                linha = simpledialog.askstring(titulo, f"Digite os valores da linha {i+1} separados por vírgulas")
                if linha is None:
                    root.destroy()
                    return None

                try:
                    linha = list(map(int, linha.split(",")))
                    if len(linha) != linhas:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Erro", "Valores de linha inválidos")
                    continue

                matriz.append(linha)
                break

        root.destroy()
        return np.array(matriz)

def multiplicar_matrizes():
    matriz1 = obter_entrada_matriz("Matriz 1")
    if matriz1 is None:
        return

    matriz2 = obter_entrada_matriz("Matriz 2")
    if matriz2 is None:
        return

    if matriz1.shape != matriz2.shape:
        messagebox.showerror("Erro", "As duas matrizes devem ter o mesmo formato")
        return

    resultado = strassen(matriz1, matriz2)
    messagebox.showinfo("Resultado", str(resultado))

root = Tk()
root.title("Calculadora de Matrizes")
root.geometry('300x100')

Label(root, text="Calculadora de Matrizes utilizando o método de Strassen").pack()

botao_multiplicar = Button(root, text="Multiplicar matrizes", command=multiplicar_matrizes)
botao_multiplicar.pack()

root.mainloop()
