import speech_recognition as sr
import pyttsx3
import time
import sys
import tkinter as tk
import random
import json
from tkinter import messagebox
from PIL import Image, ImageTk

# CONVERTIR CADENAS DE TEXTO A AUDIO Y REPRODUCIRLAS


def texto_a_audio(comando):
    palabra = pyttsx3.init()
    palabra.say(comando)
    palabra.runAndWait()

# CAPTURA AUDIO DESDE EL MICROFONO Y ANALIZA POSIBLES ERRORES


def capturar_voz(reconocer, microfono, tiempo_ruido=1.0):
    if not isinstance(reconocer, sr.Recognizer):
        raise TypeError("'reconocer' no es de la instacia 'Recognizer'")

    if not isinstance(microfono, sr.Microphone):
        raise TypeError("'reconocer' no es de la instacia 'Recognizer'")

    with microfono as fuente:
        reconocer.adjust_for_ambient_noise(fuente, duration=tiempo_ruido)
        audio = reconocer.listen(fuente)

    respuesta = {
        "suceso": True,
        "error": None,
        "mensaje": None,
    }
    try:
        respuesta["mensaje"] = reconocer.recognize_google(
            audio, language="es-PE")
    except sr.RequestError:
        respuesta["suceso"] = False
        respuesta["error"] = "API no disponible"
    except sr.UnknownValueError:
        respuesta["error"] = "Habla inteligible"
    return respuesta

# CONVIERTE A UNA CADENA DE TEXTO EN MINUSCULA EL AUDIO ENVIADO POR MICROFONO


def enviar_voz():
    while (1):
        palabra = capturar_voz(recognizer, microphone)
        if palabra["mensaje"]:
            break
        if not palabra["suceso"]:
            print("Algo no está bien. No puedo reconocer tu micrófono o no lo tienes enchufado. <",
                  nombre["error"], ">")
            texto_a_audio(
                "Algo no está bien. No puedo reconocer tu micrófono o no lo tienes enchufado.")
            exit(1)
        print("No pude escucharte, ¿podrias repetirlo?\n")
        texto_a_audio("No pude escucharte, ¿podrias repetirlo?")
    return palabra["mensaje"].lower()

# BASE DE DATOS DONDE SE ENCUENTRA TODA LA INFORMACION CONCERNIENTE


with open('basedatos.json', 'r') as archivo:
    datos = json.load(archivo)

# Acceder a la parte especifica que se desea imprimir

# CARGAR IMAGEN


def cargar_imagen(ruta):
    try:
        img = Image.open(ruta)
        # Utiliza Image.BILINEAR como filtro de resampling
        img_resized = img.resize((600, 400), Image.BILINEAR)
        img_resized.show()
    except Exception as e:
        print(f"No se pudo cargar la imagen: {e}")
        sys.exit(1)

# SEGUIR


def seguir():
    print("¿Quieres seguir aprendiendo?")
    texto_a_audio("¿Quieres seguir aprendiendo?")
    time.sleep(0.5)
    print("Responde con:\n1) Está bien\n2) No gracias")

    respuesta = enviar_voz()
    print("Tu respuesta " + respuesta)

    return respuesta


def comprobar_respuesta(respuesta, nombre):
    if respuesta == "está bien":
        print("Elige la opción que desees aprender:")
        texto_a_audio("Elige la opción que desees aprender:")
        print("\n1) Unidad central de proceso CPU\n2) Memoria\n3) Entrada / Salida\n4) Sistemas de interconexión: Buses\n5) Periféricos\n")    
    elif respuesta == "no gracias":
        print("Oh, es una lástima. En ese caso nos veremos en otra ocasión.")
        texto_a_audio(
            "Oh, es una lástima. En ese caso nos veremos en otra ocasión")
        time.sleep(0.5)
        print("Espero que hayas aprendido mucho sobre este tema. Hasta luego.")
        texto_a_audio(
            "Espero que hayas aprendido mucho sobre este tema. Hasta luego.")
        exit(0)
    else:
        print(nombre + " creo que no has respondido con alguna de las instrucciones indicadas anteriormente")
        texto_a_audio(
            nombre + " creo que no has respondido con alguna de las instrucciones indicadas anteriormente")
        print("Responde con:\n1) Está bien.\n2) No gracias")

def escribir_respuesta(pregunta, opciones, respuesta_correcta):
    print(pregunta)
    texto_a_audio(pregunta)
    for i, alternativa in enumerate(opciones, start=1):
        print(f"{i}. {alternativa}")
        texto_a_audio(f"Opción {i}: {alternativa}")

    respuesta_usuario = capturar_voz()
    print("Usuario: " + respuesta_usuario)

    if respuesta_usuario.isdigit():
        opcion_elegida = int(respuesta_usuario)
        if 1 <= opcion_elegida <= len(opciones):
            if opciones[opcion_elegida - 1] == respuesta_correcta:
                print("¡Respuesta correcta!")
                texto_a_audio("Respuesta correcta.")
                print("TU PUNTAJE ES DE 1 PUNTO")
            else:
                print("Respuesta incorrecta.")
                texto_a_audio("Respuesta incorrecta.")
        else:
            print("Opción inválida.")
            texto_a_audio("Opción inválida.")
    else:
        print("Entrada inválida. Por favor, intenta de nuevo.")
        texto_a_audio("Entrada inválida. Por favor, intenta de nuevo.")


# INICIO
if __name__ == "__main__":

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    salir = False

    # USANDO LA FUNCION TEXTO_A_AUDIO SE HACE LEER CADENAS DE TEXTO, COMO SI
    # LA COMPUTADORA TE ESTUVIERA HABLANDO

    texto_a_audio(datos['bienvenida'])
    print("Di tu nombre: ")
    # LA FUNCION 'enviar_voz' RETORNA UNA CADENA DE TEXTO DEL AUDIO ENVIADO
    # POR VOZ DEL USUARIO
    nombre = enviar_voz()
    print("Hola {}. Mucho gusto.".format(nombre))
    texto_a_audio("Hola {}. Mucho gusto.".format(nombre))
    print("{} Ahora voy a explicarte sobre las opciones que tiene este programa. Tienes 3 opciones para escoger.".format(nombre))
    texto_a_audio(
        "{} Ahora voy a explicarte sobre las opciones que tiene este programa. Tienes 3 opciones para escoger.".format(nombre))
    print("\n 1) Aprendizaje\n 2) Tests\n 3) Juegos\n")
    texto_a_audio("Aprendizaje. Tests. Juegos.")
    print("La opción Aprendizaje es donde podrás aprender todo con respecto a la Estructura de un computador. La opción Tests es donde podrás poner en práctica lo que aprendiste mediante exámenes. Y por último, la tercer opción, es Juegos, donde tambien podrás demostrar lo que aprendiste jugando.")
    texto_a_audio("La opción Aprendizaje es donde podrás aprender todo con respecto a la Estructura de un computador. La opción Tests es donde podrás poner en práctica lo que aprendiste mediante exámenes. Y por último, la tercer opción, es Juegos, donde tambien podrás demostrar lo que aprendiste jugando.")
    print("¿Qué opción eliges?")
    texto_a_audio("¿Qué opción eliges?")
    time.sleep(0.5)
    texto_a_audio("¿uno? ¿dos? ¿tres?")

    # SE USA LA FUNCION SLEEP DE LA LIBRERIA TIME PARA PAUSAR UN TIEMPO LA EJECUCION DEL PROGRAMA
    # PARA QUE LA INTERACCION SEA MAS NATURAL
    time.sleep(0.5)

    # PREGUNTA AL USUARIO QUE OPCION ELIGE
    while (1):
        respuesta = enviar_voz()
        print("Tu respuesta " + respuesta)

        if respuesta == "uno":
            print("Elegiste la opcion APRENDIZAJE.")
            texto_a_audio("Elegiste la opcion APRENDIZAJE.")
            print("Muy bien, empecemos entonces.")
            texto_a_audio("Muy bien, empecemos entonces.")

            print(
                "Antes de empezar quisiera hacer una introduccion a la estructura de computadores.")
            texto_a_audio(
                "Antes de empezar quisiera hacer una introduccion a la estructura de computadores.")
            time.sleep(0.5)

            class ImageWindow:
                def __init__(self, root, image_path):
                    self.root = root
                    self.root.title("Imagen")

                    self.image = Image.open(image_path)
                    self.tk_image = ImageTk.PhotoImage(self.image)

                    self.image_label = tk.Label(root, image=self.tk_image)
                    self.image_label.pack()

                def update(self):
                    # Actualizar la ventana (puedes agregar lógica de
                    # actualización aquí si es necesario)
                    self.root.update_idletasks()
                    # Llama a la función de actualización cada 100 ms
                    self.root.after(100, self.update)

            def main():
                root = tk.Tk()
                image_path = "./img/intro/computador.jpg"  # Ruta de la imagen que deseas abrir

                image_window = ImageWindow(root, image_path)
                image_window.update()  # Iniciar la función de actualización

                root.mainloop()

            if __name__ == "__main__":
                main()

            texto_a_audio(datos['aprendizaje'])

            ruta_imagen = "./img/aprendizaje/arquitectura.png"
            cargar_imagen(ruta_imagen)

            print(
                "Como se puede apreciar en la imagen, la estructura de un computador está dado por:")
            texto_a_audio(
                "Como se puede apreciar en la imagen, la estructura de un computador está dado por:")
            print("\n1) Unidad central de proceso (CPU)\n 2) Memoria\n 3) Entrada / Salida\n 4) Sistemas de interconexion (Buses)\n 5) Periféricos\n")
            texto_a_audio(
                "Unidad central de proceso CPU. Memoria. Entrada / Salida. Sistemas de interconexion: Buses. Periféricos.")

            # PREGUNTA AL USUARIO CON QUÉ PARTE DESEA EMPEZAR
            while (not salir):
                print("¿Por cual deseas empezar?")
                texto_a_audio("¿Por cual deseas empezar?")
                time.sleep(0.5)

                # COMPRUEBA QUE EL MENSAJE ENVIADO SEA VALIDO
                while (1):
                    respuesta = enviar_voz()
                    print("Tu respuesta " + respuesta)

                    if respuesta == "cpu":
                        ruta_imagen = "./img/aprendizaje/CPU.png"
                        cargar_imagen(ruta_imagen)
                        texto_a_audio(datos['unidad central de proceso'])
                        seguir()
                        comprobar_respuesta(respuesta, nombre)

                    elif respuesta == "memoria":
                        ruta_imagen = "./img/aprendizaje/memoria.png"
                        cargar_imagen(ruta_imagen)
                        texto_a_audio(datos['memoria'])
                        seguir()
                        comprobar_respuesta(respuesta, nombre)

                    elif respuesta == "entrada salida":
                        ruta_imagen = "./img/aprendizaje/entrada salida.png"
                        cargar_imagen(ruta_imagen)
                        texto_a_audio(datos['entrada salida'])
                        seguir()
                        comprobar_respuesta(respuesta, nombre)

                    elif respuesta == "buses":
                        ruta_imagen = "./img/aprendizaje/buses.png"
                        cargar_imagen(ruta_imagen)
                        texto_a_audio(datos['sistemas de interconexión buses'])
                        seguir()
                        comprobar_respuesta(respuesta, nombre)

                    elif respuesta == "periféricos":
                        ruta_imagen = "./img/aprendizaje/perifericos.jpg"
                        cargar_imagen(ruta_imagen)
                        texto_a_audio(datos['perifericos'])
                        seguir()
                        comprobar_respuesta(respuesta, nombre)

                    elif respuesta != "unidad central de proceso" or respuesta != "memoria" or respuesta != "entrada salida" or respuesta != "sistemas de interconexion buses" or respuesta != "perifericos":
                        print("Perdona, pero por el momento no tengo informacion sobre {}. Prueba con otra OPCION".format(
                            respuesta))
                        texto_a_audio(
                            "Perdona, pero por el momento no tengo informacion sobre {}. Prueba con otra OPCION".format(respuesta))
                        print(
                            "\n1) Unidad central de proceso CPU\n2) Memoria\n3) Entrada / Salida\n4) Sistemas de interconexion: Buses\n5) Periféricos\n")
                    # SI EL MENSAJE ENVIADO NO ES ERRONEO LE PIDE AL USUARIO SELECCIONAR UNA OPCION VALIDA
                    else:
                        print(
                            nombre + " creo que no has respondido con alguna de las instrucciones indicadas anteriormente")
                        texto_a_audio(
                            nombre + " creo que no has respondido con alguna de las instrucciones indicadas anteriormente")
                        print(
                            "\n1) Unidad central de proceso CPU\n 2) Memoria\n 3) Entrada / Salida\n 4) Sistemas de interconexion: Buses\n 5) Periféricos\n")

            break
        elif respuesta == "dos":
            print("Elegiste la opción PRUEBA.")
            texto_a_audio("Elegiste la opción PRUEBA.")
            print("En esta opción tienes para elegir en dar una prueba de entrada sobre PENSAMIENTO COMPUTACIONAL, o dar un examen sobre Estructura de Computadores.")
            texto_a_audio(
                "En esta opción tienes para elegir en dar una prueba de entrada sobre PENSAMIENTO COMPUTACIONAL, o dar un examen sobre Estructura de Computadores.")
            print("¿Cuál eliges?")
            texto_a_audio("¿Cuál eliges?")
            print(
                "\n 1) Prueba de entrada - Pensamiento Computacional\n 2) Examen - Estructura de computadores\n")
            texto_a_audio(
                "¿Prueba de entrada - Pensamiento Computacional? o ¿Examen - Estructura de computadores?")

            while (not salir):
                print("¿Por cual deseas empezar?")
                texto_a_audio("¿Por cual deseas empezar?")
                time.sleep(0.5)

                # COMPRUEBA QUE EL MENSAJE ENVIADO SEA VALIDO
                while (1):
                    respuesta = enviar_voz()
                    if respuesta == "prueba de entrada":

                        print("Tu respuesta " + respuesta)
                        print(
                            "Escogiste: Prueba de entrada de Pensamiento Computacional")
                        texto_a_audio(
                            "Escogiste: Prueba de entrada de Pensamiento Computacional")
                        print("Empezemos con la prueba:")
                        texto_a_audio("Empezemos con la prueba:")
                        
                        pregunta_actual = datos['PE PREGUNTA 01']['pregunta']
                        opciones_actual = datos['PE PREGUNTA 01']['opciones']
                        respuesta_correcta_actual = datos['PE PREGUNTA 01']['respuesta_correcta']
                        texto_a_audio(pregunta_actual)
                        escribir_respuesta(pregunta_actual, opciones_actual, respuesta_correcta_actual)
                        
                        pregunta_actual = datos['PE PREGUNTA 02']['pregunta']
                        opciones_actual = datos['PE PREGUNTA 02']['opciones']
                        respuesta_correcta_actual = datos['PE PREGUNTA 02']['respuesta_correcta']
                        texto_a_audio(pregunta_actual)
                        escribir_respuesta(pregunta_actual, opciones_actual, respuesta_correcta_actual)
                        
                        pregunta_actual = datos['PE PREGUNTA 03']['pregunta']
                        opciones_actual = datos['PE PREGUNTA 03']['opciones']
                        respuesta_correcta_actual = datos['PE PREGUNTA 03']['respuesta_correcta']
                        texto_a_audio(pregunta_actual)
                        escribir_respuesta(pregunta_actual, opciones_actual, respuesta_correcta_actual)
                        
                        """seguir()

                        print(
                            "------------------------------------------------------------------------------------")
                        texto_a_audio(datos['PE PREGUNTA 01'])
                        print(
                            "PRIMERA PREGUNTA: 1. ¿Cuál es el objetivo principal del pensamiento computacional?")
                        print("     \na) Resolver problemas utilizando algoritmos y abstracción.     \nb) Programar robots y sistemas autónomos.     \nc) Diseñar hardware de computadoras.\n")

                        print("¿Cual es tu respuesta?")
                        texto_a_audio("¿Cual es tu respuesta?")
                        texto_a_audio("¿a? ¿b? o ¿c?")

                        respuesta = enviar_voz()
                        print("Tu respuesta " + respuesta)
                        cont = 0

                        if respuesta == "a":
                            print("Tu respuesta es correcta. Muy bien.")
                            texto_a_audio(
                                "Tu respuesta es correcta. Muy bien.")
                            print("TU PUNTAJE ES DE 1 PUNTO")
                        elif respuesta == "b" or respuesta == "c":
                            print("Tu respuesta es incorrecta.")
                            texto_a_audio("Tu respuesta es incorrecta.")
                        time.sleep(0.5)

                        print(
                            "------------------------------------------------------------------------------------")
                        texto_a_audio(datos['PE PREGUNTA 02'])
                        print(
                            "SEGUNDA PREGUNTA: 2. El primer paso del pensamiento computacional es: identificar el problema.")
                        print("     \na) V     \nb) F\n")
                        print("¿Cual es tu respuesta?")
                        texto_a_audio("¿Cual es tu respuesta?")
                        respuesta = enviar_voz()
                        print("Tu respuesta " + respuesta)

                        if respuesta == "verdadero":
                            print("Tu respuesta es correcta. Muy bien.")
                            texto_a_audio(
                                "Tu respuesta es correcta. Muy bien.")
                            print("TU PUNTAJE ES DE 2 PUNTOS")
                        elif respuesta == "falso":
                            print("Tu respuesta es incorrecta.")
                            texto_a_audio("Tu respuesta es incorrecta.")

                        print(
                            "------------------------------------------------------------------------------------")

                        def escribir_respuesta(pregunta, alternativas, respuesta_correcta):
                            print(pregunta)
                            for i, alternativa in enumerate(alternativas, start=1):
                                print(f"{i}. {alternativa}")

                            respuesta_usuario = input(
                                "Escribe el número de la alternativa que crees correcta: ")

                            if respuesta_usuario.isdigit():
                                opcion_elegida = int(respuesta_usuario)
                                if 1 <= opcion_elegida <= len(alternativas):
                                    if alternativas[opcion_elegida - 1] == respuesta_correcta:
                                        print("¡Respuesta correcta!")
                                        texto_a_audio("Respuesta correcta.")
                                        print("TU PUNTAJE ES DE 3 PUNTOS")
                                    else:
                                        print("Respuesta incorrecta.")
                                        texto_a_audio("Respuesta incorrecta.")
                                else:
                                    print("Opción inválida.")
                            else:
                                print(
                                    "Entrada inválida. Por favor, ingresa el número de la alternativa.")

                        pregunta = "¿Qué es un algoritmo en términos de pensamiento computacional?"

                        texto_a_audio(datos['PE PREGUNTA 03'])
                        print(
                            "TERCERA PREGUNTA: ¿Qué es un algoritmo en términos de pensamiento computacional?")
                        alternativas = ["Un patrón de diseño visual", "Un lenguaje de programación",
                                        "Una secuencia de pasos para resolver un problema", "Una representación gráfica de datos"]
                        respuesta_correcta = "Una secuencia de pasos para resolver un problema"
                        escribir_respuesta(
                            pregunta, alternativas, respuesta_correcta)

                        print("¿Quieres seguir aprendiendo?")
                        texto_a_audio("¿Quieres seguir aprendiendo?")
                        time.sleep(0.5)
                        print("Responde con:\n1) Está bien\n2) No gracias")

                        respuesta = enviar_voz()
                        print("Tu respuesta " + respuesta)

                        # COMPRUEbA QUE EL MENSAJE ENVIADO SEA VALIDO
                        if respuesta == "está bien":
                            # ELEGIMOS CON QUÉ OPCIÓN SEGUIR
                            print("Elige la opcion que desees aprender: ")
                            texto_a_audio(
                                "Elige la opcion que desees aprender: ")
                            print("\n1) Aprendizaje\n2) Test\n3) Juegos\n")
                            break
                        elif respuesta == "no gracias":
                            print(
                                "Oh. es una lástima. En ese caso nos veremos en otra ocasión.")
                            texto_a_audio(
                                "Oh. es una lástima. En ese caso nos veremos en otra ocasión.")

                            time.sleep(0.5)
                            print(
                                "Espero que hayas aprendido mucho sobre este tema. Hasta luego.")
                            texto_a_audio(
                                "Espero que hayas aprendido mucho sobre este tema. Hasta luego.")
                            exit(0)
                        # SI EL MENSAJE ENVIADO NO ES ERRONEO LE PIDE AL USUARIO SELECCIONAR UNA OPCION VALIDA
                        else:
                            print(
                                nombre + " creo que no has respondido con alguna de las instrucciones indicadas anteriormente")
                            texto_a_audio(
                                nombre + " creo que no has respondido con alguna de las instrucciones indicadas anteriormente")
                            print("Responde con:\n1) Esta bien.\n2) No gracias") """

        elif respuesta == "tres":

            print("Elegiste la opción JUEGOS.")
            texto_a_audio("Elegiste la opción JUEGOS.")

            print("El primer juego consta en contestar las preguntas, haciendo click en la imagen que crees que es la respuesta.")
            texto_a_audio(
                "El primer juego consta en contestar las preguntas, haciendo click en la imagen que crees que es la respuesta.")

            class ComputerStructureQuizApp:
                def __init__(self, root):
                    self.root = root
                    self.root.title("JUEGO: ESTRUCTURA DE UN COMPUTADOR")

                    self.question_label = tk.Label(
                        root, text="¿Qué componente almacena datos de manera temporal en la CPU?")
                    self.question_label.pack()

                    self.image_frame = tk.Frame(root)
                    self.image_frame.pack()

                    self.image_labels = []
                    for _ in range(4):
                        image_label = tk.Label(self.image_frame, image=None)
                        image_label.pack(side=tk.LEFT, padx=10)
                        image_label.bind("<Button-1>", self.check_answer)
                        self.image_labels.append(image_label)

                    self.correct_answer = 0  # Índice de la respuesta correcta
                    self.load_question()

                def load_question(self):
                    # Cargar la pregunta y las imágenes aquí
                    question = "¿Qué componente almacena datos de manera temporal en la CPU?"
                    options = ["RAM", "GPU", "HDD", "CPU"]

                    self.question_label.config(text=question)
                    # Respuesta correcta en la posición 0 (RAM)
                    self.correct_answer = 0

                    for i in range(4):
                        image_path = f"option_{i+1}.png"
                        image = Image.open(image_path)
                        image = image.resize((200, 200))
                        photo = ImageTk.PhotoImage(image)
                        self.image_labels[i].config(image=photo)
                        self.image_labels[i].image = photo

                def check_answer(self, event):
                    clicked_label = event.widget
                    clicked_index = self.image_labels.index(clicked_label)

                    if clicked_index == self.correct_answer:
                        print("¡Respuesta correcta!")
                        texto_a_audio("Respuesta correcta.")
                    else:
                        print("Respuesta incorrecta.")
                        texto_a_audio("Respuesta incorrecta.")
                    self.load_question()

            if __name__ == "__main__":
                root = tk.Tk()
                app = ComputerStructureQuizApp(root)
                root.mainloop()

        # SI EL MENSAJE ENVIADO NO ES ERRONEO LE PIDE AL USUARIO SELECCIONAR UNA OPCION VALIDA
        else:
            print(
                nombre + " creo que no has respondido con alguna de las instrucciones indicadas anteriormente")
            texto_a_audio(
                nombre + " creo que no has respondido con alguna de las instrucciones indicadas anteriormente")
            print("Responde con una de las alternativas mencionadas.")
            texto_a_audio("Responde con una de las alternativas mencionadas.")
