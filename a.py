import numpy as np
import tkinter as tk

def strassen_multiply(A, B):
    n = A.shape[0]
    
    # Caso base: Matrizes 1x1
    if n == 1:
        return A * B
    
    # Divide as matrizes em submatrizes
    mid = n // 2
    A11 = A[:mid, :mid]
    A12 = A[:mid, mid:]
    A21 = A[mid:, :mid]
    A22 = A[mid:, mid:]
    B11 = B[:mid, :mid]
    B12 = B[:mid, mid:]
    B21 = B[mid:, :mid]
    B22 = B[mid:, mid:]
    
    # Calcula as sete multiplicações de Strassen
    P1 = strassen_multiply(A11 + A22, B11 + B22)
    P2 = strassen_multiply(A21 + A22, B11)
    P3 = strassen_multiply(A11, B12 - B22)
    P4 = strassen_multiply(A22, B21 - B11)
    P5 = strassen_multiply(A11 + A12, B22)
    P6 = strassen_multiply(A21 - A11, B11 + B12)
    P7 = strassen_multiply(A12 - A22, B21 + B22)
    
    # Calcula as submatrizes resultantes
    C11 = P1 + P4 - P5 + P7
    C12 = P3 + P5
    C21 = P2 + P4
    C22 = P1 - P2 + P3 + P6
    
    # Concatena as submatrizes para formar a matriz resultante
    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
    
    return C

def multiply_matrices():
    m = int(m_entry.get())
    n = int(n_entry.get())
    p = int(p_entry.get())

    matrix_A = np.zeros((m, n))
    matrix_B = np.zeros((n, p))
    
    for i in range(m):
        for j in range(n):
            matrix_A[i, j] = int(matrix_A_entries[i][j].get())
    
    for i in range(n):
        for j in range(p):
            matrix_B[i, j] = int(matrix_B_entries[i][j].get())

    result_matrix = strassen_multiply(matrix_A, matrix_B)

    result_entries = create_matrix_entries(root, m, p, row=2+len(matrix_A_entries), column=0)
    
    for i in range(m):
        for j in range(p):
            result_entries[i][j].insert(0, str(result_matrix[i, j]))

def create_matrix_entries(root, rows, columns, row, column):
    entries = []
    for i in range(rows):
        row_entries = []
        for j in range(columns):
            entry = tk.Entry(root, width=5)
            entry.grid(row=row+i, column=column+j, padx=3, pady=3)
            row_entries.append(entry)
        entries.append(row_entries)
    return entries

root = tk.Tk()

# Entradas para o tamanho das matrizes
m_label = tk.Label(root, text="m:")
m_label.grid(row=0, column=0)
m_entry = tk.Entry(root, width=5)
m_entry.grid(row=0, column=1)

n_label = tk.Label(root, text="n:")
n_label.grid(row=0, column=2)
n_entry = tk.Entry(root, width=5)
n_entry.grid(row=0, column=3)

p_label = tk.Label(root, text="p:")
p_label.grid(row=0, column=4)
p_entry = tk.Entry(root, width=5)
p_entry.grid(row=0, column=5)

# Botão para criar as matrizes e multiplicar
create_button = tk.Button(root, text="Criar Matrizes", command=lambda: create_matrices())
create_button.grid(row=1, column=2)

multiply_button = tk.Button(root, text="Multiplicar", command=multiply_matrices)
multiply_button.grid(row=1, column=3)

def create_matrices():
    m = int(m_entry.get())
    n = int(n_entry.get())
    p = int(p_entry.get())
    
    global matrix_A_entries, matrix_B_entries
    matrix_A_entries = create_matrix_entries(root, m, n, row=2, column=0)
    matrix_B_entries = create_matrix_entries(root, n, p, row=2, column=n+2)
    
    create_button.config(state="disabled")
    multiply_button.config(state="normal")

root.mainloop()
