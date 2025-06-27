import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="evaluaciondocente"
)
cursor = conexion.cursor()

cursor.execute("SELECT * FROM pizza")
filas = cursor.fetchall()

for fila in filas:
    print(fila)

def mostrar_menu():
    print("\n--- BIENVENIDO A TU PIZZERIA FAVORITA ---")
    print("1. Pedir una pizza")
    print("2. Mostrar tablas")
    print("3. Modificar datos")
    print("4. Eliminar datos")
    print("5. Consultas")
    print("6. Salir")

def mostrar_tabla():
    print()

    columnas = [desc[0] for desc in cursor.description]
    filas = cursor.fetchall()

    anchos = [len(col) for col in columnas]
    for fila in filas:
        for i, valor in enumerate(fila):
            anchos[i] = max(anchos[i], len(str(valor)))

    formato = " | ".join("{:<" + str(ancho) + "}" for ancho in anchos)
    separador = "-" * (sum(anchos) + 3 * (len(anchos) - 1))

    print(separador)
    print(formato.format(*columnas))
    print(separador)

    for fila in filas:
        print(formato.format(*[str(v) for v in fila]))
    print (separador)
    print()

def validar_id_existente(tabla, columna_id):
    cursor.execute(f"SELECT {columna_id} FROM {tabla}")
    ids_validos = [str(row[0]) for row in cursor.fetchall()]
    while True:
        entrada = input(f"Ingrese un ID válido de {tabla}: ")
        if entrada in ids_validos:
            return entrada
        print(f"ID inválido. Debe ser uno de estos: {', '.join(ids_validos)}")

def obtener_siguiente_id_pedidos():
    try:
        cursor.execute("SELECT MAX(id_pedidos) FROM pedido")
        resultado = cursor.fetchone()
        if resultado is None or resultado[0] is None:
            return 1
        return resultado[0] + 1
    except Exception as e:
        print("Error obteniendo el id del pedido:", e)
        return 1


###################### Funciones de menu ######################

# Función para pedir una pizza (Opción 1)
def opcion_pedir_pizza():
    def pedir_pizza():
        cursor.execute("SELECT * FROM pizza")
        mostrar_tabla()
        id_pizza = validar_id_existente("pizza", "id_pizza")

        cantidad = input("¿Cuántas pizzas deseas pedir?: ")
        while not cantidad.isdigit() or int(cantidad) <= 0:
            cantidad = input("Ingresa una cantidad válida mayor que 0: ")

        ingredientes = []
        while input("¿Agregar ingredientes adicionales? (si/no): ").lower() == "si":
            cursor.execute("SELECT * FROM ingredientes")
            mostrar_tabla()
            ingredientes.append(validar_id_existente("ingredientes", "id_ingrediente"))

        return {"id_pizza": id_pizza, "cantidad": cantidad, "ingredientes_adicionales": ingredientes}

    def pedir_cliente():
        print("\n--- INGRESO DE DATOS DEL CLIENTE ---")
        cedula = input("Ingresa cédula del cliente: ")
        cursor.execute("SELECT * FROM cliente WHERE id_cliente = %s", (cedula,))
        cliente = cursor.fetchone()
        if cliente:
            print(f"Cliente con cédula {cedula} ya esta registrado. Usando datos existentes.")
            return {
                "Cedula": cliente[0], "Nombre": cliente[1], "Email": cliente[2],
                "Telefono": cliente[3], "Direccion": cliente[4]
            }

        nombre = input("Nombre: ")
        email = input("Email: ")
        telefono = input("Teléfono: ")
        direccion = input("Dirección: ")
        cursor.execute("INSERT INTO cliente VALUES (%s, %s, %s, %s, %s)",
                       (cedula, nombre, email, telefono, direccion))
        conexion.commit()
        return {"Cedula": cedula, "Nombre": nombre, "Email": email, "Telefono": telefono, "Direccion": direccion}

    def seleccionar_pago():
        cursor.execute("SELECT * FROM metodo_pago")
        mostrar_tabla()
        return validar_id_existente("metodo_pago", "id_metodo")

    def calcular_total(pedidos):
        total = 0
        for p in pedidos:
            cursor.execute("SELECT precio_base FROM pizza WHERE id_pizza = %s", (p["id_pizza"],))
            total += cursor.fetchone()[0] * int(p["cantidad"])
            for ing in p["ingredientes_adicionales"]:
                cursor.execute("SELECT precio FROM ingredientes WHERE id_ingrediente = %s", (ing,))
                total += cursor.fetchone()[0]
        return total

    def guardar_pedido(id_pedido, cliente, metodo_pago, pedidos):
        total = calcular_total(pedidos)
        cursor.execute("INSERT INTO pedido (id_pedidos, fecha_hora, total, id_cliente, id_metodo) VALUES (%s, CURDATE(), %s, %s, %s)",
                       (id_pedido, total, cliente["Cedula"], metodo_pago))

        for p in pedidos:
            cursor.execute("SELECT precio_base FROM pizza WHERE id_pizza = %s", (p["id_pizza"],))
            base = cursor.fetchone()[0]
            subtotal = base * int(p["cantidad"])
            cursor.execute("INSERT INTO detalle_pedido (cantidad, subtotal, id_pedido, id_pizza) VALUES (%s, %s, %s, %s)",
                           (p["cantidad"], subtotal, id_pedido, p["id_pizza"]))
            id_detalle = cursor.lastrowid
            if p["ingredientes_adicionales"]:
                for ing in p["ingredientes_adicionales"]:
                    cursor.execute("INSERT INTO ingrediente_adicional (id_detalle, id_ingrediente) VALUES (%s, %s)", (id_detalle, ing))
            else:
                cursor.execute("INSERT INTO ingrediente_adicional (id_detalle, id_ingrediente) VALUES (%s, NULL)", (id_detalle,))
        conexion.commit()

    def mostrar_resumen(cliente, pedidos, metodo_pago, id_pedido):
        print(f"\n--- RESUMEN PEDIDO #{id_pedido} ---")
        print(f"Cliente: {cliente['Nombre']} | Cédula: {cliente['Cedula']}")
        print(f"Email: {cliente['Email']} | Tel: {cliente['Telefono']} | Dirección: {cliente['Direccion']}")
        print(f"Método de pago ID: {metodo_pago}")

        for i, p in enumerate(pedidos, 1):
            cursor.execute("SELECT nombre, precio_base FROM pizza WHERE id_pizza = %s", (p["id_pizza"],))
            nombre, precio = cursor.fetchone()
            print(f"\nPizza #{i}: {nombre} | Cantidad: {p['cantidad']} | Precio base: ${precio}")
            if p["ingredientes_adicionales"]:
                print("Ingredientes adicionales:")
                for ing in p["ingredientes_adicionales"]:
                    cursor.execute("SELECT nombre, precio FROM ingredientes WHERE id_ingrediente = %s", (ing,))
                    nom, prec = cursor.fetchone()
                    print(f"- {nom} (${prec})")
            else:
                print("Ingredientes adicionales: Ninguno")
        print(f"\nTotal: ${calcular_total(pedidos)}\n--- FIN DEL PEDIDO ---")

    # ----- FLUJO PRINCIPAL DE LA OPCIÓN 1 -----
    pedidos = []
    while True:
        pedidos.append(pedir_pizza())
        if input("¿Agregar otra pizza? (si/no): ").lower() != "si":
            break

    cliente = pedir_cliente()
    metodo_pago = seleccionar_pago()
    if metodo_pago is None:
        print("Método de pago no válido. Cancelando...")
        return

    id_pedido = obtener_siguiente_id_pedidos()
    mostrar_resumen(cliente, pedidos, metodo_pago, id_pedido)

    if input("¿Deseas confirmar el pedido? (si/no): ").lower() == "si":
        guardar_pedido(id_pedido, cliente, metodo_pago, pedidos)
        print("Pedido guardado correctamente. Gracias por tu compra!")
    else:
        print("Pedido cancelado.")

# Función para mostrar las tablas disponibles (Opción 2)
def tablas():
    def mostrar_tablas():
        print("\n--- TABLAS DISPONIBLES ---")
        print("1. Clientes")
        print("2. Detalle Pedido")
        print("3. Ingrediente Adicional")
        print("4. Ingredientes")
        print("5. Métodos de pago")
        print("6. Pedido")
        print("7. Pizzas")
        print("8. Regresar al menú principal")

    while True:
        mostrar_tablas()
        opcion2 = input("¿Qué tabla deseas ver?: ")
        if opcion2 == "1":
            cursor.execute("SELECT * FROM cliente")
            mostrar_tabla()
        elif opcion2 == "2":
            cursor.execute("SELECT * FROM detalle_pedido")
            mostrar_tabla()
        elif opcion2 == "3":
            cursor.execute("SELECT * FROM ingrediente_adicional")
            mostrar_tabla()
        elif opcion2 == "4":
            cursor.execute("SELECT * FROM ingredientes")
            mostrar_tabla()
        elif opcion2 == "5":
            cursor.execute("SELECT * FROM metodo_pago")
            mostrar_tabla()
        elif opcion2 == "6":
            cursor.execute("SELECT * FROM pedido")
            mostrar_tabla()
        elif opcion2 == "7":
            cursor.execute("SELECT * FROM pizza")
            mostrar_tabla()
        elif opcion2 == "8":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")
            
def ModificarDatos():
    def mostrar_tablas_modificar():
        print("\n--- OPCIONES MODIFICAR ---")
        print("1. Clientes")
        print("2. Pedido")
        print("3. Ingrediente Adicional")
        print("4. Métodos de pago")
        print("5. Pizzas")
        print("6. Regresar al menú principal")

    def modificar_tabla(tabla, id_columna):
        cursor.execute(f"SELECT * FROM {tabla}")
        mostrar_tabla()
        
        id_valido = validar_id_existente(tabla, id_columna)
        cursor.execute(f"SHOW COLUMNS FROM {tabla}")
        columnas = [col[0] for col in cursor.fetchall() if col[0] != id_columna]

        print(f"\nCampos disponibles para modificar en '{tabla}':")
        for i, col in enumerate(columnas, 1):
            print(f"{i}. {col}")
        
        opcion = input("Selecciona el número del campo que deseas modificar: ")
        if not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(columnas):
            print("Opción inválida.")
            return

        campo_a_modificar = columnas[int(opcion) - 1]
        nuevo_valor = input(f"Nuevo valor para '{campo_a_modificar}': ")

        try:
            sql = f"UPDATE {tabla} SET {campo_a_modificar} = %s WHERE {id_columna} = %s"
            cursor.execute(sql, (nuevo_valor, id_valido))
            conexion.commit()
            print("Registro actualizado exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error al actualizar: {err}")
            conexion.rollback()

    while True:
        mostrar_tablas_modificar()
        opcion = input("Selecciona una tabla (1-6): ")

        if opcion == "1":
            modificar_tabla("cliente", "id_cliente")
        elif opcion == "2":
            modificar_tabla("pedido", "id_pedidos")
        elif opcion == "3":
            modificar_tabla("ingrediente_adicional", "id_detalle")  # o usar un campo compuesto si fuera necesario
        elif opcion == "4":
            modificar_tabla("metodo_pago", "id_metodo")
        elif opcion == "5":
            modificar_tabla("pizza", "id_pizza")
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")
# Función para eliminar datos (Opción 4)
def EliminarDatos():
    def mostrar_tablas_Eliminar():
        print("\n--- OPCIONES ELIMINAR ---")
        print("1. Clientes")
        print("2. Pedido")
        print("3. Ingrediente Adicional")
        print("4. Métodos de pago")
        print("5. Pizzas")
        print("6. Regresar al menú principal")
    
    def eliminar_registro(tabla, id_columna):
        cursor.execute(f"SELECT * FROM {tabla}")
        mostrar_tabla()

        id_valido = validar_id_existente(tabla, id_columna)
        confirmar = input(f"¿Estás seguro de eliminar el registro con {id_columna} = {id_valido}? (si/no): ")
        if confirmar.lower() != "si":
            print("Eliminación cancelada.")
            return

        try:
            cursor.execute(f"DELETE FROM {tabla} WHERE {id_columna} = %s", (id_valido,))
            conexion.commit()
            print("Registro eliminado exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error al eliminar: {err}")
            conexion.rollback()

    while True:
        mostrar_tablas_Eliminar()
        opcion = input("Selecciona una tabla (1-6): ")

        if opcion == "1":
            eliminar_registro("cliente", "id_cliente")
        elif opcion == "2":
            eliminar_registro("pedido", "id_pedidos")
        elif opcion == "3":
            eliminar_registro("ingrediente_adicional", "id_detalle")  # depende de la clave primaria real
        elif opcion == "4":
            eliminar_registro("metodo_pago", "id_metodo")
        elif opcion == "5":
            eliminar_registro("pizza", "id_pizza")
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")


    def mostrar_menu_consultas():
        print("\n--- CONSULTAS DISPONIBLES ---")
        print("1. Ver una tabla completa")
        print("2. Top 3 clientes con más pedidos")
        print("3. Pedidos ordenados por demanda (descendente)")
        print("4. Listado de pedidos realizados en enero y mayo")
        print("5. Total de ingredientes adicionales más solicitados")  # Consulta adicional propuesta
        print("6. Regresar al menú principal")

    def consulta_tabla_completa():
        tablas = {
            "1": "cliente",
            "2": "pedido",
            "3": "detalle_pedido",
            "4": "ingredientes",
            "5": "ingrediente_adicional",
            "6": "metodo_pago",
            "7": "pizza"
        }
        print("\n--- TABLAS DISPONIBLES ---")
        for k, v in tablas.items():
            print(f"{k}. {v}")
        opcion = input("Selecciona la tabla a consultar: ")

        if opcion in tablas:
            try:
                cursor.execute(f"SELECT * FROM {tablas[opcion]}")
                mostrar_tabla()
            except mysql.connector.Error as e:
                print(f"Error: {e}")
        else:
            print("Opción inválida.")

    def top_3_clientes_con_mas_pedidos():
        print("\n--- TOP 3 CLIENTES CON MÁS PEDIDOS ---")
        cursor.execute("""
            SELECT c.nombre, COUNT(p.id_pedidos) AS total_pedidos
            FROM cliente c
            JOIN pedido p ON c.id_cliente = p.id_cliente
            GROUP BY c.id_cliente
            ORDER BY total_pedidos DESC
            LIMIT 3
        """)
        mostrar_tabla()

    def pedidos_ordenados_por_demanda():
        print("\n--- PEDIDOS ORDENADOS POR DEMANDA ---")
        cursor.execute("""
            SELECT pi.nombre AS pizza, SUM(dp.cantidad) AS total_vendidos
            FROM detalle_pedido dp
            JOIN pizza pi ON dp.id_pizza = pi.id_pizza
            GROUP BY dp.id_pizza
            ORDER BY total_vendidos DESC
        """)
        mostrar_tabla()

    def pedidos_en_enero_y_mayo():
        print("\n--- PEDIDOS EN ENERO Y MAYO ---")
        cursor.execute("""
            SELECT * FROM pedido
            WHERE MONTH(fecha_hora) IN (1, 5)
        """)
        mostrar_tabla()

    def ingredientes_mas_solicitados():
        print("\n--- INGREDIENTES ADICIONALES MÁS SOLICITADOS ---")
        cursor.execute("""
            SELECT i.nombre, COUNT(ia.id_ingrediente) AS veces_usado
            FROM ingrediente_adicional ia
            JOIN ingredientes i ON ia.id_ingrediente = i.id_ingrediente
            GROUP BY ia.id_ingrediente
            ORDER BY veces_usado DESC
            LIMIT 5
        """)
        mostrar_tabla()

    while True:
        mostrar_menu_consultas()
        opcion = input("Selecciona una consulta (1-6): ")

        if opcion == "1":
            consulta_tabla_completa()
        elif opcion == "2":
            top_3_clientes_con_mas_pedidos()
        elif opcion == "3":
            pedidos_ordenados_por_demanda()
        elif opcion == "4":
            pedidos_en_enero_y_mayo()
        elif opcion == "5":
            ingredientes_mas_solicitados()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")
# Función para consultas (Opción 5)
def Consultas():
    def mostrar_menu_consultas():
        print("\n--- CONSULTAS DISPONIBLES ---")
        print("1. Top 3 clientes con más pedidos")
        print("2. Pedidos ordenados por demanda (descendente)")
        print("3. Listado de pedidos realizados en enero y mayo")
        print("4. Total de ingredientes adicionales más solicitados")
        print("5. Regresar al menú principal")

    def top_3_clientes_con_mas_pedidos():
        print("\n--- TOP 3 CLIENTES CON MÁS PEDIDOS ---")
        cursor.execute("""
            SELECT c.nombre, COUNT(p.id_pedidos) AS total_pedidos
            FROM cliente c
            JOIN pedido p ON c.id_cliente = p.id_cliente
            GROUP BY c.id_cliente
            ORDER BY total_pedidos DESC
            LIMIT 3
        """)
        mostrar_tabla()

    def pedidos_ordenados_por_demanda():
        print("\n--- PEDIDOS ORDENADOS POR DEMANDA ---")
        cursor.execute("""
            SELECT pi.nombre AS pizza, SUM(dp.cantidad) AS total_vendidos
            FROM detalle_pedido dp
            JOIN pizza pi ON dp.id_pizza = pi.id_pizza
            GROUP BY dp.id_pizza
            ORDER BY total_vendidos DESC
        """)
        mostrar_tabla()

    def pedidos_en_enero_y_mayo():
        print("\n--- PEDIDOS EN ENERO Y MAYO ---")
        cursor.execute("""
            SELECT * FROM pedido
            WHERE MONTH(fecha_hora) IN (1, 5)
        """)
        mostrar_tabla()

    def ingredientes_mas_solicitados():
        print("\n--- INGREDIENTES ADICIONALES MÁS SOLICITADOS ---")
        cursor.execute("""
            SELECT i.nombre, COUNT(ia.id_ingrediente) AS veces_usado
            FROM ingrediente_adicional ia
            JOIN ingredientes i ON ia.id_ingrediente = i.id_ingrediente
            GROUP BY ia.id_ingrediente
            ORDER BY veces_usado DESC
            LIMIT 5
        """)
        mostrar_tabla()

    while True:
        mostrar_menu_consultas()
        opcion = input("Selecciona una consulta (1-5): ")

        if opcion == "1":
            top_3_clientes_con_mas_pedidos()
        elif opcion == "2":
            pedidos_ordenados_por_demanda()
        elif opcion == "3":
            pedidos_en_enero_y_mayo()
        elif opcion == "4":
            ingredientes_mas_solicitados()
        elif opcion == "5":
            break
        else:
            print("❌ Opción inválida.")


# Bucle principal
while True:
    mostrar_menu()
    opcion = input("Elige una opción (1-6): ")
    if opcion == "1":
        opcion_pedir_pizza()
    elif opcion == "2":
        tablas()
    elif opcion == "3":
        ModificarDatos()
    elif opcion == "4":
        EliminarDatos()
    elif opcion == "5":
        Consultas()
    elif opcion == "6":
        print("Gracias por su visita. ¡Hasta pronto!")
        break
    else:
        print("Opción no válida. Intenta de nuevo.")

# Cierre de conexión
cursor.close()
conexion.close()
