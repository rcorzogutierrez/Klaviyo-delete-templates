from klaviyo_api import KlaviyoAPI
from tabulate import tabulate

def get_filtered_templates(api_key, filter_criteria):
    # Crear una instancia de KlaviyoAPI
    klaviyo_api = KlaviyoAPI(api_key, max_delay=60, max_retries=3, test_host=None)

    # Obtener todos los templates
    response = klaviyo_api.Templates.get_templates(filter=filter_criteria)

    # Verificar la respuesta de la API
    if 'errors' in response:
        raise Exception("Error en la solicitud de los templates")

    # Acceder a los resultados
    templates = response['data']  # lista de templates

    return templates

def print_templates(templates):
    # Verificar si hay templates
    if not templates:
        print("No se encontraron templates que cumplan con los criterios de búsqueda.")
        return

    # Crear una lista de filas para la tabla
    table_rows = []
    for template in templates:
        name = template['attributes']['name']
        template_id = template['id']
        table_rows.append([template_id, name])

    # Definir las cabeceras de la tabla
    table_headers = ["ID", "Nombre"]

    # Imprimir la tabla
    table = tabulate(table_rows, headers=table_headers, tablefmt="grid")
    print(table)

def main():
    # Definir el filtro por fecha de creación
    filter_criteria = 'greater-than(created,2023-01-01T00:00:00Z)'

    # Obtener los templates filtrados
    filtered_templates = get_filtered_templates("pk_7d11a542a461ae7c49b6132da6f9d1d939", filter_criteria)

    # Verificar si hay templates que cumplen con los criterios de búsqueda
    if not filtered_templates:
        print("No se encontraron templates que cumplan con los criterios de búsqueda.")
        return

    # Filtrar los templates por nombre que contenga "EMCA"
    emca_templates = [template for template in filtered_templates if "EMCA" in template['attributes']['name']]

    # Mostrar los templates en una tabla
    print_templates(emca_templates)

if __name__ == "__main__":
    main()
