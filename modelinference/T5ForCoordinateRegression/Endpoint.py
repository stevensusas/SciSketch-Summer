import requests

url = "http://127.0.0.1:5000/predict"
data = {
    "abstract": """
    Neutrosophic sets provide greater versatility in dealing with a variety of
    uncertainties, including independent, partially independent, and entirely
    dependent scenarios, which q-ROF soft sets cannot handle. Indeterminacy,
    on the other hand, is ignored completely or partially by q-ROF soft sets.
    To address this issue, this study offers a unique novel concept as known as
    q-RONSS, which combines neutrosophic set with q-ROF soft set. This technique
    addresses vagueness using a set of truth, indeterminacy, and false membership
    degrees associated with the parametrization tool, with the condition that the
    sum of the qth power of the truth, indeterminacy, and false membership degrees
     be less than or equal to one. In addition, this study outlines operational
     laws for the suggested structure. The main purpose this article is to define
     some averaging and geometric operators based on the q-rung orthopair neutrosophic
      soft set. Furthermore, this article provides a step-by-step method and a
      mathematical model for the suggested techniques. To solve a MADM issue,
      this research article proposes a numerical example of people selection for
       a specific position in a real estate business based on a variety of criteria.
        Finally, to demonstrate the proposed model's superiority and authenticity,
        this article performs several analyses, including sensitivity analysis, to
        address the reliability and influence of various parameter "q" values on the
         alternatives and the ultimate results.
    """,
    "text": "Neutrosophic sets"
}

response = requests.post(url, json=data)

if response.status_code == 200:
    result = response.json()
    print("Normalized Coordinates:")
    print(f"x: {result['normalized_coordinates']['x']}")
    print(f"y: {result['normalized_coordinates']['y']}")
    print("Denormalized Coordinates:")
    print(f"x: {result['denormalized_coordinates']['x']}")
    print(f"y: {result['denormalized_coordinates']['y']}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
