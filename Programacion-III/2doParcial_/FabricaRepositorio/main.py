from datetime import date 
from output.scimeta.dominio import Autor, DocumentoCientifico
from output.scimeta.procesamiento import FabricaParsers
from FabricaParsers.validaciones import EspecificacionDocumentoActivo,EspecificacionTipoSoportado
from FabricaParsers.persistencia import FabricaRepositorio
from FabricaRepositorio.orquestador import ServicioOrquestacion

def construir_documento_de_ejemplo(): 

    autor_uno = Autor(
        id_autor=1, nombre="Ana", apellido="Pérez",
        afiliacion="UBA", fecha_registro=date(2019, 3, 10),
    )
    autor_dos = Autor(
        id_autor=2, nombre="Luis", apellido="Gómez",
        afiliacion="UNLP", fecha_registro=date(2021, 7, 1),
    )

    documento = DocumentoCientifico(
        id_documento=101,
        titulo="Arquitecturas flexibles para procesamiento de PDFs",
        resumen="Estudio sobre patrones de diseño aplicados a ETL.",
        fecha_publicacion=date(2024, 5, 20),
        path_documento="/repositorio/papers/101.pdf",
        nombre_documento="paper_101.pdf",
        likes=15,
    )
    documento.agregar_autores([autor_uno, autor_dos])
    return documento    

def main():
    tipo_persistencia_configurada = "memoria"

    repositorio = FabricaRepositorio.crear(
        tipo_persistencia_configurada)

    especificacion = (
        EspecificacionDocumentoActivo()
        & EspecificacionTipoSoportado(FabricaParsers.tipos_soportados())
    )

    servicio = ServicioOrquestacion(
        repositorio_resultados=repositorio,
        especificacion_validacion=especificacion,
    )

    documento = construir_documento_de_ejemplo()
    print("¿Atributos completos?",
          documento.tiene_atributos_completos())

    resultado = servicio.procesar_documento(documento)
    print("Resultado procesado:", resultado)

    prompt = servicio.generar_prompt_para(documento.id)
    print("\n--- PROMPT GENERADO ---\n")
    print(prompt)

    autor_demo = documento.autores[0]
    print(f"\nAutor: {autor_demo.nombre_completo()}, "
          f"antigüedad: {autor_demo.antiguedad_en_anios()} años")

if __name__ == "__main__":
    main()