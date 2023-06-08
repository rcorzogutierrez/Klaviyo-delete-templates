import requests

def get_all_filtered_templates(api_key, filter_criteria):
    url = "https://a.klaviyo.com/api/templates/"
    headers = {
        "accept": "application/json",
        "revision": "2023-02-22",
        "Authorization": f"Klaviyo-API-Key {api_key}"
    }
    params = {
        "filter": filter_criteria
    }

    all_templates = []
    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            templates = data.get("data", [])
            all_templates.extend(templates)
            url = data.get("links", {}).get("next")
        else:
            raise Exception(f"Error al obtener los templates. Código de respuesta: {response.status_code}")
        
        params = {}  # borra los parámetros para las siguientes solicitudes, ya que se incluirán en el url

    return all_templates


def delete_template(api_key, template_id):
    url = f"https://a.klaviyo.com/api/v1/email-template/{template_id}?api_key={api_key}"
    headers = {"accept": "application/json"}
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print(f"El template con ID {template_id} ha sido eliminado correctamente.")
    else:
        print(f"Error al eliminar el template con ID {template_id}. Código de respuesta: {response.status_code}")


def main():
    api_key = "your-api-key"
    filter_criteria = 'greater-or-equal(updated,2023-01-01T00:00:00Z),less-than(updated,2023-06-01T00:00:00Z)'
    templates = get_all_filtered_templates(api_key, filter_criteria)

    if templates:
        print("Lista de templates:")
        print("{:<5} {:<15} {:<25} {:<25} {:<25}".format("No.", "ID", "Nombre", "Creado", "Actualizado"))
        for i, template in enumerate(templates, start=1):
            template_id = template.get("id")
            template_name = template.get("attributes").get("name")
            created_at = template.get("attributes").get("created")
            updated_at = template.get("attributes").get("updated")
            print("{:<5} {:<15} {:<25} {:<25} {:<25}".format(i, template_id, template_name, created_at, updated_at))

        selection = input("Seleccione los números de los templates que desea eliminar (separe los números por comas o rango con guión): ")
        selected_indices = []
        for part in selection.split(","):
            if "-" in part:
                start, end = map(int, part.split("-"))
                selected_indices.extend(range(start, end + 1))
            else:
                selected_indices.append(int(part.strip()))

        for index in selected_indices:
            if 1 <= index <= len(templates):
                template_id = templates[index - 1].get("id")
                delete_template(api_key, template_id)
            else:
                print(f"Número inválido: {index}. Ignorando template.")

    else:
        print("No se encontraron templates.")

if __name__ == "__main__":
    main()
