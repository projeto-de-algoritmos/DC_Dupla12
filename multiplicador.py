import numpy as np
import tkinter as tk
import tkinter.messagebox as tkmsg
from tkinter import ttk, messagebox


def strassen_multiply(A, B):
    n = A.shape[0]
    
    if n == 1:
        return A * B
    
    mid = n // 2
    A11 = A[:mid, :mid]
    A12 = A[:mid, mid:]
    A21 = A[mid:, :mid]
    A22 = A[mid:, mid:]
    B11 = B[:mid, :mid]
    B12 = B[:mid, mid:]
    B21 = B[mid:, :mid]
    B22 = B[mid:, mid:]
    
    P1 = strassen_multiply(A11 + A22, B11 + B22)
    P2 = strassen_multiply(A21 + A22, B11)
    P3 = strassen_multiply(A11, B12 - B22)
    P4 = strassen_multiply(A22, B21 - B11)
    P5 = strassen_multiply(A11 + A12, B22)
    P6 = strassen_multiply(A21 - A11, B11 + B12)
    P7 = strassen_multiply(A12 - A22, B21 + B22)
    
    C11 = P1 + P4 - P5 + P7
    C12 = P3 + P5
    C21 = P2 + P4
    C22 = P1 - P2 + P3 + P6
    
    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
    
    return C

def is_power_of_two(n):
    return (n & (n - 1) == 0) and n != 0

def validate_size():
    m = m_entry.get()
    n = m_entry.get()
    p = m_entry.get()

    if not m.isdigit() or not n.isdigit() or not p.isdigit():
        tkmsg.showerror("Error", "Os tamanhos das matrizes devem ser números inteiros.")
        return False

    m = int(m)
    n = int(n)
    p = int(p)

    if not is_power_of_two(m) or not is_power_of_two(n) or not is_power_of_two(p):
        tkmsg.showerror("Error", "Os tamanhos das matrizes devem ser potências de 2.")
        return False

    return True


def validate_entries():
    m = int(m_entry.get())
    n = int(m_entry.get())
    p = int(m_entry.get())

    for i in range(m):
        for j in range(n):
            if not matrix_A_entries[i][j].get().isdigit():
                messagebox.showerror("Erro", "Todos os campos da Matriz A devem conter apenas números inteiros!")
                return False

    for i in range(n):
        for j in range(p):
            if not matrix_B_entries[i][j].get().isdigit():
                messagebox.showerror("Erro", "Todos os campos da Matriz B devem conter apenas números inteiros!")
                return False

    return True


def multiply_matrices():
    if not validate_entries():
        return

    m = int(m_entry.get())
    n = int(m_entry.get())
    p = int(m_entry.get())

    matrix_A = np.zeros((m, n))
    matrix_B = np.zeros((n, p))

    for i in range(m):
        for j in range(n):
            matrix_A[i, j] = int(matrix_A_entries[i][j].get())

    for i in range(n):
        for j in range(p):
            matrix_B[i, j] = int(matrix_B_entries[i][j].get())

    result_matrix = strassen_multiply(matrix_A, matrix_B)

    
    frame_result = ttk.Frame(root)
    frame_result.grid(row=2, column=2, sticky="nsew")

    result_entries = create_matrix_entries(frame_result, m, p)

    for i in range(m):
        for j in range(p):
            result_entries[i][j].insert(0, str(result_matrix[i, j]))



def create_matrix_entries(root, rows, columns):
    frame = ttk.Frame(root)
    frame.grid(row=2, column=0, sticky="nsew")

    canvas = tk.Canvas(frame)
    canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar_x = ttk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar_y.grid(row=0, column=1, sticky="ns")

    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    entry_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=entry_frame, anchor="nw")

    entries = []
    for i in range(rows):
        row_entries = []
        for j in range(columns):
            entry = ttk.Entry(entry_frame, width=5)
            entry.grid(row=i, column=j, padx=3, pady=3)
            row_entries.append(entry)
        entries.append(row_entries)

    entry_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    return entries

def create_matrices():
    if not validate_size():
        return

    m = int(m_entry.get())
    n = int(m_entry.get())
    p = int(m_entry.get())
    
    global matrix_A_entries, matrix_B_entries

    frame_A = ttk.Frame(root)
    frame_A.grid(row=2, column=0, sticky="nsew")

    frame_B = ttk.Frame(root)
    frame_B.grid(row=2, column=1, sticky="nsew")

    matrix_A_entries = create_matrix_entries(frame_A, m, n)
    matrix_B_entries = create_matrix_entries(frame_B, n, p)
    
    create_button.config(state="disabled")
    multiply_button.config(state="normal")

root = tk.Tk()
root.title("Multiplicação de Matrizes")

size_frame = tk.Frame(root)
size_frame.grid(row=0, column=0, sticky="w", padx=5, pady=5)

m_label = tk.Label(size_frame, text="Tamanho da matriz(tem que ser potencia de 2):")
m_label.grid(row=0, column=0)
m_entry = tk.Entry(size_frame, width=5)
m_entry.grid(row=0, column=1, padx=(0, 20))

button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, sticky="w", padx=5, pady=5)

create_button = tk.Button(button_frame, text="Criar Matrizes", command=lambda: create_matrices())
create_button.grid(row=0, column=0)

multiply_button = tk.Button(button_frame, text="Multiplicar", command=multiply_matrices)
multiply_button.grid(row=0, column=1, padx=(20, 0))

root.mainloop()

